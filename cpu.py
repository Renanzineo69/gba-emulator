class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.registers = [0] * 16  # R0 - R15
        self.cpsr = 0  # Status de controle
        self.pc = 0x08000000  # Inicializa o PC para o endereço correto da ROM
        self.sp = 0  # Ponteiro de pilha
        self.lr = 0  # Registrador de link
        self.emulating = True

    def execute_instruction(self, instruction):
        # Aqui você pode implementar as instruções reais do ARM
        # Para simplificação, só mostramos o endereço da instrução
        print(f"Executando instrução: {hex(instruction)}")

    def fetch(self):
        # Verifica se o PC está dentro dos limites da memória
        if self.pc >= len(self.memory.memory):
            print(f"Warning: PC out of range: {hex(self.pc)}")
            self.emulating = False  # Finaliza a execução
            return 0
        instruction = self.memory.read(self.pc)
        self.pc += 4  # Avança o PC para a próxima instrução
        return instruction

    def run(self, cycles=10000):
        # Limite de ciclos para evitar loops infinitos
        count = 0
        while self.emulating and count < cycles:
            instruction = self.fetch()
            if instruction == 0:
                break  # Sai do loop se a instrução for 0 (indicando fim ou erro)
            self.execute_instruction(instruction)
            count += 1
