import os
import tokenize
import io


def remove_comments(source_code):
    io_obj = io.StringIO(source_code)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    try:
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += " " * (start_col - last_col)
            if token_type == tokenize.COMMENT:
                pass
            else:
                out += token_string
            last_col = end_col
            last_lineno = end_line
    except tokenize.TokenError:
        return source_code
    return out


for root, _, files in os.walk("."):
    if "node_modules" in root or ".git" in root or ".venv" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            clean = remove_comments(content)
            lines = [line for line in clean.splitlines() if line.strip()]
            clean = "\n".join(lines) + "\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(clean)
