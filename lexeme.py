import re

# Define token categories
keywords = {"float", "return"}
operators = {"<=", ">=", "||", "*", "?", ":", "="}
delimiters = {"(", ")", "{", "}", ";", ","}

# Regex patterns
token_spec = [
    ("NUMBER",   r"-?\d+(\.\d+)?"),        # int or float
    ("ID",       r"[A-Za-z_]\w*"),         # identifiers
    ("OP",       r"<=|>=|\|\||\*|\?|:"),   # operators
    ("DELIM",    r"[(){};,]"),             # delimiters
    ("COMMENT",  r"/\*.*?\*/"),            # comments
    ("SKIP",     r"[ \t\n]+"),             # whitespace
    ("MISMATCH", r"."),                    # any other character
]

token_re = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec), re.DOTALL)

def lexer(code):
    tokens = []
    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "ID":
            if value in keywords:
                tokens.append(("KEYWORD", value))
            else:
                tokens.append(("IDENTIFIER", value))
        elif kind == "NUMBER":
            tokens.append(("NUM", float(value) if "." in value else int(value)))
        elif kind == "OP":
            tokens.append(("OPERATOR", value))
        elif kind == "DELIM":
            tokens.append(("DELIMITER", value))
        elif kind == "COMMENT":
            continue
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected char: {value}")
    return tokens


# Test input (the C++ program)
code = """float limitedSquare(x) float x; {
 /* returns x-squared, but never more than 100 */
 return (x<=-10.0||x>=10.0)?100:x*x;
 }"""
print ("input ----\nfloat limitedSquare(x) float x; {\n        /* returns x-squared, but never more than 100 */\n          return (x<=-10.0||x>=10.0)?100:x*x;")
print ("\noutput:")
tokens = lexer(code)
for t in tokens:
    print(t)
