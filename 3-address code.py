# ============================================
# Three Address Code Generator
# Expression: a + a*(b-c) + (b-c)*d
# ============================================

def generate_TAC(expr):
    temp_count = 1
    tac = []

    # Step 1: Compute (b - c)
    t1 = f"t{temp_count}"
    tac.append(f"{t1} = b - c")
    temp_count += 1

    # Step 2: Compute a * (b - c)
    t2 = f"t{temp_count}"
    tac.append(f"{t2} = a * {t1}")
    temp_count += 1

    # Step 3: Compute (b - c) * d
    t3 = f"t{temp_count}"
    tac.append(f"{t3} = {t1} * d")
    temp_count += 1

    # Step 4: Compute a + a*(b - c)
    t4 = f"t{temp_count}"
    tac.append(f"{t4} = a + {t2}")
    temp_count += 1

    # Step 5: Compute final result: (a + a*(b - c)) + (b - c)*d
    t5 = f"t{temp_count}"
    tac.append(f"{t5} = {t4} + {t3}")

    return tac


# =========================
# Main Program
# =========================
if __name__ == "__main__":
    expression = "a + a*(b-c) + (b-c)*d"
    print(f"Expression: {expression}\n")
    tac_list = generate_TAC(expression)

    print("Three Address Code:\n")
    for line in tac_list:
        print(line)
