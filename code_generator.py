class CodeGenerator:
  def __init__(self, parser_out):
    self.ast = parser_out
    self.mips_out = ""
    self.defining_var = False
    self.var_assigns = []
    self.var_table = {}

  def print_tree(self, tree, level = 1):
    print('-' * (level-1)) + ' ' + str(tree[0])
    for l in tree[1:]:
      if type(l) != tuple:
        print ('-' * level) + ' ' + str(l)
      else:
        self.print_tree(l, level+1)

  # AST blocks

  def var_declaration_statement(self, node):
    if self.defining_var:
      print str(node[1]) + ': .word 0' # remove
      self.mips_out += str(node[1]) + ": .word 0\n"
    else:
      print "Semantic error: '%s' variable can not be declared at main" % node[1]

    if node[2] is not None:
      self.var_assigns.append([node[1], node[2]])

  def binary_operation_statement(self, node):
    if self.defining_var is True:
      return
    return 'binary-operation'

  def assign_statement(self, node):
    return

  def while_statement(self, node):
    return

  def if_statement(self, node):
    return

  def function_call_statement(self, node):
    return

  # end AST blocks

  def assign_declared_vars(self):
    for var in self.var_assigns:
      index = var[0]
      value = self.binary_operation_statement(var[1]) if (type(var[1]) is tuple) else var[1]
      self.var_table[index] = value
      print 'li $a0, ' + str(value)
      self.mips_out += "li $a, " + str(value) + "\n"
      print 'sw $a0, ' + str(index)
      self.mips_out += "sw $a, " + str(index) + "\n"

  def var_declaration_exception(self):
    if self.defining_var:
      self.defining_var = False
      print '.text'
      self.mips_out += ".text\n"
      print '.globl main'
      self.mips_out += ".globl main\n\nmain:\n\n"

      if len(self.var_assigns) > 0:
        self.assign_declared_vars()

  def generate(self):
    print '.data' # remove
    self.mips_out += ".data\n"
    self.defining_var = True
    self.depth_search(self.ast)

  def depth_search(self, ast):
    if ast[0] is 'vardeclaration':
      self.var_declaration_statement(ast)
    elif ast[0] is 'assign':
      self.var_declaration_exception()
      self.assign_statement(ast)
    elif ast[0] is 'while':
      self.var_declaration_exception()
      self.while_statement(ast)
    elif ast[0] is 'if':
      self.var_declaration_exception()
      self.if_statement(ast)
    elif ast[0] is 'function-call':
      self.var_declaration_exception()
      self.function_call_statement(ast)

    for node in ast[1:]:
      if type(node) == tuple:
        self.depth_search(node)

