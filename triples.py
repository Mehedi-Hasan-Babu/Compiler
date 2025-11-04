import ast

class TACTriplesSequential:
    def __init__(self):
        self.triples = []
        self.tac = []
        self.expr_map = {}  # maps temp/variable to triple index
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def visit(self, node):
        """Visit AST nodes recursively"""
        if isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op = self.get_op(node.op)

            # Convert operands to index references if they are results of previous operations
            left_ref = left if isinstance(left, str) else left  # if index, keep as int
            right_ref = right if isinstance(right, str) else right

            idx = len(self.triples)
            self.triples.append((op, left_ref, right_ref))
            self.tac.append(f"t{idx} = {left_ref} {op} {right_ref}")
            self.expr_map[f"t{idx}"] = idx  # map temp to triple index
            return idx  # return triple index as result

        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            if isinstance(node.op, ast.USub):
                operand_ref = operand if isinstance(operand, str) else operand
                idx = len(self.triples)
                self.triples.append(('neg', operand_ref, '-'))
                self.tac.append(f"t{idx} = -{operand_ref}")
                self.expr_map[f"t{idx}"] = idx
                return idx
            else:
                raise NotImplementedError("Only unary minus supported")

        elif isinstance(node, ast.Name):
            return node.id

        elif isinstance(node, ast.Constant):
            return str(node.value)

        else:
            raise NotImplementedError(f"Unsupported node type: {type(node)}")

    def visit_Assign(self, node):
        """Handle assignment statements"""
        target = node.targets[0].id
        value_idx = self.visit(node.value)
        # Assignment triple: target in Arg1, computed index in Arg2
        idx = len(self.triples)
        self.triples.append(('=', target, value_idx))
        self.tac.append(f"{target} = t{value_idx}" if isinstance(value_idx, int) else f"{target} = {value_idx}")
        return idx

    def get_op(self, op_node):
        ops = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Mod: "%",
            ast.Pow: "**"
        }
        return ops[type(op_node)]

    def generate(self, stmt):
        stmt = stmt.strip()
        if '=' in stmt:
            tree = ast.parse(stmt, mode='exec')
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    self.visit_Assign(node)
        else:
            tree = ast.parse(stmt, mode='eval')
            self.visit(tree.body)


# =========================
# Main Program
# =========================
if __name__ == "__main__":
    stmt = input("Enter an arithmetic statement (with or without assignment): ")
    generator = TACTriplesSequential()
    generator.generate(stmt)

    print("\nThree Address Code (TAC):\n")
    for line in generator.tac:
        print(line)

    print("\nTriples Representation:\n")
    print(f"{'Index':^6} | {'Op':^6} | {'Arg1':^6} | {'Arg2':^6}")
    print("-"*32)
    for i, triple in enumerate(generator.triples):
        op, arg1, arg2 = triple
        print(f"{i:^6} | {op:^6} | {arg1:^6} | {arg2:^6}")
