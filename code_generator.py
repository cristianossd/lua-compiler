class CodeGenerator:
  def __init__(self, parser_out):
    self.ast = parser_out
    self.defining_var = False
    self.var_assigns = []

  def print_tree(self, tree, level = 1):
    print('--' * (level-1)) + ' ' + str(tree[0])
    for l in tree[1:]:
      if type(l) != tuple:
        print ('--' * level) + ' ' + str(l)
      else:
        self.print_tree(l, level+1)

  # AST blocks

  def var_declaration_statement(self, node):
    print str(node[1]) + ': .word 0'

    if node[2] is not None:
      self.var_assigns.append([node[1], node[2]])

  # end AST blocks

  def generate(self):
    print '.data'
    self.defining_variable = True
    self.depth_search(self.ast)
    print "\nvar assign list"
    print self.var_assigns

  def depth_search(self, ast):
    if ast[0] is 'vardeclaration':
      self.var_declaration_statement(ast)

    for node in ast[1:]:
      if type(node) == tuple:
        self.depth_search(node)

