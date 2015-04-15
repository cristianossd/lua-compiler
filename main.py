import ply.lex as lex
from sys import argv

reserved = {
  'and'     : 'AND',
  'break'   : 'BREAK',
  'do'      : 'DO',
  'else'    : 'ELSE',
  'elseif'  : 'ELSEIF',
  'end'     : 'END',
  'false'   : 'FALSE',
  'for'     : 'FOR',
  'function': 'FUNCTION',
  'if'      : 'IF',
  'in'      : 'IN',
  'local'   : 'LOCAL',
  'nil'     : 'NIL',
  'not'     : 'NOT',
  'or'      : 'OR',
  'repeat'  : 'REPEAT',
  'return'  : 'RETURN',
  'then'    : 'THEN',
  'true'    : 'TRUE',
  'until'   : 'UNTIL',
  'while'   : 'WHILE'
}

# List of token names
tokens = ['ID'] + list(reserved.values())

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_error(t):
  t.lexer.skip(1)

filename = argv[1]

f = open(filename)
code = f.read()

lexer = lex.lex()
lexer.input(code)

while True:
  tok = lexer.token()
  if not tok: break
  print tok
