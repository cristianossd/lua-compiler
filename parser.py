import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

def p_block(p):
    '''block : blocklist'''
    pass

def p_blocklist(p):
    '''blocklist : empty
                 | blocklist command blockterminator'''
    pass

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
    pass

def p_elsestnt(p):
    '''elsestnt : empty
                | ELSE block'''
    pass

def p_exp(p):
    '''exp : NUMBER
           | ID
           | functioncall
           | exp binop exp
           | unaryop exp
           | LPAREN exp RPAREN'''
    pass

def p_functioncall(p):
    '''functioncall : ID LPAREN explist RPAREN'''
    pass

def p_vardeclaration(p):
    '''vardeclaration : VAR ID expassign'''
    pass

def p_expassign(p):
    '''expassign : empty
                 | ASSIGN exp'''
    pass

def p_explist(p):
    '''explist : empty
               | lexp exp'''

def p_lexp(p):
    '''lexp : empty
            | lexp exp COMMA'''
    pass

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
    pass

def p_unaryop(p):
    '''unaryop : MINUS %prec UMINUS
               | NOT'''
    pass

def p_empty(p):
    'empty : '
    pass

def p_error(p):
    print("Syntax error in input")

# Building parser
parser = yacc.yacc()
