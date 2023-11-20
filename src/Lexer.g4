/* Python based stack machine grammar. */

lexer grammar Lexer;

// Keywords

TRUE               : 'True'  ;
FALSE              : 'False' ;

STRING             : ([uU] | [fF] [rR]? | [rR] [fF]?)? (SHORT_STRING | LONG_STRING)
                   | ([bB] [rR]? | [rR] [bB]) (SHORT_BYTES | LONG_BYTES)
                   ;

INTEGER            : PREFIX [1-9] [0-9]*
                   | '0'+
                   ;

FLOAT              : PREFIX EXPONENT_OR_POINT_FLOAT;

NAME_REF           : '\'' NAME ;
NAME               : ID_START ID_CONTINUE*;

NEWLINE            : RN                -> channel(HIDDEN);
WS                 : [ \t]+            -> channel(HIDDEN);
COMMENT            : '#' ~[\r\n\f]*    -> channel(HIDDEN);

// Fragments

fragment PREFIX : ('-' | '+')? ;

fragment SHORT_STRING
    : '\'' ('\\' (RN | .) | ~[\\\r\n'])* '\''
    | '"'  ('\\' (RN | .) | ~[\\\r\n"])* '"'
    ;

fragment LONG_STRING
    : '\'\'\'' LONG_STRING_ITEM*? '\'\'\''
    | '"""' LONG_STRING_ITEM*? '"""'
    ;

fragment LONG_STRING_ITEM
    : ~'\\'
    | '\\' (RN | .)
    ;

fragment RN
    : '\r'? '\n'
    ;

fragment EXPONENT_OR_POINT_FLOAT
    : ([0-9]+ | POINT_FLOAT) [eE] [+-]? [0-9]+
    | POINT_FLOAT
    ;

fragment POINT_FLOAT
    : [0-9]* '.' [0-9]+
    | [0-9]+ '.'
    ;

fragment SHORT_BYTES
    : '\'' (SHORT_BYTES_CHAR_NO_SINGLE_QUOTE | BYTES_ESCAPE_SEQ)* '\''
    | '"' (SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE | BYTES_ESCAPE_SEQ)* '"'
    ;

fragment LONG_BYTES
    : '\'\'\'' LONG_BYTES_ITEM*? '\'\'\''
    | '"""' LONG_BYTES_ITEM*? '"""'
    ;

fragment LONG_BYTES_ITEM
    : LONG_BYTES_CHAR
    | BYTES_ESCAPE_SEQ
    ;

fragment SHORT_BYTES_CHAR_NO_SINGLE_QUOTE
    : [\u0000-\u0009]
    | [\u000B-\u000C]
    | [\u000E-\u0026]
    | [\u0028-\u005B]
    | [\u005D-\u007F]
    ;

fragment SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE
    : [\u0000-\u0009]
    | [\u000B-\u000C]
    | [\u000E-\u0021]
    | [\u0023-\u005B]
    | [\u005D-\u007F]
    ;

/// Any ASCII character except "\"
fragment LONG_BYTES_CHAR
    : [\u0000-\u005B]
    | [\u005D-\u007F]
    ;

/// "\" <any ASCII character>
fragment BYTES_ESCAPE_SEQ
    : '\\' [\u0000-\u007F]
    ;

/// All characters in id_start, plus characters in the categories Mn, Mc, Nd, Pc and others with the Other_ID_Continue property
fragment ID_CONTINUE
    : ID_START
    | [0-9]
    ;

/// All characters in general categories Lu, Ll, Lt, Lm, Lo, Nl, the underscore, and characters with the Other_ID_Start property
fragment ID_START
    : [!-&]
    | [(-/]
    | [:-@]
    | [A-Z]
    | [[-`]
    | [a-z]
    | [{-~]
    ;
