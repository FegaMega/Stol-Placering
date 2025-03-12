import pygame

class Table:

   def __init__(self, type:str, pos, size, seats=[], scale=1):
      self.type = type

      self.rect = pygame.Rect(pos[0], pos[1], size[0], size[0])

      self.color = (0, 0, 0)

      #Function that will be created depending on the type of tabel when it's created
      #Will return boolean depending on if the mouse if above the table or not 
      #Inputs are the position of the cursor as a tuple of length 2 
      self.getMouseTouching = None

      # Format for seats 
      # inside the list their is a dict
      # the dict contains the relative position ("Pos") of the seat center 
      # and the index ("Taken") of the person who is sitting on the seat
      # if no-one is sitting on the seat the index is -1
      # Example
      # self.seats = [
      #    {
      #    "Pos" : (200, 50)  
      #    "Taken" : 3
      #    }
      # ] 
      self.seats = []

   def draw(self, screen: pygame.surface.Surface):

      match self.type:

         case "Round":
            pygame.draw.circle(screen, self.color, self.rect.center, self.rect.width)

         case "Rectangular":
            pygame.draw.rect(screen, self.color, self.rect)

class Person:

   def __init__(self, pos, text, FONT, scale):

      self.outlineRadius : float = 10* scale["People"]

      self.text : str = text
      self.Font : pygame.font.Font = pygame.font.SysFont(FONT, 20*scale["Font"]["People"])
      self.name : pygame.Surface = self.Font.render(text, True, (255, 255, 255, 255)).convert_alpha()

      self.rect = pygame.Rect(pos[0], pos[1], self.name.get_size()[0] + 10*scale["People"], self.name.get_size()[1] + 10*scale["People"])


   def draw(self, screen:pygame.Surface):   

      surface = pygame.surface.Surface(self.rect.size).convert_alpha()
      surface.fill((0, 0, 0, 0))
      r = surface.get_rect()

      pygame.draw.rect(surface, (0, 0, 0, 255), r, border_radius=self.outlineRadius)

      surface.blit(self.name, [ r.centerx - self.name.get_size()[0]/2, r.centery - self.name.get_size()[1]/2 ])

      screen.blit(surface, self.rect)


   def changeName(self, text:str, scale):

      self.name : pygame.Surface = self.Font.render(text, True, (255, 255, 255, 255)).convert_alpha()

      self.rect = pygame.Rect(self.rect.x, self.rect.y, self.name.get_size()[0] + 10*scale["People"], self.name.get_size()[1] + 10*scale["People"])



class Tavla:

   def __init__(self, pos, size, FONT, scale=1):
      self.rect = pygame.Rect(pos[0] *scale, pos[1] *scale, size[0] *scale, size[1] *scale)

      self.color = (0, 0, 0)

      self.Font = pygame.font.SysFont(FONT, 20*scale)
      self.text : pygame.Surface = self.Font.render("Tavla", True, (255, 255, 255))


   def draw(self, screen:pygame.surface.Surface):
      self.surface = pygame.surface.Surface(self.rect.size)

      self.surface.blit(self.text, [ self.rect.centerx - self.text.get_size()[0]/2, self.rect.centery - self.text.get_size()[1]/2 ])

      screen.blit(self.surface, self.rect.topleft)