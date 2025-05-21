import re

class SyntaxAnalyzer:
    def __init__(self, tokensWithTypes):
        self.tokensWithTypes = tokensWithTypes
        self.valid = False
        self.matched_rule = None
        self.current_index = 0
        
        # Define operator precedence (higher number = higher precedence)
        self.precedence = {
            '=': 1,
            '<': 2, '>': 2, '<=': 2, '>=': 2, '==': 2, '!=': 2,
            '+': 3, '-': 3,
            '*': 4, '/': 4,
            '**': 5  # Exponentiation has highest precedence
        }

        self.rules = {
            'assignment': ['identifier', 'operator', '*expression'],
            'declaration': [
                ['keyword', 'identifier', 'operator', 'identifier', 'delimiter'],
                ['keyword', 'identifier', 'operator', 'string', 'delimiter']
            ],
            'function_call': [
                ['identifier', 'delimiter', 'identifier', 'delimiter'],
                ['identifier', 'delimiter', 'string', 'delimiter']
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
                ['keyword', 'identifier', 'delimiter', 'delimiter']
            ]
        }

    def convert_type(self, token, original_type):
        if original_type == 'identifier':
            if token.startswith('"') and token.endswith('"') or token.startswith("'") and token.endswith("'"):
                return 'string'
            if re.match(r'^\d+(\.\d+)?$', token):
                return 'number'
        elif original_type == 'int':
            return 'number'
        return original_type

    def analyze(self):
        # Reset index for parsing
        self.current_index = 0
        
        # Get types sequence with properly converted types
        self.types_sequence = [self.convert_type(t[0], t[1]) for t in self.tokensWithTypes]
        
        # Try all rule patterns
        for rule_name, patterns in self.rules.items():
            if isinstance(patterns[0], list):  # multiple patterns
                for pattern in patterns:
                    if self.match_pattern(pattern):
                        self.valid = True
                        self.matched_rule = rule_name
                        return True
            else:  # flexible pattern like assignment
                if patterns == ['identifier', 'operator', '*expression']:
                    if (len(self.types_sequence) >= 3 and 
                        self.types_sequence[0] == 'identifier' and 
                        self.types_sequence[1] == 'operator' and
                        self.tokensWithTypes[1][0] == '='):  # Must be assignment operator
                        
                        # Check if the rest forms a valid expression
                        self.current_index = 2  # Start after identifier and operator
                        if self.parse_expression():
                            if self.current_index == len(self.types_sequence):  # Consumed all tokens
                                self.valid = True
                                self.matched_rule = 'assignment'
                                return True
        
        return False

    def match_pattern(self, pattern):
        if len(pattern) != len(self.types_sequence):
            return False
        
        for i, expected_type in enumerate(pattern):
            if self.types_sequence[i] != expected_type:
                return False
        
        return True

    def parse_expression(self):
        """
        Parse expression with operator precedence and brackets
        Based on recursive descent parsing
        """
        return self.parse_assignment()
    
    def parse_assignment(self):
        """Lowest precedence: assignment"""
        return self.parse_comparison()
    
    def parse_comparison(self):
        """Next level: comparison operators"""
        left = self.parse_additive()
        if not left:
            return False
        
        while (self.current_index < len(self.types_sequence) and
               self.types_sequence[self.current_index] == 'operator' and
               self.precedence.get(self.tokensWithTypes[self.current_index][0], 0) == 2):
            
            self.current_index += 1  # Skip operator
            right = self.parse_additive()
            if not right:
                return False
        
        return True
    
    def parse_additive(self):
        """Next level: addition and subtraction"""
        left = self.parse_multiplicative()
        if not left:
            return False
        
        while (self.current_index < len(self.types_sequence) and
               self.types_sequence[self.current_index] == 'operator' and
               self.precedence.get(self.tokensWithTypes[self.current_index][0], 0) == 3):
            
            self.current_index += 1  # Skip operator
            right = self.parse_multiplicative()
            if not right:
                return False
        
        return True
    
    def parse_multiplicative(self):
        """Next level: multiplication and division"""
        left = self.parse_exponentiation()
        if not left:
            return False
        
        while (self.current_index < len(self.types_sequence) and
               self.types_sequence[self.current_index] == 'operator' and
               self.precedence.get(self.tokensWithTypes[self.current_index][0], 0) == 4):
            
            self.current_index += 1  # Skip operator
            right = self.parse_exponentiation()
            if not right:
                return False
        
        return True
    
    def parse_exponentiation(self):
        """Highest binary operator precedence: exponentiation"""
        left = self.parse_primary()
        if not left:
            return False
        
        while (self.current_index < len(self.types_sequence) and
               self.types_sequence[self.current_index] == 'operator' and
               self.precedence.get(self.tokensWithTypes[self.current_index][0], 0) == 5):
            
            self.current_index += 1  # Skip operator
            right = self.parse_primary()
            if not right:
                return False
        
        return True
    
    def parse_primary(self):
        """Parse primary expressions including parenthesized expressions"""
        if self.current_index >= len(self.types_sequence):
            return False
        
        # Handle literal or identifier
        if self.types_sequence[self.current_index] in {'identifier', 'number', 'string'}:
            self.current_index += 1
            return True
        
        # Handle parenthesized expression
        elif (self.types_sequence[self.current_index] == 'delimiter' and 
              self.tokensWithTypes[self.current_index][0] == '('):
            
            self.current_index += 1  # Skip opening bracket
            result = self.parse_expression()
            
            # Check for closing bracket
            if (result and 
                self.current_index < len(self.types_sequence) and
                self.types_sequence[self.current_index] == 'delimiter' and
                self.tokensWithTypes[self.current_index][0] == ')'):
                
                self.current_index += 1  # Skip closing bracket
                return True
            
            return False
        
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
        tokens = self.tokensWithTypes
        left = tokens[0][0]  # assignment target
        
        # Parse the right-hand expression with precedence handling
        ast = self.build_expression_tree(tokens[2:])
        
        return {
            'type': 'assignment',
            'operator': '=',
            'left': left,
            'right': ast
        }

    def build_expression_tree(self, tokens):
        """
        Builds an expression tree respecting operator precedence and brackets
        """
        # Create a parser for just the expression tokens
        parser = ExpressionParser(tokens, self.precedence)
        return parser.parse()


class ExpressionParser:
    def __init__(self, tokens, precedence):
        self.tokens = tokens
        self.current = 0
        self.precedence = precedence
    
    def parse(self):
        return self.expression()
    
    def expression(self):
        return self.binary_expression(0)  # Start with lowest precedence
    
    def binary_expression(self, min_precedence):
        left = self.primary()
        
        while self.current < len(self.tokens):
            # Check if current token is an operator
            if self.tokens[self.current][1] != 'operator':
                break
                
            op = self.tokens[self.current][0]
            op_precedence = self.precedence.get(op, 0)
            
            # Break if operator has lower precedence than minimum
            if op_precedence < min_precedence:
                break
                
            # Consume operator
            self.current += 1
            
            # Parse right side with higher precedence
            right = self.binary_expression(op_precedence + 1)
            
            # Create binary expression node
            left = {
                'operator': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def primary(self):
        token = self.tokens[self.current]
        
        # Handle bracketed expressions
        if token[1] == 'delimiter' and token[0] == '(':
            self.current += 1  # Skip opening bracket
            expr = self.expression()
            
            # Verify closing bracket
            if self.current < len(self.tokens) and self.tokens[self.current][0] == ')':
                self.current += 1  # Skip closing bracket
                return expr
            else:
                raise SyntaxError("Expected closing bracket ')'")
        
        # Handle literals and identifiers
        self.current += 1
        return token[0]