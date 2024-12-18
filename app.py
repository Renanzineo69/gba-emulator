import pygame
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageTk

# Classe para gerenciar a CPU ARM7
class ARM7:
    def __init__(self):
        self.registers = [0] * 16  # 16 registradores de propósito geral (R0 a R15)
        self.pc = 0x08000000  # Program Counter (inicia na ROM)
        self.sp = 0x0307F000  # Stack Pointer
        self.lr = 0  # Link Register
        self.cpsr = 0  # Current Program Status Register (não implementado)

    def read_register(self, index):
        """ Lê o valor de um registrador específico (R0 a R15) """
        return self.registers[index]

    def write_register(self, index, value):
        """ Escreve um valor em um registrador específico (R0 a R15) """
        self.registers[index] = value


# Classe para gerenciar o emulador
class Emulator:
    def __init__(self, canvas):
        self.cpu = ARM7()
        self.memory = [0] * (32 * 1024 * 1024)  # 32MB de memória
        self.video = Video(self, canvas)  # Inicializando a renderização de vídeo
        self.running = True

    def load_rom(self, rom_path):
        """ Carrega a ROM na memória do GBA """
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        # Verificar se a ROM não ultrapassa o limite de memória a partir de 0x08000000
        rom_size = len(rom_data)
        if rom_size > (32 * 1024 * 1024 - 0x08000000):
            print(f"Erro: ROM de {rom_size} bytes é muito grande para a memória alocada!")
            return None
        
        # Carregar a ROM na memória (a partir da posição 0x08000000)
        for i in range(rom_size):
            self.memory[0x08000000 + i] = rom_data[i]

        print(f"ROM carregada: {rom_path}")
        return rom_data

    def read_instruction(self):
        """ Lê a próxima instrução da memória """
        instruction = (self.memory[self.cpu.pc] << 24) | \
                      (self.memory[self.cpu.pc + 1] << 16) | \
                      (self.memory[self.cpu.pc + 2] << 8) | \
                      self.memory[self.cpu.pc + 3]
        self.cpu.pc += 4  # A instrução tem 4 bytes
        return instruction

    def execute_instruction(self, instruction):
        """ Decodifica e executa a instrução """
        opcode = (instruction >> 21) & 0xF  # Pega os 4 bits mais significativos (código da operação)

        if opcode == 0b0100:  # Exemplo: ADD
            rd = (instruction >> 12) & 0xF
            rn = (instruction >> 16) & 0xF
            rm = instruction & 0xF
            self.cpu.write_register(rd, self.cpu.read_register(rn) + self.cpu.read_register(rm))
            print(f"ADD: r{rd} = r{rn} + r{rm}")
        else:
            print(f"Instrução desconhecida: {hex(instruction)}")

    def emulate_cpu(self, rom_data):
        """ Executa as instruções da ROM """
        self.cpu.pc = 0x08000000  # O GBA começa a executar a partir do endereço 0x08000000
        while self.running:
            instruction = self.read_instruction()
            self.execute_instruction(instruction)
            # Verifique se o PC está fora dos limites da ROM para parar a execução
            if self.cpu.pc >= 0x08000000 + len(rom_data):
                self.running = False

    def process_input(self):
        """ Captura a entrada do usuário (teclado) """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            pass  # Simula o pressionamento do botão A
        if keys[pygame.K_b]:
            pass  # Simula o pressionamento do botão B
        if keys[pygame.K_UP]:
            pass  # Simula o pressionamento do direcional para cima
        if keys[pygame.K_DOWN]:
            pass  # Simula o pressionamento do direcional para baixo

    def run(self, rom_data):
        """ Loop principal do emulador """
        pygame.init()
        self.video.init_screen()

        while self.running:
            self.process_input()  # Lê a entrada do usuário
            self.emulate_cpu(rom_data)  # Executa a CPU
            self.video.update_screen()  # Atualiza a tela do emulador
            pygame.display.update()  # Atualiza a tela

        pygame.quit()


class Video:
    def __init__(self, emulator, canvas):
        self.emulator = emulator
        self.canvas = canvas
        self.framebuffer = np.zeros((240, 160), dtype=np.uint8)  # Memória de vídeo (tela)
        self.pygame_surface = pygame.Surface((240, 160))  # Superfície do Pygame

    def init_screen(self):
        """ Inicializa a tela do Pygame """
        pygame.display.set_caption("GBA Emulator")

    def update_screen(self):
        """ Atualiza a tela com os dados da memória de vídeo """
        for y in range(160):
            for x in range(240):
                color = self.framebuffer[x, y]
                self.pygame_surface.set_at((x, y), (color, color, color))  # Coloca o pixel na tela

        # Atualiza a tela do Tkinter com a superfície do Pygame
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pygame_to_tk_image())

    def pygame_to_tk_image(self):
        """ Converte a superfície do Pygame para uma imagem Tkinter """
        pygame_image = pygame.image.tostring(self.pygame_surface, "RGB")
        img = Image.frombytes('RGB', (240, 160), pygame_image)
        return ImageTk.PhotoImage(img)


def open_rom():
    """ Abre o explorador de arquivos para selecionar a ROM """
    file_path = filedialog.askopenfilename(title="Selecione a ROM", filetypes=[("GBA Files", "*.gba")])
    if file_path:
        print(f"Arquivo selecionado: {file_path}")
        emulator.load_rom(file_path)


# Interface gráfica com Tkinter
def setup_gui():
    """ Cria a interface gráfica do emulador """
    global emulator, root

    # Configuração da janela Tkinter
    root = tk.Tk()
    root.title("Emulador GBA")

    # Criar o Canvas para exibir a tela do Pygame
    canvas = tk.Canvas(root, width=240, height=160)
    canvas.pack(pady=20)

    # Criar botão para importar a ROM
    import_button = tk.Button(root, text="Importar Jogo", command=open_rom)
    import_button.pack(pady=20)

    # Criar um label para exibir a tela do Pygame dentro da janela Tkinter
    global label
    label = tk.Label(root)
    label.pack()

    # Inicializar o emulador
    emulator = Emulator(canvas)

    # Iniciar a interface gráfica
    root.mainloop()


def main():
    """ Função principal para rodar o emulador """
    setup_gui()


if __name__ == "__main__":
    main()
