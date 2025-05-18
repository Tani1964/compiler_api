import re

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = ["if", "else", "while", "for", "int", "float", "char"]
        self.operators = ["+", "-", "*", "/", "=", "<", ">", "<=", ">=", "==", "!="]
        self.delimiters = [";", ",", "{", "}"]

    def is_keyword(self, token):
        return token in self.keywords

    def is_operator(self, token):
        return token in self.operators

    def is_delimiter(self, token):
        return token in self.delimiters

    def is_identifier(self, token):
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token) and not self.is_keyword(token)

    def scanner(self, statement):
        # Tokenize using regex to capture operators, identifiers, numbers, etc.
        pattern = r'(\b\w+\b|==|!=|<=|>=|[+\-*/=<>;{},])'
        tokens = re.findall(pattern, statement)
        return tokens

    def analyzer(self, statement):
        tokensWithTypes = []
        tokens = self.scanner(statement)

        for token in tokens:
            if self.is_keyword(token):
                tokensWithTypes.append([token, "keyword"])
            elif self.is_operator(token):
                tokensWithTypes.append([token, "operator"])
            elif self.is_delimiter(token):
                tokensWithTypes.append([token, "delimiter"])
            elif token.isdigit():
                tokensWithTypes.append([token,"int"])
            elif self.is_identifier(token):
                tokensWithTypes.append([token,"identifier"])
            else:
                tokensWithTypes.append([token,"unknown"])
        
        print(tokensWithTypes)
        return tokensWithTypes
