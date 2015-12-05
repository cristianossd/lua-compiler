import sys

class CodeGenerator:
  def __init__(self, parser_out):
    self.ast = parser_out
    self.mips_out = ""
    self.defining_var = False
    self.var_assigns = []
    self.var_table = {}
    self.defining_else = []
    self.else_count = 0
    self.else_max = 0
    self.while_count = 0
    self.while_max = 0
    self.while_min = 0
    self.if_st = False
    self.while_st = False

  def print_tree(self, tree, level = 1):
    print('-' * (level-1)) + ' ' + str(tree[0])
    for l in tree[1:]:
      if type(l) != tuple:
        print ('-' * level) + ' ' + str(l)
      else:
        self.print_tree(l, level+1)

  # MIPS instructions
  def mips_uminus_term():
    self.mips_top_stack_on_a0(self)
    self.mips_out += "lw $t1, $a0\n"
    self.mips_out += "sub $a0, $a0, $a0\n"
    self.mips_out += "sub $a0, $a0, $t1\n"
    self.mips_push_a0_on_stack()

  def mips_print_out_a0(self):
    self.mips_out += "li $v0, 1\n"
    self.mips_out += "syscall\n"

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
    self.mips_out += "lw $t1, 4($sp)\n"
    self.mips_out += "addiu $sp, $sp, 4\n"
    self.mips_out += "lw $t2, 4($sp)\n"
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

  def mips_var_in_a0(self, var):
    self.mips_out += "lw $a0, " + var + "\n"

  def mips_unary_op(self):
    self.mips_out += "sub $a0, $t1, $t1\n"
    self.mips_out += "sub $a0, $a0, $t1\n"
    self.mips_push_a0_on_stack()

  def mips_exit(self):
    self.mips_out += "li $v0, 10\n"
    self.mips_out += "syscall\n"

  # end MIPS instructions

  def line_break(self):
    self.mips_out += "\n"

  # Accessing var table
  def get_var(self, var):
    v = self.var_table.get(var)
    if v == None:
      print "Semantic error: Trying to use undeclared variable '%s'" % var
      sys.exit()
    return True

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
      self.mips_get_two_tmp()
      self.mips_out += "bne $t1, $t2, else"+str(self.else_count)+"\n"
      return
    elif op == '~=':
      self.mips_get_two_tmp()
      self.mips_out += "beq $t1, $t2, else"+str(self.else_count)+"\n"
      return
    #If True
    elif op == '<=' and self.if_st is True and self.while_st is False:
      self.mips_get_two_tmp()
      self.mips_out += "bgt $t2, $t1, else"+str(self.else_count)+"\n"
      return
    elif op == '>=' and self.if_st is True and self.while_st is False:
      self.mips_get_two_tmp()
      self.mips_out += "blt $t2, $t1, else"+str(self.else_count)+"\n"
      return
    elif op == '<' and self.if_st is True and self.while_st is False:
      self.mips_get_two_tmp()
      self.mips_out += "bge $t2, $t1, else"+str(self.else_count)+"\n"
      return
    elif op == '>' and self.if_st is True and self.while_st is False:
      self.mips_get_two_tmp()
      self.mips_out += "ble $t2, $t1, else"+str(self.else_count)+"\n"
      return
    #While True
    elif op == '<=' and self.if_st is False and self.while_st is True:
      self.mips_get_two_tmp()
      self.mips_out += "blt $t1, $t2, endwhile"+str(self.while_count)+"\n"
      self.enter_nested_while()
      return
    elif op == '>=' and self.if_st is False and self.while_st is True:
      self.mips_get_two_tmp()
      self.mips_out += "bgt $t1, $t2, endwhile"+str(self.while_count)+"\n"
      self.enter_nested_while()
      return
    elif op == '<' and self.if_st is False and self.while_st is True:
      self.mips_get_two_tmp()
      self.mips_out += "ble $t1, $t2, endwhile"+str(self.while_count)+"\n"
      self.enter_nested_while()
      return
    elif op == '>' and self.if_st is False and self.while_st is True:
      self.mips_get_two_tmp()
      self.mips_out += "bge $t1, $t2, endwhile"+str(self.while_count)+"\n"
      self.enter_nested_while()
      return
    elif op == 'or':
      self.mips_get_two_tmp()
      self.mips_out += "or $a0, $t1, $t2\n"
      self.mips_out += "li $t1, 0\n"
      self.mips_out += "beq $a0, $t1, else"+str(self.else_count)+"\n"
      return
    elif op == 'and':
      self.mips_get_two_tmp()
      self.mips_out += "and $a0, $t1, $t2\n"
      self.mips_out += "li $t1, 0\n"
      self.mips_out += "beq $a0, $t1, else"+str(self.else_count)+"\n"
      return

  # Making unary operation
  def make_unary_operation(self, op):
    if op == '-':
      self.mips_top_stack_on_t1()
      self.mips_unary_op()
    elif op == 'not':
      self.mips_top_stack_on_t1()
      self.mips_out += "not $a0, $t1\n"
      self.mips_push_a0_on_stack()
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
      if type(node[1]) is int:
        value = node[1]
        self.mips_assign_a0(str(value))
        self.mips_push_a0_on_stack()
        self.line_break()
      else:
        if self.get_var(node[1]):
          var = node[1]
          self.mips_var_in_a0(str(var))
          self.mips_push_a0_on_stack()
          self.line_break()

    if type(node[3]) is tuple:
      if node[3][0] == 'binary-operation':
        self.binary_operation_statement(node[3])
      elif node[3][0] == 'unary-operation':
        self.unary_operation_statement(node[3])
      else:
        self.function_call_statement(node[3])
    else:
      if type(node[3]) is int:
        value = node[3]
        self.mips_assign_a0(str(value))
        self.mips_push_a0_on_stack()
        self.line_break()
      else:
        if self.get_var(node[3]):
          var = node[3]
          self.mips_var_in_a0(str(var))
          self.mips_push_a0_on_stack()
          self.line_break()

    op = node[2][1]
    self.make_bin_operation(op)
    self.line_break()
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
      if type(node[2]) is int:
        term = node[2]
        self.line_break()
        self.mips_assign_a0(str(term))
        self.mips_push_a0_on_stack()
        self.line_break()
      else:
        if self.get_var(node[2]):
          var = node[2]
          self.line_break()
          self.mips_var_in_a0(str(var))
          self.mips_push_a0_on_stack()
          self.line_break()

    self.make_unary_operation(op)
    self.line_break()
    return

  # Assign
  def assign_statement(self, node):
    index = node[1]

    if type(node[2]) is tuple:
      if node[2][0] == 'binary-operation':
        self.binary_operation_statement(node[2]) # must push the recursive return
        self.mips_top_stack_on_a0()
        value = 'unassigned'
      elif node[2][0] == 'unary-operation':
        self.unary_operation_statement(node[2]) # must push the recursive return
        self.mips_top_stack_on_a0()
        value = 'unassigned'
      else:
        self.function_call_statement(node[2])
    else:
      if type(node[2]) is int:
        value = node[2]
        self.mips_assign_a0(str(value))
        self.mips_push_a0_on_stack()
        self.line_break()
      else:
        if self.get_var(node[2]):
          var = node[2]
          value = self.var_table.get(var)
          self.mips_var_in_a0(str(var))
          self.mips_push_a0_on_stack()
          self.line_break()
    
    #print node
    self.var_table[index] = value
    self.mips_store_var(str(index))
    self.line_break()
      
    return

  # While
  def while_statement(self, node):
    self.mips_out += "while"+str(self.while_count)+":\n"
    self.line_break()
    if type(node[1]) is tuple:
      self.if_st = False
      self.while_st = True
      self.binary_operation_statement(node[1])
    return

  # EndWhile
  def endwhile_statement(self):
    self.leave_nested_while()
    self.mips_out += "j while"+str(self.while_count)+"\n\n"
    self.mips_out += "endwhile"+str(self.while_count)+":\n"
    self.line_break()
    self.check_min_while()
    return

  def enter_nested_while(self):
    self.while_count += 1
    if self.while_count > self.while_max:
      self.while_max = self.while_count
    return

  def leave_nested_while(self):
    self.while_count -= 1
    return

  def check_min_while(self):
    if self.while_min == self.while_count:
      self.while_count = self.while_max
      self.while_min = self.while_max
    return
  
  # If
  def if_statement(self, node):
    if type(node[1]) is tuple:
      self.defining_else.append(False)
      self.if_st = True
      self.while_st = False
      self.else_count += 1
      if self.else_count > self.else_max:
        self.else_max = self.else_count
      self.binary_operation_statement(node[1])
    return

  # Else
  def else_statement(self, node):
    self.defining_else[len(self.defining_else)-1] = True
    self.mips_out += "j else_end"+str(self.else_count)+"\n"
    self.line_break()
    self.mips_out += "else"+str(self.else_count)+":\n"
    self.line_break()
    return

  # EndIf
  def endif_statement(self):
    if self.defining_else[len(self.defining_else)-1] is True:
      self.mips_out += "else_end"+str(self.else_count)+":\n"
      self.line_break()
    else:
      self.mips_out += "else"+str(self.else_count)+":\n"
      self.line_break()
    self.defining_else.pop()
    self.else_count -= 1
    self.check_else_count()
    return
  
  def check_else_count(self):
    if self.defining_else == []:
      self.else_count = self.else_max
    return

  # Function call
  def function_call_statement(self, node):
    if node[1] == 'print':
      op_node = node[2][2]
      if type(op_node) is tuple:
        if op_node[0] == 'binary-operation':
          self.binary_operation_statement(op_node)
        elif op_node[0] == 'unary-operation':
          self.unary_operation_statement(op_node)
      else:
        if type(node[2][2]) is int:
          term = node[2][2]
          self.mips_assign_a0(str(term))
        else:
          if self.get_var(node[2][2]):
            var = node[2][2]
            self.mips_var_in_a0(str(var))

      self.mips_print_out_a0()
      self.line_break()
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
      self.line_break()

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
    if self.defining_var:
      self.var_declaration_exception()
    self.mips_exit()

  def depth_search(self, ast):
    if ast[0] == 'vardeclaration':
      self.var_declaration_statement(ast)
    elif ast[0] == 'assign':
      self.var_declaration_exception()
      self.assign_statement(ast)
    elif ast[0] == 'while':
      self.var_declaration_exception()
      self.while_statement(ast)
    elif ast[0] == 'if':
      self.var_declaration_exception()
      self.if_statement(ast)
    elif ast[0] == 'else':
      self.var_declaration_exception()
      self.else_statement(ast)
    elif ast[0] == 'function-call':
      self.var_declaration_exception()
      self.function_call_statement(ast)
    
    for node in ast[1:]:
      if type(node) == tuple:
        self.depth_search(node)
      elif node == 'endif':
        self.endif_statement()
      elif node == 'endwhile':
        self.endwhile_statement()

