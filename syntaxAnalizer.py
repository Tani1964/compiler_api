import re
"""
Token types:
- keyword
- operator
- delimiter
- identifier

"""


class SyntaxAnalyzer:
    def __init__(self, tokensWithTypes):
        self.tokensWithTypes = tokensWithTypes
        self.valid = False
        self.matched_rule = None

        self.rules = {
            'assignment': [
                ['identifier', 'operator', 'identifier'],
                ['identifier', 'operator', 'string'],
                ['identifier', 'operator', 'identifier', 'operator', 'identifier'],
                ['identifier', 'operator', 'identifier', 'operator', 'string'],
                ['identifier', 'operator', 'string', 'operator', 'identifier']
            ],
            'arithmetic': [
                ['identifier', 'operator', 'identifier', 'operator', 'identifier'],
                ['identifier', 'operator', 'identifier', 'operator', 'identifier', 'operator', 'identifier']
            ],
            'declaration': [
                ['keyword', 'identifier', 'operator', 'identifier', 'delimiter'],
                ['keyword', 'identifier', 'operator', 'string', 'delimiter']
            ],
            'function_call': [
                ['identifier', 'delimiter', 'identifier', 'delimiter'],
                ['identifier', 'delimiter', 'string', 'delimiter'],
                ['identifier', 'delimiter', 'identifier', 'delimiter', 'delimiter'],
                ['identifier', 'delimiter', 'string', 'delimiter', 'delimiter']
            ],
            'if': [
                ['keyword', 'delimiter', 'identifier', 'delimiter'],
                ['keyword', 'delimiter', 'string', 'delimiter']
            ],
            'else': [['keyword']],
            'while': [
                ['keyword', 'delimiter', 'identifier', 'delimiter'],
                ['keyword', 'delimiter', 'string', 'delimiter']
            ],
            'function_def': [
                ['keyword', 'identifier', 'delimiter', 'identifier', 'delimiter', 'identifier', 'delimiter'],
                ['keyword', 'identifier', 'delimiter', 'delimiter']  # function f()
            ]
        }

    def convert_type(self, token, original_type):
        if original_type == 'identifier' and (
            token.startswith('"') and token.endswith('"') or
            token.startswith("'") and token.endswith("'")
        ):
            return 'string'
        return original_type

    def analyze(self):
        types_sequence = [self.convert_type(t[0], t[1]) for t in self.tokensWithTypes]
        for rule_name, patterns in self.rules.items():
            for pattern in patterns:
                if types_sequence == pattern:
                    self.valid = True
                    self.matched_rule = rule_name
                    return True
        return False

    def get_result(self):
        if self.analyze():
            return f"✅ Valid syntax: {self.matched_rule}"
        else:
            return "❌ Invalid syntax."

    def parseTreeGenerator(self):
        if not self.analyze():
            return "❌ Invalid syntax."

        if self.matched_rule == 'assignment':
            return self.assignmentTree()
        else:
            return f"✅ Matched rule: {self.matched_rule}, but no AST generator implemented."

    def assignmentTree(self):
        """
        Supports: 
        x = y
        x = y + z
        x = "hello" + y
        x = y + "hello"
        """
        tokens = self.tokensWithTypes
        tree = {}

        # Find assignment operator
        for i, (tok, typ) in enumerate(tokens):
            if tok == "=":
                left = tokens[i-1][0]

                # Simple binary or ternary expressions
                right_tokens = tokens[i+1:]
                if len(right_tokens) == 1:
                    right = right_tokens[0][0]
                elif len(right_tokens) == 3:
                    # y + z
                    right = {
                        'operator': right_tokens[1][0],
                        'left': right_tokens[0][0],
                        'right': right_tokens[2][0]
                    }
                else:
                    # Handle malformed expressions
                    right = "Unsupported expression structure"

                tree = {
                    'type': 'assignment',
                    'operator': '=',
                    'left': left,
                    'right': right
                }
                break
        return tree
