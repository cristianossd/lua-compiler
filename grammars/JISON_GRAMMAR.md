block
    : blocklist
    ;

blocklist
    :
    | blocklist command blockterminator
    ;

blockterminator
    :
    | SEMICOLON
    ;

command
    : ID ASSIGN exp
    | functioncall
    | vardeclaration
    | WHILE exp DO block END
    | IF exp THEN block elsestnt END
    ;

elsestnt
    :
    | ELSE block
    ;

exp
    : NUMBER
    | ID
    | functioncall
    | exp binop exp
    | unaryop exp
    | LPAREN exp RPAREN
    ;

functioncall
    : ID LPAREN explist RPAREN
    ;

vardeclaration
    : VAR ID expassign
    ;

expassign
    :
    | ASSIGN exp
    ;

explist
    :
    | lexp exp
    ;

lexp
    :
    | lexp exp COMMA
    ;

binop
    : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | LESS
    | LESSEQUAL
    | GREATER
    | GREATEREQUAL
    | EQUAL
    | NOTEQUAL
    | AND
    | OR
    ;

unaryop
    : MINUS
    | NOT
    ;
