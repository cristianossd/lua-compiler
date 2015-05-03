import lexer
from sys import argv

if __name__ == '__main__':
  filename = argv[1]
  f = open(filename)
  code = f.read()

  lex = lexer.Lexer()
  lex.build()
  lex.test(code)
