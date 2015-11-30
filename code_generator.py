import sys

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

  # Accessing var table
  def get_var(self, var):
    v = self.var_table.get(var)
    if v == None:
      print "Semantic error: Trying to use undeclared variable '%s'" % var
      sys.exit()

  # Making binary operation
  def make_bin_operation(self, first, op, second):
    if op == '+':
      self.mips_out += "li $a0, " + str(first) + "\n"
      self.mips_out += "sw $a0, 0($sp)\n"
      self.mips_out += "addiu $sp $sp -4\n"
      self.mips_out "li $a0, " + str(second) "\n"
      self.mips_out "lw $t1 4($sp)\n"
      self.mips_out "add $a0 $t1 $a0\n"
      self.mips_out "addiu $sp $sp 4\n"
    elif op == '-':
      self.mips_out += "li $a0, " + str(first) + "\n"
      self.mips_out += "sw $a0, 0($sp)\n"
      self.mips_out += "addiu $sp $sp -4\n"
      self.mips_out "li $a0, " + str(second) "\n"
      self.mips_out "lw $t1 4($sp)\n"
      self.mips_out "sub $a0 $t1 $a0\n"
      self.mips_out "addiu $sp $sp 4\n"
    elif op == '*':
      self.mips_out += "li $a0, " + str(first) + "\n"
      self.mips_out += "sw $a0, 0($sp)\n"
      self.mips_out += "addiu $sp $sp -4\n"
      self.mips_out "li $a0, " + str(second) "\n"
      self.mips_out "lw $t1 4($sp)\n"
      self.mips_out "mul $a0 $t1 $a0\n"
      self.mips_out "addiu $sp $sp 4\n"
    elif op == '/':
      self.mips_out += "li $a0, " + str(first) + "\n"
      self.mips_out += "sw $a0, 0($sp)\n"
      self.mips_out += "addiu $sp $sp -4\n"
      self.mips_out "li $a0, " + str(second) "\n"
      self.mips_out "lw $t1 4($sp)\n"
      self.mips_out "div $a0 $t1 $a0\n"
      self.mips_out "addiu $sp $sp 4\n"
    elif op == '==':
      return first == second
    elif op == '~=':
      return first != second
    elif op == '<=':
      return first <= second
    elif op == '>=':
      return first >= second
    elif op == '<':
      return first < second
    elif op == '>':
      return first > second

  # Making unary operation
  def make_unary_operation(self, term, op):
    if op == '-':
      return -term
    elif op == 'NOT':
      return not term

  # AST blocks
  # Var declaration
  def var_declaration_statement(self, node):
    if self.defining_var:
      self.mips_out += str(node[1]) + ": .word 0\n"
      self.var_table[node[1]] = 0
    else:
      print "Semantic error: '%s' variable can not be declared at main" % node[1]
      sys.exit()

    if node[2] is not None:
      self.var_assigns.append([node[1], node[2]])

  # Binary Operation
  def binary_operation_statement(self, node):
    if self.defining_var is True:
      return

    if node[1] is tuple:
      if node[1][0] == 'binary-operation':
        first = self.binary_operation_statement(node[1])
      elif node[1][0] == 'unary-operation':
        first = self.unary_operation_statement(node[1])
      else:
        first = self.function_call_statement(node[1])
    else:
      first = node[1] if type(node[1]) is int else self.get_var(node[1])

    if node[3] is tuple:
      if node[3][0] == 'binary-operation':
        second = self.binary_operation_statement(node[3])
      elif node[3][0] == 'unary-operation':
        second = self.unary_operation_statement(node[3])
      else:
        second = self.function_call_statement(node[3])
    else:
      second = node[3] if type(node[3]) is int else self.get_var(node[3])

    op = node[2][1]

    return self.make_bin_operation(first, op, second)

  # Unary Operation
  def unary_operation_statement(self, node):
    if self.defining_var is True:
      return

    op = node[1]
    if node[2] is tuple:
      if node[2][0] == 'binary-operation':
        term = self.binary_operation_statement(node[2])
      elif node[2][0] == 'unary-operation':
        term = self.unary_operation_statement(node[2])
      else:
        term = self.function_call_statement(node[2])
    else:
      term = node[2] if type(node[2]) is int else self.get_var(node[2])

    self.make_unary_operation(term, op)
    return

  # Assign
  def assign_statement(self, node):
    return

  # While
  def while_statement(self, node):
    return

  # If
  def if_statement(self, node):
    return

  # Function call
  def function_call_statement(self, node):
    return
  # end AST blocks

  def assign_declared_vars(self):
    for var in self.var_assigns:
      index = var[0]

      if type(var[1]) is tuple:
        if var[1][0] == 'binary-operation':
          self.binary_operation_statement(var[1])
          self.mips_out += "sw $t1, 4($sp)\n"
          self.mips_out += "addiu $sp, $sp 4\n"
          self.mips_out += "sw $a0, $t1\n"
          value = 'unassigned'
        elif var[1][0] == 'unary-operation':
          self.unary_operation_statement(var[1])
          self.mips_out += "sw $t1, 4($sp)\n"
          self.mips_out += "addiu $sp, $sp 4\n"
          self.mips_out += "sw $a0, $t1\n"
          value = 'unassigned'
        else:
          print "Semantic error: can not assign its value for '%s' variable" % var[0]
          sys.exit()
      else:
        value = var[1]
        self.mips_out += "li $a0, " + str(value) + "\n"

      self.var_table[index] = value
      self.mips_out += "sw $a0, " + str(index) + "\n\n"

  def var_declaration_exception(self):
    if self.defining_var:
      self.defining_var = False
      self.mips_out += ".text\n"
      self.mips_out += ".globl main\n\nmain:\n\n"

      if len(self.var_assigns) > 0:
        self.assign_declared_vars()

  def generate(self):
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

