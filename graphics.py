import pygame
import numpy as np

class Graphics:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((240, 160))  # Resolução GBA
        self.framebuffer = pygame.Surface((240, 160))

    def render(self, framebuffer_data):
        # Garantir que framebuffer_data seja um array 2D (160x240)
        framebuffer_array = np.array(framebuffer_data, dtype=np.uint16)

        # Verifica se a forma do framebuffer_array é a correta (160x240)
        if framebuffer_array.shape != (160, 240):
            print(f"Warning: framebuffer_data has incorrect shape: {framebuffer_array.shape}")
            return

        # Converte de RGB565 para RGB888 (16 bits para 24 bits)
        framebuffer_rgb = self.convert_rgb565_to_rgb888(framebuffer_array)

        # Agora, usamos pygame.surfarray.blit_array para desenhar na tela
        pygame.surfarray.blit_array(self.framebuffer, framebuffer_rgb)

        # Atualiza a tela
        self.screen.blit(self.framebuffer, (0, 0))
        pygame.display.update()

    def clear(self):
        self.framebuffer.fill((0, 0, 0))  # Limpar a tela

    def convert_rgb565_to_rgb888(self, framebuffer_data):
        # Converte um array de 16 bits (RGB565) para um array de 24 bits (RGB888)
        r = (framebuffer_data >> 11) & 0x1F
        g = (framebuffer_data >> 5) & 0x3F
        b = framebuffer_data & 0x1F

        # Expande de 5/6 bits para 8 bits por canal
        r = (r << 3) | (r >> 2)
        g = (g << 2) | (g >> 4)
        b = (b << 3) | (b >> 2)

        # Concatena os 3 canais (r, g, b) para criar um array RGB
        rgb888 = np.stack((r, g, b), axis=-1)
        return rgb888
