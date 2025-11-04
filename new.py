"""
Predictive (LL(1)) parser and Bottom-up (shift-reduce) parser demo.

- Builds a predictive parsing table for grammar G:
	E  -> T E'
	E' -> + T E' | epsilon
	T  -> F T'
	T' -> * F T' | epsilon
	F  -> ( E ) | id

- Uses the table to do a top-down parse for the input:  id + id * id
- Implements a simple bottom-up shift-reduce parser (using the equivalent
  left-recursive grammar) and parses: id + id

Run as a script to see the parse trees printed.
"""

from collections import defaultdict, deque
import sys


class Node:
	def __init__(self, symbol, children=None):
		self.symbol = symbol
		self.children = children or []

	def pretty(self, level=0):
		out = "  " * level + str(self.symbol) + "\n"
		for c in self.children:
			out += c.pretty(level + 1)
		return out


def tokenize(s):
	# Accepts inputs like: "id + id * id" or "( id + id )"
	toks = []
	for part in s.replace('(', ' ( ').replace(')', ' ) ').split():
		if part == 'id' or part in ['+', '*', '(', ')']:
			toks.append(part)
		else:
			raise ValueError(f"Unknown token: {part}")
	toks.append('$')
	return toks


# Grammar G in the factorized form (for LL(1))
GRAMMAR = {
	'E': [['T', "E'"]],
	"E'": [['+', 'T', "E'"], ['epsilon']],
	'T': [['F', "T'"]],
	"T'": [['*', 'F', "T'"], ['epsilon']],
	'F': [['(', 'E', ')'], ['id']]
}


def compute_first(grammar):
	first = defaultdict(set)
	changed = True
	while changed:
		changed = False
		for A, prods in grammar.items():
			for prod in prods:
				if prod[0] == 'epsilon':
					if 'epsilon' not in first[A]:
						first[A].add('epsilon'); changed = True
					continue
				i = 0
				while i < len(prod):
					X = prod[i]
					if X.islower() or X in ['+', '*', '(', ')', 'id'] and X != 'epsilon':
						# terminal
						if X not in first[A]:
							first[A].add(X); changed = True
						break
					else:
						# non-terminal
						before = len(first[A])
						# add FIRST(X) - {epsilon}
						for sym in first[X]:
							if sym != 'epsilon' and sym not in first[A]:
								first[A].add(sym)
						after = len(first[A])
						if 'epsilon' in first[X]:
							i += 1
							if i == len(prod):
								if 'epsilon' not in first[A]:
									first[A].add('epsilon'); changed = True
						else:
							# stop
							pass
						if after != before:
							changed = True
						break
	return first


def compute_follow(grammar, first, start='E'):
	follow = defaultdict(set)
	follow[start].add('$')
	changed = True
	while changed:
		changed = False
		for A, prods in grammar.items():
			for prod in prods:
				for i, B in enumerate(prod):
					if B in grammar:  # non-terminal
						beta = prod[i+1:]
						if not beta:
							# add FOLLOW(A)
							before = len(follow[B])
							follow[B] |= follow[A]
							if len(follow[B]) != before:
								changed = True
						else:
							# add FIRST(beta) - epsilon
							first_beta = set()
							j = 0
							while j < len(beta):
								Y = beta[j]
								if Y in grammar:
									first_beta |= (first[Y] - {'epsilon'})
									if 'epsilon' in first[Y]:
										j += 1
										if j == len(beta):
											# add follow(A) as well
											before = len(follow[B])
											follow[B] |= follow[A]
											if len(follow[B]) != before:
												changed = True
									else:
										break
								else:
									# terminal
									first_beta.add(Y)
									break
							before = len(follow[B])
							follow[B] |= first_beta
							if len(follow[B]) != before:
								changed = True
	return follow


def build_parsing_table(grammar, first, follow):
	table = defaultdict(dict)  # table[A][a] = production (list)
	for A, prods in grammar.items():
		for prod in prods:
			if prod[0] == 'epsilon':
				for b in follow[A]:
					table[A][b] = prod
			else:
				# compute FIRST(prod)
				first_prod = set()
				i = 0
				while i < len(prod):
					X = prod[i]
					if X in grammar:
						first_prod |= (first[X] - {'epsilon'})
						if 'epsilon' in first[X]:
							i += 1
							if i == len(prod):
								first_prod.add('epsilon')
						else:
							break
					else:
						first_prod.add(X)
						break
				for a in (first_prod - {'epsilon'}):
					table[A][a] = prod
				if 'epsilon' in first_prod:
					for b in follow[A]:
						table[A][b] = prod
	return table


def predictive_parse(tokens, table, start='E'):
	# tokens: list ending with '$'
	stack = ['$', start]
	node_stack = [Node('$'), Node(start)]
	i = 0
	token = tokens[i]
	while stack:
		top = stack.pop()
		node = node_stack.pop()
		if top == 'epsilon':
			# epsilon production creates no children
			continue
		if top in ['+', '*', '(', ')', 'id', '$']:
			# terminal
			if top == token:
				# match
				node.children = []  # terminal leaf
				i += 1
				token = tokens[i]
				continue
			else:
				raise SyntaxError(f"Unexpected token: {token}, expected: {top}")
		else:
			# non-terminal
			prod = table.get(top, {}).get(token)
			if prod is None:
				raise SyntaxError(f"No rule for non-terminal {top} with lookahead {token}")
			# create child nodes for prod
			children = []
			# push RHS in reverse onto stack
			for sym in reversed(prod):
				children.append(Node(sym))
				stack.append(sym)
			# reverse children to natural order
			children = list(reversed(children))
			node.children = children
			# push corresponding nodes
			for child in children[::-1]:
				node_stack.append(child)
	# finished, node_stack empty, root built: return node representing start (we kept it earlier)
	# Reconstruct root by parsing the produced tree from a fresh root
	# For simplicity we return the first Node created as start
	return Node(start, [])  # unused in current flow; better to construct differently


def predictive_parse_build_tree(tokens, table, start='E'):
	# A more direct version returning the built root node
	stack = [start]
	root = Node(start)
	node_stack = [root]
	i = 0
	token = tokens[i]
	while stack:
		top = stack.pop()
		node = node_stack.pop()
		if top == 'epsilon':
			continue
		if top in ['+', '*', '(', ')', 'id', '$']:
			if top == token:
				node.children = []
				i += 1
				token = tokens[i]
				continue
			else:
				raise SyntaxError(f"Unexpected token: {token}, expected: {top}")
		else:
			prod = table.get(top, {}).get(token)
			if prod is None:
				raise SyntaxError(f"No rule for non-terminal {top} with lookahead {token}")
			children = [Node(sym) for sym in prod if sym != 'epsilon']
			node.children = children
			# push children in reverse
			for child, sym in zip(reversed(children), reversed([s for s in prod if s != 'epsilon'])):
				stack.append(sym)
				node_stack.append(child)
	return root


# Bottom-up shift-reduce parser using left-recursive productions
LR_GRAMMAR = [
	('E', ['E', '+', 'T']),
	('E', ['T']),
	('T', ['T', '*', 'F']),
	('T', ['F']),
	('F', ['(', 'E', ')']),
	('F', ['id'])
]


def bottom_up_shift_reduce(tokens):
	# tokens end with '$'
	stack = []  # will hold symbols
	node_stack = []
	i = 0
	token = tokens[i]
	while True:
		if token != '$':
			# shift
			stack.append(token)
			node_stack.append(Node(token))
			i += 1
			token = tokens[i]
		# Try reductions until none apply
		reduced = True
		while reduced:
			reduced = False
			for lhs, rhs in LR_GRAMMAR:
				if len(rhs) <= len(stack) and stack[-len(rhs):] == rhs:
					# perform reduction
					children = node_stack[-len(rhs):]
					# pop
					del stack[-len(rhs):]
					del node_stack[-len(rhs):]
					stack.append(lhs)
					node_stack.append(Node(lhs, children))
					reduced = True
					break
		if token == '$':
			# accept when stack is ['E'] and single node
			if stack == ['E']:
				return node_stack[0]
			else:
				raise SyntaxError(f"Unable to reduce to start symbol, stack={stack}")


def main():
	# compute FIRST and FOLLOW and build parsing table
	first = compute_first(GRAMMAR)
	follow = compute_follow(GRAMMAR, first)
	table = build_parsing_table(GRAMMAR, first, follow)

	print('FIRST sets:')
	for k in sorted(first):
		print(f'  {k}:', first[k])
	print('\nFOLLOW sets:')
	for k in sorted(follow):
		print(f'  {k}:', follow[k])

	print('\nPredictive Parsing Table (partial view):')
	for A in sorted(table):
		for a in sorted(table[A]):
			print(f'  M[{A}, {a}] = {table[A][a]}')

	# Top-down parse tree for: id + id * id
	s1 = 'id + id * id'
	toks1 = tokenize(s1)
	print('\nTop-down (LL(1)) parse for:', s1)
	root = predictive_parse_build_tree(toks1, table, start='E')
	# Pretty print the tree (we used symbol-only nodes)
	print(root.pretty())

	# Bottom-up parse for: id + id
	s2 = 'id + id'
	toks2 = tokenize(s2)
	print('Bottom-up (shift-reduce) parse for:', s2)
	bu_root = bottom_up_shift_reduce(toks2)
	print(bu_root.pretty())


if __name__ == '__main__':
	main()

