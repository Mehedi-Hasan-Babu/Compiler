# =============================================
# Compiler-style Type Conversion Simulation
# =============================================

def type_conversion_demo():
    # Symbol table: var_name -> (type, value)
    symbol_table = {}

    # Step 1: Declare a = 2
    a_val = 2
    a_type = 'int'
    symbol_table['a'] = (a_type, a_val)
    print(f"a = {a_val} (type: {a_type})")

    # Step 2: Expression b = a * 3.14
    # Get a's value and type
    operand1_val, operand1_type = symbol_table['a'][1], symbol_table['a'][0]
    operand2_val, operand2_type = 3.14, 'float'

    # Compiler-style implicit type conversion
    if operand1_type == 'int' and operand2_type == 'float':
        print("Promoting 'a' from int to float for multiplication")
        operand1_val = float(operand1_val)
        result_type = 'float'
    elif operand1_type == 'float' and operand2_type == 'int':
        operand2_val = float(operand2_val)
        result_type = 'float'
    else:
        result_type = operand1_type  # same type

    # Compute result
    b_val = operand1_val * operand2_val
    symbol_table['b'] = (result_type, b_val)

    print(f"b = {b_val} (type: {result_type})")

    # Final Symbol Table
    print("\nSymbol Table:")
    for var, (typ, val) in symbol_table.items():
        print(f"{var}: value = {val}, type = {typ}")


if __name__ == "__main__":
    type_conversion_demo()
