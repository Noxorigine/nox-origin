def solve(line):
    fields = []
    i, n = 0, len(line)
    cur = ''
    in_quotes = False
    while i < n:
        ch = line[i]
        if in_quotes:
            if ch == '"':
                # Look ahead for escaped quote
                if i + 1 < n and line[i + 1] == '"':
                    cur += '"'
                    i += 1
                else:
                    in_quotes = False
            else:
                cur += ch
        else:
            if ch == ',':
                fields.append(cur)
                cur = ''
            elif ch == '"':
                # start of quoted field
                in_quotes = True
            else:
                cur += ch
        i += 1
    # Append last field (handles trailing comma)
    fields.append(cur)
    return fields
