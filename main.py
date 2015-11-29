import lexer
import parser
import sys
from sys import argv

def print_as_tree(lst, level = 1):
  print('--' * (level-1)) + ' ' + str(lst[0])
  for l in lst[1:]:
    if type(l) != tuple:
      print ('--' * level) + ' ' + str(l)
    else:
      print_as_tree(l, level+1)


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

  if lexer.num_errors > 0:
    print 'has errors'
    sys.exit()
  else:
    print 'no errors'

  # Preserve lines number
  parser.num_lines = lexer.lexer.lineno - 1

  result = parser.parser.parse(code, lexer.lexer, tracking = True)
  print result
  print_as_tree(result)
