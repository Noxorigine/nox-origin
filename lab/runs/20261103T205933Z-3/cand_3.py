def solve(line: str):
    fields = []
    i, n = 0, len(line)
    while True:
        if i >= n:
            fields.append("")
            break
        if line[i] == '"':
            i += 1
            field = []
            while i < n:
                if line[i] == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        field.append('"')
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    field.append(line[i])
                    i += 1
            fields.append(''.join(field))
        else:
            start = i
            while i < n and line[i] != ',':
                i += 1
            fields.append(line[start:i])
        if i < n and line[i] == ',':
            i += 1
            if i >= n:
                fields.append("")
                break
        else:
            break
    return fields
