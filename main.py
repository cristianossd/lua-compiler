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
  'ID'        , 'NUMBER'      , 'STRING',
  'PLUS'      , 'MINUS'       , 'TIMES',
  'DIVIDE'    , 'PERCENT'     , 'CIRCUMFLEX',
  'SHARP'     , 'EQUAL'       , 'NOTEQUAL',
  'LESSEQUAL' , 'GREATEREQUAL', 'LESS',
  'GREATER'   , 'ASSIGN'      , 'LPAREN',
  'RPAREN'    , 'LCURLY'      , 'RCURLY',
  'LSQUARE'   , 'RSQUARE'     , 'SEMICOLON',
  'COLON'     , 'COMMA'       , 'DOT',
  'TWODOTS'   , 'THREEDOTS'
] + list(reserved.values())

t_STRING        = r'(\'(.|\s|\\(a|b|f|n|r|t|v|\\|\"|\'))+\')|(\"(.|\s|\\(a|b|f|n|r|t|v|\\|\"|\'))+\")'
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_PERCENT       = r'%'
t_CIRCUMFLEX    = r'\^'
t_SHARP         = r'\#'
t_EQUAL         = r'=='
t_NOTEQUAL      = r'~='
t_LESSEQUAL     = r'<='
t_GREATEREQUAL  = r'>='
t_LESS          = r'<'
t_GREATER       = r'>'
t_ASSIGN        = r'='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LCURLY        = r'\{'
t_RCURLY        = r'}'
t_LSQUARE       = r'\['
t_RSQUARE       = r'\]'
t_SEMICOLON     = r';'
t_COLON         = r':'
t_COMMA         = r','
t_DOT           = r'\.'
t_TWODOTS       = r'\.\.'
t_THREEDOTS     = r'\.\.\.'

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

def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value)
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
