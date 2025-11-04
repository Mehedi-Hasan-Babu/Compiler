class Token:
    def __init__(self, token_type, attribute=None):
        self.token_type = token_type
        self.attribute = attribute

    def __repr__(self):
        return f"TOKEN(type={self.token_type}, attribute={self.attribute})"


def getRelop(input_string):
    """
    Simulates the DFA for relational operators (relops).
    Recognizes: <, <=, <>, =, >, >=
    """
    state = 0
    i = 0
    retToken = Token("RELOP")

    def nextChar():
        nonlocal i
        if i < len(input_string):
            ch = input_string[i]
            i += 1
            print(f"nextChar() -> '{ch}'")
            return ch
        else:
            return None

    def retract():
        nonlocal i
        i -= 1
        print("retract() called → step back one char")

    def fail():
        raise ValueError(f"fail(): '{input_string}' is not a valid relop")

    while True:
        if state == 0:
            c = nextChar()
            if c == '<':
                state = 1
            elif c == '=':
                state = 5
            elif c == '>':
                state = 6
            else:
                fail()

        elif state == 1:  # saw '<'
            c = nextChar()
            if c == '=':
                retToken.attribute = "LE"
                print("Matched '<=' → LE")
                return retToken
            elif c == '>':
                retToken.attribute = "NE"
                print("Matched '<>' → NE")
                return retToken
            else:
                retract()
                retToken.attribute = "LT"
                print("Matched '<' → LT")
                return retToken

        elif state == 5:  # saw '='
            retToken.attribute = "EQ"
            print("Matched '=' → EQ")
            return retToken

        elif state == 6:  # saw '>'
            c = nextChar()
            if c == '=':
                retToken.attribute = "GE"
                print("Matched '>=' → GE")
                return retToken
            else:
                retract()
                retToken.attribute = "GT"
                print("Matched '>' → GT")
                return retToken
tests = ["<", "<=", "<>", "=", ">", ">="]

for t in tests:
    print(f"\nInput: '{t}'")
    token = getRelop(t)
    print("Output:", token)
