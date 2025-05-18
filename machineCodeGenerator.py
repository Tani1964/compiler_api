class MachineCodeGenerator:
    def __init__(self, intermediate_code):
        self.intermediate_code = intermediate_code
        self.code = []
        self.masm_to_binary = {
            # Arithmetic
            "ADD": "000000",
            "SUB": "001010",
            "IMUL": "0000111110101111",
            "IDIV": "11110111",
            # Assignment
            "MOV": "100010",
            # Comparison / Conditionals
            "CMP": "001110",
            "JE": "01110100",
            "JNE": "01110101",
            "JL": "01111100",
            "JLE": "01111110",
            "JG": "01111111",
            "JGE": "01111101",
            # Logical
            "AND": "001000",
            "OR": "000010",
            "NOT": "1111011",
            # Control Flow
            "JMP": "11101011",
            "LABEL": "00000000",
            # Functions
            "PROC": "00000000",
            "ENDP": "00000000",
            "CALL": "11101000",
            "RET": "11000011",
            # I/O
            "CALL Print": "11101000",
            "CALL Input": "11101000",
            # Data types
            "BYTE PTR": "",
            "DWORD PTR": "",
        }

    def add_instruction(self, instruction):
        self.code.append(instruction)

    def generate_code(self):
        for instruction in self.intermediate_code:
            instruction_parts = instruction.split()
            if not instruction_parts:
                continue
            opcode = instruction_parts[0]

            if opcode in self.masm_to_binary:
                binary_opcode = self.masm_to_binary[opcode]
                operands = instruction_parts[1:]
                binary_operands = " ".join(operands) if operands else ""
                binary_instruction = f"{binary_opcode} {binary_operands}".strip()
                self.add_instruction(binary_instruction)
            else:
                # Fallback or unsupported opcode
                self.add_instruction(f"; Unsupported instruction: {instruction}")

        return "\n".join(self.code)

    def clear_code(self):
        self.code = []
