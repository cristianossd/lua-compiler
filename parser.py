import ply.yacc as yacc
from lexer import tokens

num_errors = 0
num_lines = 0

precedence = (
  ('nonassoc', 'AND', 'OR'),
  ('nonassoc', 'EQUAL', 'NOTEQUAL'),
  ('nonassoc', 'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'UMINUS', 'NOT')
)

def p_block(p):
    '''block : blocklist'''
    p[0] = p[1]

def p_blocklist(p):
    '''blocklist : empty
                 | blocklist command blockterminator'''
    if len(p) == 2:
       p[0] = p[1]
    else:
       p[0] = ('blocklist', p[1], p[2])

def p_blockterminator(p):
    '''blockterminator : empty
                       | SEMICOLON'''
    pass

def p_command(p):
    '''command : ID ASSIGN exp
               | functioncall
               | vardeclaration
               | WHILE exp DO block END
               | IF exp THEN block elsestnt END'''
    if len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    elif len(p) == 6:
        p[0] = ('while', p[2], p[4], 'endwhile')
    elif len(p) == 7:
        p[0] = ('if', p[2], p[4], p[5], 'endif')
    else:
        p[0] = p[1]

def p_elsestnt(p):
    '''elsestnt : empty
                | ELSE block'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('else', p[2])

def p_exp(p):
    '''exp : NUMBER
           | ID
           | functioncall
           | exp PLUS exp
           | exp MINUS exp
           | exp TIMES exp
           | exp DIVIDE exp
           | exp LESS exp
           | exp LESSEQUAL exp
           | exp GREATER exp
           | exp GREATEREQUAL exp
           | exp EQUAL exp
           | exp NOTEQUAL exp
           | exp AND exp
           | exp OR exp
           | NOT exp
           | MINUS exp %prec UMINUS
           | LPAREN exp RPAREN'''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        elif p[1] == 'MINUS' or p[1] == 'NOT':
            p[0] = ('unary-operation', p[1], p[2])
        else:
            p[0] = ('binary-operation', p[1], ('binary-operator', p[2]), p[3])
    #elif len(p) == 3:
    #    p[0] = ('unary-operation', p[1], p[2])
    elif len(p) == 3:
        p[0] = ('unary-operation', p[1], p[2])
    else:
        p[0] = p[1]

def p_functioncall(p):
    '''functioncall : ID LPAREN explist RPAREN'''
    p[0] = ('function-call', p[1], p[3])

def p_vardeclaration(p):
    '''vardeclaration : VAR ID expassign'''
    p[0] = ('vardeclaration', p[2], p[3])

def p_expassign(p):
    '''expassign : empty
                 | ASSIGN exp'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_explist(p):
    '''explist : empty
               | lexp exp'''
    if len(p) == 2:
       p[0] = p[1]
    else:
       p[0] = ('exp-list', p[1], p[2])

def p_lexp(p):
    '''lexp : empty
            | lexp exp COMMA'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('exp-seq', p[1], p[2])

#def p_unaryop(p):
#    '''unaryop : MINUS %prec UMINUS
#               | NOT'''
#    p[0] = ('unary-operator', p[1])

def p_empty(p):
    'empty : '
    pass

def p_error(p):
    global num_errors
    global num_lines

    line = p.lineno - num_lines
    print "Syntax error in input at token '%s' at line: %d" % (p.type, line)
    num_errors += 1

# Building parser
parser = yacc.yacc(debug=True)
