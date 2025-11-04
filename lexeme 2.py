import re
import keyword

# Get all Python keywords
python_keywords = set(keyword.kwlist)

# Define token categories and regex patterns for Python
token_spec = [
    ("NUMBER",   r"-?\d+(\.\d+)?"),                # int or float
    ("STRING",   r"(['\"]).*?\1"),                 # string literals ('...' or "...")
    ("ID",       r"[A-Za-z_]\w*"),                 # identifiers
    ("OP",       r"==|!=|<=|>=|->|:=|\+|-|\*|/|%|=|<|>|\*\*|//"),  # operators
    ("DELIM",    r"[\(\){}\[\],.:;]"),             # delimiters
    ("COMMENT",  r"#.*"),                          # single-line comments
    ("NEWLINE",  r"\n"),                           # newlines
    ("SKIP",     r"[ \t]+"),                       # whitespace
    ("MISMATCH", r"."),                            # any other character
]

# Compile regex
token_re = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec), re.DOTALL)

def lexer(code):
    tokens = []
    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "ID":
            if value in python_keywords:
                tokens.append(("KEYWORD", value))
            else:
                tokens.append(("IDENTIFIER", value))
        elif kind == "NUMBER":
            tokens.append(("NUM", float(value) if "." in value else int(value)))
        elif kind == "STRING":
            tokens.append(("STRING", value))
        elif kind == "OP":
            tokens.append(("OPERATOR", value))
        elif kind == "DELIM":
            tokens.append(("DELIMITER", value))
        elif kind == "COMMENT":
            continue   # ignore comments
        elif kind == "NEWLINE":
            continue   # ignore newlines (optional)
        elif kind == "SKIP":
            continue   # ignore spaces/tabs
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected char: {value}")
    return tokens


# ----------------------------
# Example: Python input program
# ----------------------------
code = """
def limited_square(x):
    
    return 100 if x <= -10.0 or x >= 10.0 else x * x
"""

tokens = lexer(code)
for t in tokens:
    print(t)
