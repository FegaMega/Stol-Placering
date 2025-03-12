import pygame

class Table:
   def __init__(self, type:str, pos, size, children=[], scale=1):
      self.type = type
      self.rect = pygame.Rect(pos[0], pos[1], size[0], size[0])
      self.color = (0, 0, 0)
   def draw(self, screen: pygame.surface.Surface):
      match self.type:
         case "Round":
            pygame.draw.circle(screen, self.color, self.rect.center, self.rect.width)
         case "Rectangular":
            pygame.draw.rect(screen, self.color, self.rect)

class Person:
   def __init__(self, pos, text, FONT, scale):
      self.Font = pygame.font.SysFont(FONT, 20*scale["Font"]["People"])
      self.name : pygame.Surface = self.Font.render(text, True, (255, 255, 255))
      self.rect = pygame.Rect(pos[0], pos[1], self.name.get_size()[0], self.name.get_size()[1])
   def draw(self, screen:pygame.Surface):
      screen.blit(self.name, self.rect)

class Tavla:
   def __init__(self, pos, size, FONT, scale=1):
      self.rect = pygame.Rect(pos[0] *scale, pos[1] *scale, size[0] *scale, size[1] *scale)
      self.color = (0, 0, 0)
      self.Font = pygame.font.SysFont(FONT, 20*scale)
      self.text : pygame.Surface = self.Font.render("Tavla", True, (255, 255, 255))
   def draw(self, screen:pygame.surface.Surface):
      self.surface = pygame.surface.Surface(self.rect.size)
      self.surface.blit(self.text, [ self.rect.centerx - self.text.__sizeof__()[0]/2, self.rect.centery - self.text.__sizeof__()[1]/2 ])
      screen.blit(self.surface, self.rect.topleft)