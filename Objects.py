import pygame


class ClassTable : 
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        