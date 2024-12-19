class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.registers = [0] * 16  # R0 - R15
        self.cpsr = 0  # Status de controle
        self.pc = 0x08000000  # Inicializa o PC para o endereço de início da ROM
        self.sp = 0  # Ponteiro de pilha
        self.lr = 0  # Registrador de link
        self.emulating = True

    def execute_instruction(self, instruction):
        print(f"Executando instrução: {hex(instruction)}")  # Log de cada instrução
        # Aqui, em uma implementação completa, você emularia cada instrução da ARM.

    def fetch(self):
        # Verifica se o PC está dentro dos limites da memória
        if self.pc >= len(self.memory.memory):
            print(f"Warning: PC out of range: {hex(self.pc)}")
            self.emulating = False
            return 0
        instruction = self.memory.read(self.pc)
        self.pc += 4  # Avança para a próxima instrução
        print(f"PC atualizado para: {hex(self.pc)}")  # Log do PC
        return instruction

    def run(self, cycles=10000):
        count = 0
        while self.emulating and count < cycles:
            instruction = self.fetch()
            if instruction == 0:
                break  # Finaliza se encontrar uma instrução inválida (ou um finalizador)
            self.execute_instruction(instruction)
            count += 1
