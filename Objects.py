import pygame

class Table:
   def __init__(self, type:str, pos, size, children=[], scale=1):
        self.type = type
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[0])