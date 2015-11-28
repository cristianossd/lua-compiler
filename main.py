import lexer
import parser
import sys
from sys import argv

if __name__ == '__main__':
  filename = argv[1]
  f = open(filename)
  code = f.read()

  # Building the lexer
  lexer.lexer.input(code)
  while True:
    tok = lexer.lexer.token()
    if not tok:
      break
    print(tok.type, tok.value, tok.lineno, tok.lexpos)

  if lexer.num_errors > 0:
    print 'has errors'
    sys.exit()
  else:
    print 'no errors'

  print lexer.num_errors

  result = parser.parser.parse(code)
  print result
