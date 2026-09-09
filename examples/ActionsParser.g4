parser grammar ActionsParser;
options { tokenVocab = ModesLexer; }
@members { int count = 0; }
start[int limit]
returns [int result]
locals [int seen = 0]
@init { count = 0; }
    : item[$limit] { $result = count; }
    ;
catch [Exception e] { throw e; }
finally { count = 0; }
item[int limit] : {count < $limit}? NAME { count++; };
