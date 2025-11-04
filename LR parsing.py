from tabulate import tabulate

# ACTION and GOTO tables for the grammar
ACTION = {
    0: {"id": ("S", 5), "(": ("S", 4)},
    1: {"+": ("S", 6), "$": ("ACC",)},
    2: {"+": ("R", 2), "*": ("S", 7), ")": ("R", 2), "$": ("R", 2)},
    3: {"+": ("R", 4), "*": ("R", 4), ")": ("R", 4), "$": ("R", 4)},
    4: {"id": ("S", 5), "(": ("S", 4)},
    5: {"+": ("R", 6), "*": ("R", 6), ")": ("R", 6), "$": ("R", 6)},
    6: {"id": ("S", 5), "(": ("S", 4)},
    7: {"id": ("S", 5), "(": ("S", 4)},
    8: {"+": ("S", 6), ")": ("S", 11)},
    9: {"+": ("R", 1), "*": ("S", 7), ")": ("R", 1), "$": ("R", 1)},
    10: {"+": ("R", 3), "*": ("R", 3), ")": ("R", 3), "$": ("R", 3)},
    11: {"+": ("R", 5), "*": ("R", 5), ")": ("R", 5), "$": ("R", 5)},
}

GOTO = {
    0: {"E": 1, "T": 2, "F": 3},
    4: {"E": 8, "T": 2, "F": 3},
    6: {"T": 9, "F": 3},
    7: {"F": 10},
}

# Grammar productions
productions = {
    1: ("E", ["E", "+", "T"]),
    2: ("E", ["T"]),
    3: ("T", ["T", "*", "F"]),
    4: ("T", ["F"]),
    5: ("F", ["(", "E", ")"]),
    6: ("F", ["id"]),
}

def show_grammar():
    rows = []
    for num, (lhs, rhs) in productions.items():
        rows.append([num, f"{lhs} → {' '.join(rhs)}"])
    print("\nGrammar Productions:")
    print(tabulate(rows, headers=["No.", "Production"], tablefmt="fancy_grid"))

def lr_parse(tokens):
    tokens.append("$")
    stack = [0]  # state stack
    index = 0
    step = 1
    rows = []

    while True:
        state = stack[-1]
        current_token = tokens[index]

        action = ACTION.get(state, {}).get(current_token, None)

        if not action:
            rows.append([step, stack[:], tokens[index:], f"Error ❌ at {current_token}"])
            break

        if action[0] == "S":  # Shift
            stack.append(current_token)
            stack.append(action[1])  # push state
            rows.append([step, stack[:], tokens[index:], f"Shift {current_token}, goto {action[1]}"])
            index += 1

        elif action[0] == "R":  # Reduce
            prod_num = action[1]
            lhs, rhs = productions[prod_num]
            pop_len = 2 * len(rhs)  # each symbol + state
            if pop_len > 0:
                stack = stack[:-pop_len]
            state = stack[-1]
            stack.append(lhs)
            new_state = GOTO[state][lhs]
            stack.append(new_state)
            rows.append([step, stack[:], tokens[index:], f"Reduce by {lhs} → {' '.join(rhs)}"])

        elif action[0] == "ACC":  # Accept
            rows.append([step, stack[:], tokens[index:], "Accept ✅"])
            break

        step += 1

    print(tabulate(rows, headers=["Step", "Stack", "Input", "Action"], tablefmt="fancy_grid"))


# --------------------
# Example Runs
# --------------------
tokens1 = ["id", "+", "id", "*", "id"]   # valid
tokens2 = ["(", "id", "+", "id", ")", "*", "id"]  # valid
tokens3 = ["id", "*", "+", "id"]  # invalid

print("\n--- Grammar ---")
show_grammar()

print("\n--- Parsing tokens1 ---")
lr_parse(tokens1.copy())

print("\n--- Parsing tokens2 ---")
lr_parse(tokens2.copy())

print("\n--- Parsing tokens3 ---")
lr_parse(tokens3.copy())
