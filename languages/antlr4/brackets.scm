("(" @open ")" @close)
("{" @open "}" @close)
("[" @open "]" @close)
(elementOptions "<" @open ">" @close)
(predicateOptions "<" @open ">" @close)
; Strings and lexer character sets are single tokens in the upstream grammar;
; their internal delimiters cannot be paired using structural queries.
