# Simplified Lua Compiler

We build a compiler for a simplified language based on [Lua](http://www.lua.org/). On the front end stages, we used a pure-Python implementation of the popular tools **lex** and **yacc**, the [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/ply.html).

### Usage

First, you must run the front end stages (lexical and syntatic), semantic and code generation with just one line described below. The `input_file` is your source code.

```
$ python main.py input_file output_file
```

After that, you'll execute your `output_file` using SPIM simulator (see details [here](https://www.dropbox.com/s/ugc5oz8c5gpb9ro/SPIM_Manual.pdf)). Download the SPIM simulator in this [link](http://spimsimulator.sourceforge.net/).

### About the language

Our language supports procedural programming. An identifier can be composed of letters, digits and underscore only. The first letter of identifier should be a letter.

The keywords below represented can't be used as identifier.
```
  and   do    else    while   then
  end   for   if      var     or
```

More lexical items allowed:
```
  +   -   *   /   <=    >=    <   >
  (   )   ;   ,   ==    ~=    =
```

The **syntax** is described in [E-BNF (Extended BNF)](grammars/EBNF_GRAMMAR.md) and [BNF](grammars/BNF_GRAMMAR.md) notations, and for [Jison](http://zaach.github.io/jison/try/usf/index.html) to display an interactive parsing table [check here](grammars/JISON_GRAMMAR.md).

We defined the operators precedence like the convention of C language.

### Function call

For this implementation, we only used the function call for `print(exp)` that will be used a syscall on MIPS. Semantic errors are been checked in code generation.

### Code Generation

The code is generated to [MIPS architecture](https://en.wikipedia.org/wiki/MIPS_instruction_set) using a stack machine strategy.
