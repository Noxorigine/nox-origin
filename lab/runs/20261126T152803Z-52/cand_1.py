def solve(line):
    fields = []
    i, n = 0, len(line)
    while True:
        if i >= n:
            # End of line, add empty field if line ends with comma or line empty
            if line.endswith(',') or n == 0:
                fields.append('')
            break
        if line[i] == '"':
            # Quoted field
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
            # After closing quote, expect comma or end
            while i < n and line[i] != ',':
                # Skip any characters until comma (RFC allows only comma or end)
                i += 1
            fields.append(''.join(field))
        else:
            # Unquoted field
            start = i
            while i < n and line[i] != ',':
                i += 1
            fields.append(line[start:i])
        # Skip comma separator
        if i < n and line[i] == ',':
            i += 1
            # If comma is last character, loop will add empty field on next iteration
        else:
            # No more commas
            if i >= n:
                break
    return fields
