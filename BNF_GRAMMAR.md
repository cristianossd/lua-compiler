block := blocklist

blocklist := "" | blocklist command blockterminator

blockterminator := "" | SEMICOLON

command ::= ID ASSIGN exp |
            functioncall |
            vardeclaration |
            WHILE relexp DO block END |
            IF relexp THEN block elsestnt END

elsestnt ::= "" | ELSE block

relexp ::= exp relop exp

relop ::= LESS | LESSEQUAL | GREATER | GREATEREQUAL |
       EQUAL | NOTEQUAL | AND | OR

exp ::= functioncall
        exp MINUS term |
        exp PLUS term |
        term

term ::= term TIMES factor |
         term DIVIDE factor |
         factor

factor ::= LPAREN exp RPAREN |
           operator |
           unaryop LPAREN exp RPAREN |
           unaryop operator

operator ::= ID |
             NUMBER

functioncall ::= ID LPAREN explist RPAREN

vardeclaration := VAR ID expassign

expassign := "" | ASSIGN exp

explist ::= "" | lexp exp

lexp ::= "" | lexp exp COMMA

unaryop ::= MINUS | NOT
