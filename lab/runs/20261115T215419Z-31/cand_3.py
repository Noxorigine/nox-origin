def solve(line):
    fields = []
    i, n = 0, len(line)
    while i <= n:
        if i == n:
            # end of line, add empty field if line ends with comma
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
            # after quoted field expect comma or end
            if i < n and line[i] == ',':
                i += 1
                if i == n:
                    # trailing comma yields empty field
                    fields.append("")
                    break
            else:
                # end of line
                if i == n:
                    break
        else:
            # unquoted field
            start = i
            while i < n and line[i] != ',':
                i += 1
            fields.append(line[start:i])
            if i < n and line[i] == ',':
                i += 1
                if i == n:
                    fields.append("")
                    break
    return fields
