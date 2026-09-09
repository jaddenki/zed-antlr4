lexer grammar ModesLexer;
channels { COMMENTS }
OPEN : '<' -> pushMode(TAG);
TEXT : ~[<]+;
WS : [ \t\r\n]+ -> channel(HIDDEN);
mode TAG;
CLOSE : '>' -> popMode;
NAME : [a-z]+;
