bloco ::= {comando [`;´]}

comando ::= Nome `=´ exp |
            chamadadefuncao |
            declaracaodevariavel |
            while exp do bloco end |
            if exp then bloco [else bloco] end

exp ::= Numero | Nome | chamadadefuncao |
        exp opbin exp | opunaria exp | `(´ exp `)´

chamadadefuncao ::=  Nome `(´ [listaexp] `)´

declaracaodevariavel ::= var Nome [`=´ exp]

listaexp ::= {exp `,´} exp

opbin ::= `+´ | `-´ | `*´ | `/´ | `<´ | `<=´ |
          `>´ | `>=´ | `==´ | `~=´ | and | or

opunaria ::= `-´  | not
