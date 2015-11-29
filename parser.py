import ply.yacc as yacc
from lexer import tokens

num_errors = 0
num_lines = 0

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
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
       p[0] = ('BLOCKLIST', p[1], p[2])

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
        p[0] = ('ASSIGN', p[1], p[3])
    elif len(p) == 6:
        p[0] = ('WHILE', p[2], p[4])
    elif len(p) == 7:
        p[0] = ('IF', p[2], p[4], p[5])
    else:
        p[0] = p[1]

def p_elsestnt(p):
    '''elsestnt : empty
                | ELSE block'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('ELSE', p[2])

def p_exp(p):
    '''exp : NUMBER
           | ID
           | functioncall
           | exp binop exp
           | unaryop exp
           | LPAREN exp RPAREN'''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = ('BINARY OPERATION', p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ('UNARY OPERATION', p[1], p[2])
    else:
        p[0] = p[1]

def p_functioncall(p):
    '''functioncall : ID LPAREN explist RPAREN'''
    p[0] = ('FUNCTION CALL', p[1], p[3])

def p_vardeclaration(p):
    '''vardeclaration : VAR ID expassign'''
    p[0] = ('VAR', p[2], p[3])

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
       p[0] = ('EXP LIST', p[1], p[2])

def p_lexp(p):
    '''lexp : empty
            | lexp exp COMMA'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('EXP SEQ', p[1], p[2])

def p_binop(p):
    '''binop : PLUS
             | MINUS
             | TIMES
             | DIVIDE
             | LESS
             | LESSEQUAL
             | GREATER
             | GREATEREQUAL
             | EQUAL
             | NOTEQUAL
             | AND
             | OR'''
    p[0] = ('BINARY OPERATOR', p[1])

def p_unaryop(p):
    '''unaryop : MINUS %prec UMINUS
               | NOT'''
    p[0] = ('UNARY OPERATOR', p[1])

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
parser = yacc.yacc()
