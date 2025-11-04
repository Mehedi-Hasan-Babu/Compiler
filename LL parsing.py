from tabulate import tabulate  # pip install tabulate if not installed

# Parsing Table for the grammar
parsing_table = {
    "E": {
        "id": ["T", "E'"],
        "(": ["T", "E'"]
    },
    "E'": {
        "+": ["+", "T", "E'"],
        ")": ["ε"],
        "$": ["ε"]
    },
    "T": {
        "id": ["F", "T'"],
        "(": ["F", "T'"]
    },
    "T'": {
        "+": ["ε"],
        "*": ["*", "F", "T'"],
        ")": ["ε"],
        "$": ["ε"]
    },
    "F": {
        "id": ["id"],
        "(": ["(", "E", ")"]
    }
}

# Grammar rules (numbered for clarity)
grammar = [
    ("E", ["T", "E'"]),
    ("E'", ["+", "T", "E'"]),
    ("E'", ["ε"]),
    ("T", ["F", "T'"]),
    ("T'", ["*", "F", "T'"]),
    ("T'", ["ε"]),
    ("F", ["id"]),
    ("F", ["(", "E", ")"])
]

def show_grammar():
    rows = []
    for i, (lhs, rhs) in enumerate(grammar, start=1):
        rows.append([i, f"{lhs} → {' '.join(rhs)}"])
    print("\nGrammar Productions:")
    print(tabulate(rows, headers=["No.", "Production"], tablefmt="fancy_grid"))

def parse(tokens):
    stack = ["$", "E"]
    tokens.append("$")
    index = 0
    step = 1
    rows = []

    while len(stack) > 0:
        top = stack[-1]
        current_token = tokens[index]

        if top == current_token == "$":
            rows.append([step, list(stack), tokens[index:], "Accept ✅"])
            break

        elif top == current_token:
            stack.pop()
            index += 1
            rows.append([step, list(stack), tokens[index:], f"Match {current_token}"])

        elif top in parsing_table and current_token in parsing_table[top]:
            stack.pop()
            production = parsing_table[top][current_token]
            if production != ["ε"]:
                for symbol in reversed(production):
                    stack.append(symbol)
            rows.append([step, list(stack), tokens[index:], f"{top} → {' '.join(production)}"])

        else:
            rows.append([step, list(stack), tokens[index:], f"Error ❌ at {current_token}"])
            break

        step += 1

    print(tabulate(rows, headers=["Step", "Stack", "Input", "Action"], tablefmt="fancy_grid"))


# --------------------
# Example Runs
# --------------------
print("\n--- Grammar ---")
show_grammar()

tokens1 = ["id", "+", "id", "*", "id"]   # valid
tokens2 = ["(", "id", "+", "id", ")", "*", "id"]  # valid
tokens3 = ["id", "*", "+", "id"]  # invalid

print("\n--- Parsing tokens1 ---")
parse(tokens1.copy())

print("\n--- Parsing tokens2 ---")
parse(tokens2.copy())

print("\n--- Parsing tokens3 ---")
parse(tokens3.copy())
