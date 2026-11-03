def solve(line: str):
    fields = []
    i, n = 0, len(line)
    while i <= n:
        if i == n:
            # End of line reached, add last field (could be after trailing comma)
            fields.append("")
            break
        if line[i] == ',':
            # Empty field before comma
            fields.append("")
            i += 1
            continue
        if line[i] == '"':
            # Quoted field
            i += 1
            start = i
            field_chars = []
            while i < n:
                if line[i] == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        field_chars.append('"')
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    field_chars.append(line[i])
                    i += 1
            fields.append(''.join(field_chars))
            # After closing quote, expect comma or end
            if i < n and line[i] == ',':
                i += 1
            elif i < n:
                # Unexpected character after closing quote, treat rest as part of field
                # (RFC 4180 says this is malformed, but we include it)
                while i < n and line[i] != ',':
                    fields[-1] += line[i]
                    i += 1
                if i < n and line[i] == ',':
                    i += 1
        else:
            # Unquoted field
            start = i
            while i < n and line[i] != ',':
                i += 1
            fields.append(line[start:i])
            if i < n and line[i] == ',':
                i += 1
    # Adjust for trailing comma producing extra empty field
    if line and line[-1] == ',':
        if not (fields and fields[-1] == ""):
            fields.append("")
    # Special case: empty line should return [""] not []
    if line == "":
        return [""]
    return fields
