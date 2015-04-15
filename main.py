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
tokens = [
  'ID', 'NUMBER',
  'CHAR', 'STRING',
  'PLUS', 'MINUS',
  'TIMES', 'DIVIDE',
  'PERCENT', 'CIRCUMFLEX',
  'SHARP', 'EQUAL',
  'NOTEQUAL', 'LESSEQUAL',
  'GREATEREQUAL', 'LESS',
  'GREATER', 'ASSIGN',
  'LPAREN', 'RPAREN',
  'LCURLY', 'RCURLY',
  'LSQUARE', 'RSQUARE'
  'SEMICOLON', 'COLON',
  'COMMA', 'DOT',
  'TWODOTS', 'THREEDOTS'
] + list(reserved.values())

# Regular expressions rules
def t_COMMENT(t):
  r'--.*\n'
  print "matched a comment"
  pass
  # Discarded comment

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

t_ignore = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print "Ilegal character '%s' at line %d" % (t.value[0], t.lexer.lineno)
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
