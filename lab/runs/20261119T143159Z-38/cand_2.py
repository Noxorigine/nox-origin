def solve(line: str):
    fields = []
    field = []
    i = 0
    n = len(line)
    in_quotes = False
    while i < n:
        c = line[i]
        if in_quotes:
            if c == '"':
                # Look ahead for escaped quote
                if i + 1 < n and line[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(c)
        else:
            if c == ',':
                fields.append(''.join(field))
                field = []
            elif c == '"':
                # start of quoted field (only if at beginning of field)
                if not field:
                    in_quotes = True
                else:
                    # stray quote, treat as literal
                    field.append(c)
            else:
                field.append(c)
        i += 1
    # Append last field (even if line is empty)
    fields.append(''.join(field))
    return fields
