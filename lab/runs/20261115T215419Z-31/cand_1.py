def solve(line: str):
    fields = []
    i = 0
    n = len(line)
    while i <= n:
        if i == n:
            # end of line, add empty field if line ends with comma
            fields.append('')
            break
        if line[i] == '"':
            # quoted field
            i += 1
            start = i
            field = ''
            while i < n:
                if line[i] == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        field += '"'
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    field += line[i]
                    i += 1
            fields.append(field)
            # after closing quote may be comma or end
            if i < n and line[i] == ',':
                i += 1
                continue
            elif i == n:
                # line ends after quoted field
                break
            else:
                # unexpected character, treat as literal
                # continue parsing as unquoted until comma
                while i < n and line[i] != ',':
                    fields[-1] += line[i]
                    i += 1
                if i < n and line[i] == ',':
                    i += 1
                continue
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
    # handle case of empty input line
    if line == '':
        return ['']
    return fields
