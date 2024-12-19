class Memory:
    def __init__(self, size):
        self.memory = [0] * size  # Criando a memória

    def read(self, address):
        # Verifica se o endereço está dentro dos limites da memória
        if address >= len(self.memory):
            print(f"Warning: Accessing memory out of bounds at address {hex(address)}")
            return 0  # Ou lance uma exceção, dependendo de como deseja lidar com isso.
        return self.memory[address]

    def write(self, address, value):
        # Verifica se o endereço está dentro dos limites da memória
        if address >= len(self.memory):
            print(f"Warning: Writing memory out of bounds at address {hex(address)}")
            return  # Ou lance uma exceção
        self.memory[address] = value

    def load_rom(self, rom_data):
        # Carregar a ROM na memória (parte da memória mapeada)
        for i in range(len(rom_data)):
            self.write(i, rom_data[i])
