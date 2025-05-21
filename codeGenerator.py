class IntermediateCodeGenerator:
    """
    Converts the AST to intermediate code (MASM-like instructions)
    """

    def __init__(self, ast):
        self.ast = ast
        self.intermediate_code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table = {
            # Arithmetic operations
            "+": "ADD",  # ADD destination, source
            "**":"POWER",
            "-": "SUB",  # SUB destination, source
            "*": "IMUL",  # IMUL destination, source
            "**": "POWER",  # POWER destination, source
            "/": "IDIV",  # IDIV source (DIV/IDIV uses implicit registers AX/DX)
            # Assignment
            "=": "MOV",  # MOV destination, source
            # Comparison (used with conditional jumps)
            "==": "JE",  # Jump if equal (use CMP first)
            "!=": "JNE",  # Jump if not equal
            "<": "JL",  # Jump if less (signed)
            "<=": "JLE",  # Jump if less or equal
            ">": "JG",  # Jump if greater
            ">=": "JGE",  # Jump if greater or equal
            # Logical operations
            "&&": "AND",  # AND destination, source
            "||": "OR",  # OR destination, source
            "!": "NOT",  # NOT destination
            # Control flow
            "if": "CMP",  # CMP followed by conditional jump
            "else": "JMP",  # Unconditional jump to else block
            "while": "CMP",  # CMP + loop label
            "jmp": "JMP",  # Unconditional jump
            "label": "LABEL",  # Just a label marker
            # Function support
            "function": "PROC",  # Label for a procedure
            "end_function": "ENDP",  # End of procedure
            "call": "CALL",  # Call a function
            "return": "RET",  # Return from procedure
            # I/O
            "print": "CALL Print",  # Custom I/O function call
            "input": "CALL Input",  # Custom input routine
            # Data types
            "string": "BYTE PTR",  # Define a string
            "int": "DWORD PTR",  # Define a 32-bit integer
        }

    def generate_intermediate_code(self):
        print("Generating intermediate code...")
        if not self.ast or not isinstance(self.ast, dict):
            raise ValueError("AST is empty or invalid")
        self.process_node(self.ast)
        return self.intermediate_code

    def process_node(self, node):
        node_type = node.get("type")
        if node_type == "assignment":
            self.handle_assignment(node)
        elif node_type == "arithmetic":
            self.handle_arithmetic(node)
        elif node_type == "conditional":
            self.handle_conditional(node)
        elif node_type == "loop":
            self.handle_loop(node)
        elif node_type == "function":
            self.handle_function(node)
        elif node_type == "io":
            self.handle_io(node)
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def handle_assignment(self, node):
        left = node["left"]
        right = node["right"]
        if isinstance(right, dict) and "operator" in right:
            temp = self.handle_arithmetic(right)
            self.intermediate_code.append(f"MOV {left}, {temp}")
        else:
            self.intermediate_code.append(f"MOV {left}, {right}")

    def handle_arithmetic(self, node):
        left = node["left"]
        op = node["operator"]
        right = node["right"]

        # Recursively handle operands if they are nested operations
        if isinstance(left, dict):
            left = self.handle_arithmetic(left)
        if isinstance(right, dict):
            right = self.handle_arithmetic(right)

        temp = f"temp{self.temp_counter}"
        self.temp_counter += 1
        self.intermediate_code.append(f"MOV {temp}, {left}")
        self.intermediate_code.append(f"{self.symbol_table[op]} {temp}, {right}")
        return temp

    def handle_conditional(self, node):
        cond = node["condition"]
        true_block = node["true_block"]
        false_block = node.get("false_block")
        l_true = f"label{self.label_counter}"
        self.label_counter += 1

        self.intermediate_code.append(f"CMP {cond['operand1']}, {cond['operand2']}")
        self.intermediate_code.append(f"JE {l_true}")

        for stmt in true_block:
            self.process_node(stmt)

        if false_block:
            l_end = f"LABEL{self.label_counter}"
            self.label_counter += 1
            self.intermediate_code.append(f"JMP {l_end}")
            for stmt in false_block:
                self.process_node(stmt)
            self.intermediate_code.append(f"{l_end}:")

        self.intermediate_code.append(f"{l_true}:")

    def handle_loop(self, node):
        cond = node["condition"]
        body = node["body"]
        l_start = f"LABEL{self.label_counter}"
        self.label_counter += 1
        l_end = f"LABEL{self.label_counter}"
        self.label_counter += 1

        self.intermediate_code.append(f"{l_start}:")
        self.intermediate_code.append(f"CMP {cond['operand1']}, {cond['operand2']}")
        self.intermediate_code.append(f"JE {l_end}")

        for stmt in body:
            self.process_node(stmt)

        self.intermediate_code.append(f"JMP {l_start}")
        self.intermediate_code.append(f"{l_end}:")

    def handle_function(self, node):
        name = node["name"]
        params = node.get("parameters", [])
        body = node["body"]

        self.intermediate_code.append(f"{self.symbol_table['function']} {name}")
        for param in params:
            self.intermediate_code.append(f"; param {param}")
        for stmt in body:
            self.process_node(stmt)
        self.intermediate_code.append("RET")

    def handle_io(self, node):
        op = node["operation"]
        var = node["variable"]
        self.intermediate_code.append(f"{self.symbol_table[op]} {var}")
