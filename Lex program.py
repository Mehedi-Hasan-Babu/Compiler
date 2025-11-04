import re

# -----------------------------
# Token definitions
# -----------------------------
TOKENS = {
    "IF": r"\bif\b",
    "THEN": r"\bthen\b",
    "ELSE": r"\belse\b",
    "RELOP_LT": r"<",
    "RELOP_LE": r"<=",
    "RELOP_EQ": r"=",
    "RELOP_NE": r"<>",
    "RELOP_GT": r">",
    "RELOP_GE": r">=",
    "NUMBER": r"\d+(\.\d+)?(E[+-]?\d+)?",
    "ID": r"[A-Za-z][A-Za-z0-9]*",
    "WS": r"[ \t\n]+",  # whitespace
}

# -----------------------------
# Lexer implementation
# -----------------------------
def lexer(input_code):
    tokens = []
    i = 0
    while i < len(input_code):
        match_found = False
        for token_type, pattern in TOKENS.items():
            regex = re.compile(pattern)
            match = regex.match(input_code, i)
            if match:
                value = match.group(0)
                if token_type != "WS":  # ignore whitespace
                    tokens.append((token_type, value))
                i = match.end()
                match_found = True
                break
        if not match_found:
            raise ValueError(f"Unexpected character at position {i}: '{input_code[i]}'")
    return tokens

# -----------------------------
# Example usage
# -----------------------------
code = "if x <= 10 then y = 20 else y <> z"

tokens = lexer(code)

print("Input code:", code)
print("Recognized tokens:")
for ttype, val in tokens:
    print(f"  {ttype:10} → {val}")
