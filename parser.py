import ply.yacc as yacc

class Parser(object):

  precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'CIRCUMFLEX'),
    ('right', 'UMINUS')
  )

  def p_chunk(p):
    '''chunk : {stat [SEMICOLON]} [laststat [SEMICOLON]]'''
    pass

  def p_block(p):
    '''block : chunk'''
    pass

  def p_stat(p):
    '''stat : varlist ASSIGN explist
            | functioncall
            | DO block END
            | WHILE exp DO block END
            | REPEAT block UNTIL exp
            | IF exp THEN block {ELSEIF exp THEN block} [ELSE block] END
            | FOR ID ASSIGN exp COMMA exp [COMMA exp] DO block END
            | FOR namelist IN explist DO block END
            | FUNCTION funcname funcbody
            | LOCAL FUNCTION ID funcbody
            | LOCAL namelist [ASSIGN explist]'''
    pass

  def p_laststat(p):
    '''laststat : RETURN [explist]
                | BREAK'''
    pass

  def p_funcname(p):
    '''funcname : ID {DOT ID} [TWODOTS ID]'''
    pass

  def p_varlist(p):
    '''varlist : var {COMMA var}'''
    pass

  def p_var(p):
    '''var : ID
           | prefixexp LSQUARE exp RSQUARE
           | prefixexp DOT ID'''
    pass

  def p_namelist(p):
    '''namelist : ID {DOT ID}'''
    pass

  def p_explist(p):
    '''explist : {exp COMMA} exp'''
    pass

  def p_exp(p):
    '''exp : NIL
           | FALSE
           | TRUE
           | NUMBER
           | STRING
           | THREEDOTS
           | function
           | prefixexp
           | tableconstructor
           | exp binop exp
           | unop exp'''
    pass

  def p_prefixexp(p):
    '''prefixexp : var
                 | functioncall
                 | LPAREN exp RPAREN'''
    pass

  def p_functioncall(p):
    '''functioncall : prefixexp args
                    | prefixexp COLON ID args'''
    pass

  def p_args(p):
    '''args : LPAREN [explist] RPAREN
            | tableconstructor
            | STRING'''
    pass

  def p_function(p):
    '''function : FUNCTION funcbody'''
    pass

  def p_funcbody(p):
    '''funcbody : LPAREN [parlist] RPAREN block END'''
    pass

  def p_parlist(p):
    '''parlist : namelist [COMMA THREEDOTS]
               | THREEDOTS'''
    pass

  def p_tableconstructor(p):
    '''tableconstructor : LCURLY [fieldlist] RCURLY'''
    pass

  def p_fieldlist(p):
    '''fieldlist : field {fieldsep field} [fieldsep]'''
    pass

  def p_field(p):
    '''field : LSQUARE exp RSQUARE ASSIGN exp
             | ID ASSIGN exp
             | exp'''
    pass

  def p_fieldsep(p):
    '''fieldsep : COMMA
                | SEMICOLON'''
    pass

  def p_binop(p):
    '''binop : PLUS
             | MINUS
             | TIMES
             | DIVIDE
             | CIRCUMFLEX
             | PERCENT
             | TWODOTS
             | LESS
             | LESSEQUAL
             | GREATER
             | GREATEREQUAL
             | EQUAL
             | NOTEQUAL
             | AND
             | OR'''
    pass

  def p_unop(p):
    '''unop : MINUS
            | NOT
            | SHARP'''
    pass
