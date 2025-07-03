import pygame

class mouse:
   def __init__(self):
      self.pos = pygame.Vector2(pygame.mouse.get_pos())

   def update(self):
      self.pos = pygame.Vector2(pygame.mouse.get_pos())

      return
   def getPos(self):
      return self.pos