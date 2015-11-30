import lexer
import parser
from code_generator import CodeGenerator
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

  if lexer.num_errors > 0:
    sys.exit()

  # Preserve lines number
  parser.num_lines = lexer.lexer.lineno - 1

  # Building parser
  result = parser.parser.parse(code, lexer.lexer, tracking = True)
  if parser.num_errors > 0:
    sys.exit()

  # Code Generation
  cg = CodeGenerator(result)
  cg.generate()

  with open("mips.out", "w") as f_out:
    f_out.write(cg.mips_out)
