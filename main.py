import re
import pandas as pd


KEYWORDS = {
    "alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit", "atomic_noexcept",
    "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t",
    "class", "compl", "concept", "const", "consteval", "constexpr", "const_cast", "continue", "co_await",
    "co_return", "co_yield", "decltype", "default", "delete", "do", "double", "dynamic_cast", "else", "enum",
    "explicit", "export", "extern", "false", "float", "for", "friend", "goto", "if", "inline", "int",
    "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq",
    "private", "protected", "public", "register", "reinterpret_cast", "requires", "return", "short",
    "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch", "template",
    "this", "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using",
    "virtual", "void", "volatile", "while", "xor", "xor_eq", "include"
}

DATATYPES = {"int", "float", "double", "char", "bool", "void", "long", "short", "unsigned"}

OPERATORS = {
    "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "&", "|", "^", "~",
    "<<", ">>", "++", "--", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", "->", "->*", ".*",
    "?", ":", "::", ".", "..."
}

SPECIAL_CHARS = {
    "{", "}", "(", ")", "[", "]", ";", ",", "#", "<", ">", "\"", "\'", "\\", "::"
}

TOKEN_REGEX = [
    ("KEYWORD", re.compile(r"\b(" + "|".join(KEYWORDS) + r")\b", re.IGNORECASE)),
    ("IDENTIFIER", re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")),
    ("NUMBER", re.compile(r"\b\d+(\.\d+)?\b")),
    ("OPERATOR", re.compile(r"(" + "|".join(re.escape(op) for op in OPERATORS) + r")")),
    ("SYMBOL", re.compile(r"(" + "|".join(re.escape(sym) for sym in SPECIAL_CHARS) + r")")),
    ("STRING_LITERAL", re.compile(r"\".*?\"")),
    ("CHAR_LITERAL", re.compile(r"'.?'")),
    ("NEWLINE", re.compile(r"\n"))
]

def lexical_analyzer(code):
    tokens = []
    errors = []
    line_num = 1
    
    for line in code.splitlines():
        position = 0
        prev_token_type = None
        prev_token_value = None
        has_semicolon = False 

        while position < len(line):
            match = None
            
            for token_type, pattern in TOKEN_REGEX:
                match = pattern.match(line, position)
                if match:
                    value = match.group(0)
                    
                    if token_type == "KEYWORD" and value.lower() in KEYWORDS and value not in KEYWORDS:
                        errors.append(f"Syntax Error: '{value}' should be lowercase as '{value.lower()}' at line {line_num}")

                    if token_type == "IDENTIFIER" and prev_token_type != "KEYWORD" and prev_token_value not in DATATYPES:
                        errors.append(f"Syntax Error: '{value}' is an identifier without a preceding datatype at line {line_num}")
                    
                    if prev_token_type == "IDENTIFIER" and token_type == "IDENTIFIER":
                        errors.append(f"Syntax Error: Unexpected identifier '{value}' at line {line_num}")
                    
                    tokens.append({"Line": line_num, "Token": value, "Type": token_type})
                    
                    if value == ";":
                        has_semicolon = True
                    
                    position = match.end(0)
                    prev_token_type = token_type
                    prev_token_value = value
                    break
            
            if not match:
                position += 1

        if not has_semicolon and any(tok["Type"] in ["KEYWORD", "IDENTIFIER", "OPERATOR"] for tok in tokens if tok["Line"] == line_num):
            errors.append(f"Syntax Error: Missing ';' at the end of line {line_num}")

        line_num += 1

    df = pd.DataFrame(tokens)
    print("\nToken Table:")
    print(df)

    if errors:
        print("\nErrors:")
        for error in errors:
            print(error)
    
    return df

if __name__ == "__main__":
    while True:
        cpp_code = input("Enter C++ code to analyze (or type 'exit' to quit):\n")
        if cpp_code.lower() == 'exit':
            break
        token_table = lexical_analyzer(cpp_code)
        print(token_table)

    input("Press Enter to exit...")

