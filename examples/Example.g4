grammar Example;

// Open this file in Zed after installing the extension.
options {
    language = Java;
}
import Common;
tokens { EXTRA }

@parser::members { int count = 0; }

/** A small expression grammar. */
start
    : expression EOF
    ;

expression
    : left=expression op=('+' | '-') right=expression # Binary
    | INT                                             # Integer
    | '(' expression ')'                              # Group
    ;

// Epsilon alternatives are supported.
optionalName : ID | ;
empty : ;

fragment DIGIT : '0'..'9';
INT : DIGIT+;
ID : [a-zA-Z_] [a-zA-Z_0-9]*;
WS : [ \t\r\n]+ -> skip;
/* A literal escape and a negated character set. */
LINE : '//' ~[\r\n]* -> channel(HIDDEN);
