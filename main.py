import pygame
from cpu import CPU
from memory import Memory
from graphics import Graphics
from input import Input

def main():
    # Inicialização dos componentes
    memory = Memory(32 * 1024 * 1024)  # 32MB de RAM
    cpu = CPU(memory)
    graphics = Graphics()
    input_handler = Input()

    # Carregar a ROM do Pokémon Emerald
    try:
        with open('pokemon_emerald.gba', 'rb') as rom_file:
            rom_data = rom_file.read()
            print("ROM carregada com sucesso!")
            print(f"Primeiros 64 bytes da ROM: {rom_data[:64]}")  # Imprime os primeiros 64 bytes da ROM
            memory.load_rom(rom_data)
    except FileNotFoundError:
        print("Erro: Arquivo da ROM não encontrado.")
        return

    # Loop principal do emulador
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Atualizar o estado de entrada
        input_handler.update()

        # Emular o ciclo da CPU por mais ciclos
        cpu.run(cycles=10000)  # Emular mais ciclos para garantir que o código da ROM avance

        # Verificar o endereço do framebuffer
        framebuffer_start = 0x06000000
        framebuffer_end = framebuffer_start + 240 * 160

        framebuffer_data = memory.memory[framebuffer_start:framebuffer_end]

        # Verifique o comprimento e conteúdo
        if len(framebuffer_data) != 240 * 160:
            print(f"Warning: framebuffer_data has incorrect length: {len(framebuffer_data)}")
        if not framebuffer_data:
            print("Warning: framebuffer_data is empty!")

        # Atualizar a parte gráfica (renderizando o framebuffer)
        graphics.render(framebuffer_data)

        # Controlar o FPS
        pygame.time.delay(16)  # Aproximadamente 60 FPS

if __name__ == '__main__':
    main()
