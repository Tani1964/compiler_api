from lexicalAnalizer import LexicalAnalyzer
from syntaxAnalizer import SyntaxAnalyzer
from codeGenerator import IntermediateCodeGenerator
from machineCodeGenerator import MachineCodeGenerator

class Compiler:
    def __init__(self, statement):
        self.statement = statement
        self.tokens = []
        self.ast = {}
        self.lexical_analyzer = LexicalAnalyzer()
        self.syntax_analyzer = None
        self.intermediate_code_generator = None
        self.semantic_analyzer = None
        self.machine_code_generator = None
        self.intermediate_code = []
        self.machine_code = []

    def compile(self):
        # Step 1: lexical analysis
        self.tokens = self.lexical_analyzer.analyzer(self.statement)
        
        # Step 2: syntax analysis
        self.syntax_analyzer = SyntaxAnalyzer(self.tokens)
        self.ast = self.syntax_analyzer.parseTreeGenerator()
        print(self.ast)
        
        # Step 3: semantic analysis
        
        # Step 4: intermediate code generation
        self.intermediate_code_generator = IntermediateCodeGenerator(self.ast)
        self.intermediate_code = self.intermediate_code_generator.generate_intermediate_code()
        
        # # Step 5: code generation
        self.machine_code_generator = MachineCodeGenerator(self.intermediate_code)
        self.machine_code = self.machine_code_generator.generate_code()
        
        
        return [["tokens",self.tokens], ["AST",self.ast], ["intermediate_code",self.intermediate_code], ["machine_code",self.machine_code]]
