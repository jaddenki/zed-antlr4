(RULE_REF) @function
(TOKEN_REF) @constant

(grammarDecl (identifier) @type)
(delegateGrammar (identifier) @type)
(modeSpec (identifier) @label)
(option (identifier) @property)
(elementOption (identifier) @property)
(labeledElement (identifier) @label)
(labeledAlt "#" (identifier) @label)
(action_ (identifier) @attribute)
(ruleAction (identifier) @attribute)
(lexerCommandName) @keyword

((TOKEN_REF) @constant.builtin
  (#eq? @constant.builtin "EOF"))

(ACTION) @embedded
(argActionBlock) @embedded
(STRING_LITERAL) @string
(DoubleQuoteLiteral) @string
(TripleQuoteLiteral) @string
(BacktickQuoteLiteral) @string
(LEXER_CHAR_SET) @string.regex
(INT) @number

[
  "grammar" "lexer" "parser" "import" "options" "tokens" "channels"
  "fragment" "mode" "returns" "locals" "throws" "catch" "finally"
  "public" "private" "protected"
] @keyword

[ "=" "+=" "->" "?" "*" "+" "~" ".." "." ] @operator
[ ":" ";" "," "|" "::" ] @punctuation.delimiter
[ "@" "#" ] @punctuation.special
[ "(" ")" "[" "]" "{" "}" "<" ">" ] @punctuation.bracket

(line_comment) @comment
(block_comment) @comment
(doc_comment) @comment.doc
