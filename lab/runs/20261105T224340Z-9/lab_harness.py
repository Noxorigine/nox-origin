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
import os
import random
import signal
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab_specs  # noqa: E402

BANNED_NAMES = {"eval", "exec", "compile", "open", "__import__", "input", "globals", "locals", "getattr",
                "setattr", "delattr", "vars", "breakpoint", "exit", "quit", "help", "memoryview", "type", "object"}
SAFE = ["abs", "all", "any", "bool", "dict", "enumerate", "filter", "float", "int", "isinstance", "len", "list",
        "map", "max", "min", "pow", "range", "reversed", "set", "sorted", "str", "sum", "tuple", "zip", "divmod",
        "ord", "chr", "next", "iter", "Exception", "ValueError", "IndexError", "KeyError", "TypeError", "ZeroDivisionError", "True", "False", "None", "round"]
CALL_SECONDS = 3
CHILD_SECONDS = 40


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
        if isinstance(node, ast.Attribute) and (node.attr.startswith("__") or node.attr in forbidden):
            return f"forbidden_attribute:{node.attr}"
        if isinstance(node, ast.FunctionDef) and node.name == "solve":
            found = True
    return None if found else "no_solve_function"


def short(value, n=110):
    text = repr(value)
    return text if len(text) <= n else text[: n - 3] + "..."


class Timeout(Exception):
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
        working = copy.deepcopy(args)
        try:
            signal.setitimer(signal.ITIMER_REAL, CALL_SECONDS)
            out = solve(*working)
            signal.setitimer(signal.ITIMER_REAL, 0)
        except Timeout:
            first = {"input": short(original), "reason": "timeout"}
            continue
        except BaseException as exc:  # candidate code is untrusted
            signal.setitimer(signal.ITIMER_REAL, 0)
            first = {"input": short(original), "reason": f"exception:{type(exc).__name__}"}
            continue
        expected = spec["ref"](*copy.deepcopy(original))
        if (not weak) and working != original:
            first = {"input": short(original), "reason": "input_modified"}
        elif weak:
            if not spec["weak"](original, out):
                first = {"input": short(original), "reason": "weak_check_failed"}
        else:
            try:
                same = [list(x) for x in out] == expected if spec is lab_specs.SPECS["merge_intervals"] else out == expected
            except TypeError:
                same = False
            if not same:
                first = {"input": short(original), "expected": short(expected), "got": short(out), "reason": "wrong_output"}
    return {"passed": first is None, "cases": count, "first_failure": first}


def child(spec_name, path, weak_only):
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
        resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
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
    sys.stdout = real_out
    passed = all(layer["passed"] for layer in layers.values())
    result.update({"status": "passed_all" if passed else "failed", "layers": layers})
    real_out.write(json.dumps(result))


def run_child(spec_name, path, weak):
    try:
        proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "child", spec_name, path, "1" if weak else "0"],
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
        full = run_child(spec_name, path, False)
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


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "all":
        main_all(sys.argv[2])
    elif len(sys.argv) >= 5 and sys.argv[1] == "child":
        child(sys.argv[2], sys.argv[3], sys.argv[4] == "1")
