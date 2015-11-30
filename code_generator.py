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

  # MIPS instructions
  def mips_uminus_term():
    self.mips_top_stack_on_a0()
    self.mips_out += "lw $t1, $a0\n"
    self.mips_out += "sub $a0, $a0, $a0\n"
    self.mips_out += "sub $a0, $a0, $t1\n"
    self.mips_push_a0_on_stack()

  def mips_top_stack_on_a0(self):
    self.mips_out += "lw $a0, 4($sp)\n"
    self.mips_out += "addiu $sp, $sp 4\n"

  def mips_top_stack_on_t1(self):
    self.mips_out += "lw $t1, 4($sp)\n"
    self.mips_out += "addiu $sp, $sp 4\n"

  def mips_top_stack_on_t2(self):
    self.mips_out += "lw $t2, 4($sp)\n"
    self.mips_out += "addiu $sp, $sp 4\n"

  def mips_get_two_tmp(self):
    self.mips_out += "lw $t1, 0($sp)\n"
    self.mips_out += "addiu $sp, $sp, 4\n"
    self.mips_out += "lw $t2, 0($sp)\n"
    self.mips_out += "addiu $sp, $sp, 4\n"

  def mips_push_a0_on_stack(self):
    self.mips_out += "sw $a0, 0($sp)\n"
    self.mips_out += "addiu $sp, $sp, -4\n"

  def mips_assign_a0(self, value):
    self.mips_out += "li $a0, " + value + "\n"

  def mips_assign_t1(self, value):
    self.mips_out += "li $t1, " + value + "\n"

  def mips_assign_t2(self, value):
    self.mips_out += "li $t2, " + value + "\n"

  def mips_store_var(self, value):
    self.mips_out += "sw $a0, " + value + "\n"

  # Accessing var table
  def get_var(self, var):
    print var
    v = self.var_table.get(var)
    print v
    if v == None:
      print "Semantic error: Trying to use undeclared variable '%s'" % var
      sys.exit()

  # Making binary operation
  def make_bin_operation(self, op):
    if op == '+':
      self.mips_get_two_tmp()
      self.mips_out += "add $a0, $t2, $t1\n"
      self.mips_push_a0_on_stack()
    elif op == '-':
      self.mips_get_two_tmp()
      self.mips_out += "sub $a0, $t2, $t1\n"
      self.mips_push_a0_on_stack()
    elif op == '*':
      self.mips_get_two_tmp()
      self.mips_out += "mul $a0, $t2, $t1\n"
      self.mips_push_a0_on_stack()
    elif op == '/':
      self.mips_get_two_tmp()
      self.mips_out += "div $a0, $t2, $t1\n"
      self.mips_push_a0_on_stack()
    elif op == '==':
      return
    elif op == '~=':
      return
    elif op == '<=':
      return
    elif op == '>=':
      return
    elif op == '<':
      return
    elif op == '>':
      return

  # Making unary operation
  def make_unary_operation(self, op):
    if op == '-':
      self.mips_top_stack_on_t1()
    elif op == 'NOT':
      return

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

    if type(node[1]) is tuple:
      if node[1][0] == 'binary-operation':
        self.binary_operation_statement(node[1])
      elif node[1][0] == 'unary-operation':
        self.unary_operation_statement(node[1])
      else:
        self.function_call_statement(node[1])
    else:
      value = node[1] if type(node[1]) is int else self.get_var(node[1])
      self.mips_assign_a0(str(value))
      self.mips_push_a0_on_stack()

    if type(node[3]) is tuple:
      if node[3][0] == 'binary-operation':
        self.binary_operation_statement(node[3])
      elif node[3][0] == 'unary-operation':
        self.unary_operation_statement(node[3])
      else:
        self.function_call_statement(node[3])
    else:
      value = node[3] if type(node[3]) is int else self.get_var(node[3])
      self.mips_assign_a0(str(value))
      self.mips_push_a0_on_stack()

    op = node[2][1]
    self.make_bin_operation(op)
    return

  # Unary Operation
  def unary_operation_statement(self, node):
    if self.defining_var is True:
      return

    op = node[1]
    if type(node[2]) is tuple:
      if node[2][0] == 'binary-operation':
        self.binary_operation_statement(node[2])
      elif node[2][0] == 'unary-operation':
        self.unary_operation_statement(node[2])
      else:
        self.function_call_statement(node[2])
    else:
      term = node[2] if type(node[2]) is int else self.get_var(node[2])
      self.mips_assign_a0(str(term))
      self.mips_push_a0_on_stack()

    self.make_unary_operation(op)
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
          self.binary_operation_statement(var[1]) # must push the recursive return
          self.mips_top_stack_on_a0()
          value = 'unassigned'
        elif var[1][0] == 'unary-operation':
          self.unary_operation_statement(var[1]) # must push the recursive return
          self.mips_top_stack_on_a0()
          value = 'unassigned'
        else:
          print "Semantic error: can not assign its value for '%s' variable" % var[0]
          sys.exit()
      else:
        value = var[1]
        self.mips_assign_a0(str(value))

      self.var_table[index] = value
      self.mips_store_var(str(index))

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

