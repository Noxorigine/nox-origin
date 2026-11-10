"""NØX Lab harness. Runs untrusted candidate code in short-lived child processes.
Modes:
  python3 -I lab_harness.py all <workdir>          -> JSON on stdout (orchestrator)
  python3 -I lab_harness.py child <spec> <file> <weak 0|1>  -> JSON on stdout (one candidate)
The orchestrator must itself run inside a network-less, unprivileged sandbox."""
import ast
import builtins
import copy
import hashlib
import json
import math
import os
import random
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab_specs  # noqa: E402

BANNED_NAMES = {"eval", "exec", "compile", "open", "__import__", "input", "globals", "locals", "getattr",
                "setattr", "delattr", "vars", "breakpoint", "exit", "quit", "help", "memoryview", "type", "object"}
# Attribute names that reach frames, code objects or string-format traversal: never needed for these tasks.
BANNED_ATTRS = {"gi_frame", "gi_code", "gi_yieldfrom", "gi_running", "f_back", "f_globals", "f_locals", "f_builtins",
                "f_code", "f_trace", "tb_frame", "tb_next", "cr_frame", "cr_code", "cr_await", "cr_origin", "ag_frame",
                "ag_code", "ag_await", "func_globals", "func_code", "co_code", "co_consts", "co_names", "mro",
                "format", "format_map", "with_traceback", "add_note"}
SAFE = ["abs", "all", "any", "bool", "dict", "enumerate", "filter", "float", "int", "isinstance", "len", "list",
        "map", "max", "min", "pow", "range", "reversed", "set", "sorted", "str", "sum", "tuple", "zip", "divmod",
        "ord", "chr", "next", "iter", "Exception", "ValueError", "IndexError", "KeyError", "TypeError", "ZeroDivisionError", "True", "False", "None", "round"]
CALL_SECONDS = 3
CHILD_SECONDS = 90


def static_check(source, forbidden):
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return f"syntax_error:{exc.msg}"
    if len(source) > 6000:
        return "too_long"
    found = False
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return "import_not_allowed"
        if isinstance(node, ast.Name) and (node.id in BANNED_NAMES or node.id in forbidden):
            return f"forbidden_name:{node.id}"
        if isinstance(node, ast.Attribute) and (node.attr.startswith("__") or node.attr in forbidden or node.attr in BANNED_ATTRS):
            return f"forbidden_attribute:{node.attr}"
        if isinstance(node, ast.FunctionDef) and node.name == "solve":
            found = True
    return None if found else "no_solve_function"


def short(value, n=110):
    text = repr(value)
    return text if len(text) <= n else text[: n - 3] + "..."


def show(args, n=110):
    """Readable call arguments: f([1, 2]) rather than ([1, 2],)."""
    text = ", ".join(repr(a) for a in args)
    return text if len(text) <= n else text[: n - 3] + "..."


MUTATORS = ("append", "extend", "insert", "remove", "pop", "clear", "sort", "reverse",
            "__setitem__", "__delitem__", "__iadd__", "__imul__")


def tracked(values, log):
    """A list that records every mutating call. The log lives in a closure the candidate cannot reach."""
    class Tracked(list):
        pass

    def make(base, label):
        def method(self, *a, **k):
            log.append(label)
            return base(self, *a, **k)
        return method

    for name in MUTATORS:
        setattr(Tracked, name, make(getattr(list, name), name))
    return Tracked(values)


class Timeout(BaseException):
    pass


def _alarm(signum, frame):
    raise Timeout()


def run_layer(solve, spec, cases, weak):
    count = 0
    first = None
    for args in cases:
        count += 1
        if first is not None:
            continue  # keep counting, but report only the first counterexample
        original = copy.deepcopy(args)
        log = []
        if weak:
            working = copy.deepcopy(args)
        else:
            working = tuple(tracked(a, log) if isinstance(a, list) else a for a in copy.deepcopy(args))
        try:
            signal.setitimer(signal.ITIMER_REAL, CALL_SECONDS)
            out = solve(*working)
            signal.setitimer(signal.ITIMER_REAL, 0)
        except Timeout:
            first = {"input": show(original), "reason": "timeout"}
            continue
        except BaseException as exc:  # candidate code is untrusted
            signal.setitimer(signal.ITIMER_REAL, 0)
            first = {"input": show(original), "reason": f"exception:{type(exc).__name__}"}
            continue
        expected = spec["ref"](*copy.deepcopy(original))
        if (not weak) and working != original:
            first = {"input": show(original), "reason": "input_modified"}
        elif (not weak) and log:
            first = {"input": show(original), "reason": "input_mutated_during_execution"}
        elif (not weak) and isinstance(out, list) and any(out is arg for arg in working if isinstance(arg, list)):
            first = {"input": show(original), "reason": "returned_input_object"}
        elif weak:
            if not spec["weak"](original, out):
                first = {"input": show(original), "reason": "weak_check_failed"}
        else:
            try:
                same = [list(x) for x in out] == expected if spec is lab_specs.SPECS["merge_intervals"] else out == expected
            except TypeError:
                same = False
            if not same:
                first = {"input": show(original), "expected": short(expected), "got": short(out), "reason": "wrong_output"}
    return {"passed": first is None, "cases": count, "first_failure": first}



def probe_scaling(solve, spec, key="scale"):
    """Informational only: how the running time grows when the input is 4 times larger (timing is noisy on shared runners)."""
    sizes = (1000, 2000, 4000)
    times = []
    for n in sizes:
        args = spec[key](n, random.Random(4242 + n))
        best = None
        for _ in range(3 if n < 2000 else 2):
            work = copy.deepcopy(args)
            try:
                signal.setitimer(signal.ITIMER_REAL, CALL_SECONDS)
                start = time.perf_counter()
                solve(*work)
                elapsed = time.perf_counter() - start
                signal.setitimer(signal.ITIMER_REAL, 0)
            except Timeout:
                return {"label": "too_slow", "timeout_at": n, "times_ms": [round(t * 1000, 2) for t in times]}
            except BaseException:
                signal.setitimer(signal.ITIMER_REAL, 0)
                return {"label": "probe_error"}
            best = elapsed if best is None else min(best, elapsed)
        times.append(best)
    if times[2] < 5e-5:
        return {"label": "too_fast", "times_ms": [round(t * 1000, 3) for t in times], "sizes": list(sizes)}
    first, last = max(times[0], 2e-5), max(times[2], 2e-5)
    exponent = math.log(last / first) / math.log(4)
    if exponent <= 1.45:
        label = "near_linear"
    elif exponent >= 1.75:
        label = "near_quadratic"
    else:
        label = "in_between"
    return {"label": label, "exponent": round(exponent, 2), "growth": round(last / first, 1),
            "times_ms": [round(t * 1000, 2) for t in times], "sizes": list(sizes)}

def child(spec_name, path, weak_only, extended=False, probe=False):
    spec = lab_specs.SPECS[spec_name]
    source = open(path, encoding="utf-8").read()
    is_mutant = os.path.basename(path).startswith("mutant_")
    problem = static_check(source, [] if is_mutant else spec["forbidden"])
    real_out = sys.stdout
    result = {"digest": hashlib.sha256(source.strip().encode()).hexdigest()[:12]}
    if problem:
        result.update({"status": "rejected_static", "reason": problem})
        real_out.write(json.dumps(result))
        return
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (75, 75))
        resource.setrlimit(resource.RLIMIT_AS, (768 * 1024 * 1024, 768 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
        resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
    except Exception:
        pass
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    safe = {name: getattr(builtins, name) for name in SAFE if hasattr(builtins, name)}
    safe["print"] = lambda *a, **k: None
    namespace = {"__builtins__": safe}
    signal.signal(signal.SIGALRM, _alarm)
    try:
        signal.setitimer(signal.ITIMER_REAL, CALL_SECONDS)
        exec(compile(source, "candidate", "exec"), namespace)  # noqa: S102 - sandboxed by the caller
        signal.setitimer(signal.ITIMER_REAL, 0)
        solve = namespace["solve"]
    except BaseException as exc:
        sys.stdout = real_out
        result.update({"status": "error", "reason": f"load_failed:{type(exc).__name__}"})
        real_out.write(json.dumps(result))
        return
    rng = random.Random(20260101)
    layers = {}
    layers["L1_exhaustive_tiny"] = run_layer(solve, spec, spec["tiny"](), weak_only)
    layers["L2_seeded_random"] = run_layer(solve, spec, spec["rand"](rng), weak_only)
    layers["L3_heldout_adversarial"] = run_layer(solve, spec, spec["held"](random.Random(777)), weak_only)
    if extended and all(layer["passed"] for layer in layers.values()):
        total, first_fail = 0, None
        for seed in range(100, 106):
            part = run_layer(solve, spec, spec["rand"](random.Random(seed)), False)
            total += part["cases"]
            if first_fail is None and part["first_failure"] is not None:
                first_fail = part["first_failure"]
        layers["L4_extended_random"] = {"passed": first_fail is None, "cases": total, "first_failure": first_fail}
    passed = all(layer["passed"] for layer in layers.values())
    scaling = None
    adv_scaling = None
    if probe and passed and "scale" in spec:
        scaling = probe_scaling(solve, spec)
        if "scale_adv" in spec and scaling.get("label") != "too_slow":
            adv_scaling = probe_scaling(solve, spec, "scale_adv")
    sys.stdout = real_out
    result.update({"status": "passed_all" if passed else "failed", "layers": layers})
    if scaling is not None:
        result["scaling"] = scaling
    if scaling is not None and "scale_adv" in spec and scaling.get("label") != "too_slow":
        result["scaling_adv"] = adv_scaling
    real_out.write(json.dumps(result))


def run_child(spec_name, path, weak, extended=False, probe=False):
    try:
        proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "child", spec_name, path, "1" if weak else "0", "1" if extended else "0", "1" if probe else "0"],
                              capture_output=True, text=True, timeout=CHILD_SECONDS, cwd=HERE, env={"PATH": "/usr/bin:/bin"})
    except subprocess.TimeoutExpired:
        return {"status": "error", "reason": "child_timeout"}
    try:
        return json.loads(proc.stdout)
    except Exception:
        return {"status": "error", "reason": f"child_crash:{proc.returncode}"}


def main_all(workdir):
    meta = json.load(open(os.path.join(workdir, "meta.json"), encoding="utf-8"))
    spec_name = meta["spec"]
    spec = lab_specs.SPECS[spec_name]
    out = {"spec": spec_name, "corpus_version": lab_specs.VERSION, "sandbox": os.environ.get("LAB_SANDBOX", "none"), "candidates": [], "mutants": []}
    for item in meta["candidates"]:
        path = os.path.join(workdir, item["file"])
        full = run_child(spec_name, path, False, True, True)
        full["file"] = item["file"]
        out["candidates"].append(full)
    for name, code in spec["mutants"].items():
        path = os.path.join(workdir, f"mutant_{name}.py")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(code)
        full = run_child(spec_name, path, False)
        weak = run_child(spec_name, path, True)
        out["mutants"].append({"name": name,
                               "full_suite_rejects": full.get("status") == "failed",
                               "weak_check_accepts": weak.get("status") == "passed_all"})
    sys.stdout.write(json.dumps(out))


def main_submissions(workdir):
    meta = json.load(open(os.path.join(workdir, "requests.json"), encoding="utf-8"))
    out = {"corpus_version": lab_specs.VERSION, "sandbox": os.environ.get("LAB_SANDBOX", "none"), "results": []}
    for item in meta.get("requests", []):
        name = item.get("spec")
        if name not in lab_specs.SPECS:
            out["results"].append({"file": item.get("file"), "status": "error", "reason": "unknown_spec"})
            continue
        res = run_child(name, os.path.join(workdir, item["file"]), False, True, True)
        res["file"] = item["file"]
        out["results"].append(res)
    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "all":
        main_all(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "submissions":
        main_submissions(sys.argv[2])
    elif len(sys.argv) >= 5 and sys.argv[1] == "child":
        child(sys.argv[2], sys.argv[3], sys.argv[4] == "1", len(sys.argv) > 5 and sys.argv[5] == "1", len(sys.argv) > 6 and sys.argv[6] == "1")
