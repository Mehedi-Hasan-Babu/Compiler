import ast

class TACQuadSequential:
    def __init__(self):
        self.temp_count = 0
        self.tac = []
        self.quadruples = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def visit(self, node):
        """Visit AST nodes recursively"""
        if isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op = self.get_op(node.op)
            temp = self.new_temp()
            self.tac.append(f"{temp} = {left} {op} {right}")
            self.quadruples.append((op, left, right, temp))
            return temp

        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            if isinstance(node.op, ast.USub):
                temp = self.new_temp()
                self.tac.append(f"{temp} = -{operand}")
                self.quadruples.append(('minus', operand, '-', temp))
                return temp
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
        value = self.visit(node.value)
        self.tac.append(f"{target} = {value}")
        self.quadruples.append(('=', value, '-', target))
        return target

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
        """Detect assignment or plain expression"""
        stmt = stmt.strip()
        if '=' in stmt:
            # Assignment statement
            tree = ast.parse(stmt, mode='exec')
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    self.visit_Assign(node)
        else:
            # Plain expression
            tree = ast.parse(stmt, mode='eval')
            self.visit(tree.body)


# =========================
# Main Program
# =========================
if __name__ == "__main__":
    stmt = input("Enter an arithmetic statement (with or without assignment): ")
    generator = TACQuadSequential()
    generator.generate(stmt)

    print("\nThree Address Code (TAC):\n")
    for line in generator.tac:
        print(line)

    print("\nQuadruple Representation:\n")
    print(f"{'Op':^6} | {'Arg1':^6} | {'Arg2':^6} | {'Result':^6}")
    print("-"*32)
    for quad in generator.quadruples:
        op, arg1, arg2, res = quad
        print(f"{op:^6} | {arg1:^6} | {arg2:^6} | {res:^6}")
