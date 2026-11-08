def solve(line: str):
    fields = []
    i = 0
    n = len(line)
    while i <= n:
        if i == n:
            # end of line reached, add empty field if line ends with comma
            fields.append("")
            break
        if line[i] == '"':
            # quoted field
            i += 1
            start = i
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
            # after quoted field, expect comma or end
            if i < n and line[i] == ',':
                i += 1
                if i == n:
                    # trailing comma, next loop will add empty field
                    continue
            elif i == n:
                break
            else:
                # stray characters after closing quote, treat as part of field
                # (RFC 4180 disallows this, but we handle gracefully)
                while i < n and line[i] != ',':
                    fields[-1] += line[i]
                    i += 1
                if i < n and line[i] == ',':
                    i += 1
        else:
            # unquoted field
            start = i
            while i < n and line[i] != ',':
                i += 1
            fields.append(line[start:i])
            if i < n and line[i] == ',':
                i += 1
                if i == n:
                    # trailing comma leads to empty field
                    fields.append("")
                    break
    # handle case of empty input line
    if len(fields) == 0:
        return [""]
    return fields
