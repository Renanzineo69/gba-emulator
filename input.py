import pygame

class Input:
    def __init__(self):
        self.keys = {'A': False, 'B': False, 'Start': False, 'Select': False}

    def update(self):
        # Atualiza o estado dos botões
        keys = pygame.key.get_pressed()
        self.keys['A'] = keys[pygame.K_a]
        self.keys['B'] = keys[pygame.K_b]
        self.keys['Start'] = keys[pygame.K_RETURN]
        self.keys['Select'] = keys[pygame.K_SPACE]
