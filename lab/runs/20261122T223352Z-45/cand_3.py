def solve(line: str):
    fields = []
    i = 0
    n = len(line)
    while i <= n:
        if i == n:
            # end of line reached, add last empty field if line ends with comma
            if line.endswith(','):
                fields.append('')
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
            # after closing quote, expect comma or end
            if i < n and line[i] == ',':
                i += 1
                continue
            elif i == n:
                break
            else:
                # stray characters after closing quote, treat as part of field per RFC (shouldn't happen)
                # consume until next comma
                while i < n and line[i] != ',':
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
                continue
            else:
                break
    # handle empty line
    if line == '':
        return ['']
    return fields
