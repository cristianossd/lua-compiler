import lexer
import parser
from sys import argv

if __name__ == '__main__':
  filename = argv[1]
  f = open(filename)
  code = f.read()

  # Building the lexer
  lex = lexer.Lexer()
  lex.build()
  lex.lexer.input(code)

  # Building the parser
  parser = parser.Parser()
  parser.build()
  parser.parse(lex.lexer)
