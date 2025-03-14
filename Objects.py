import pygame, math
from GeneralFuntions import *

class Table:

   def __init__(self, type:str, pos, size, seats=[], scale=1):
      self.type = type

      self.rect = pygame.Rect(pos[0], pos[1], size[0], size[0])

      self.color = (0, 0, 0)

      #It's a Function pointer!
      #Function that will be created depending on the type of tabel when it's created
      #Will return boolean depending on if the mouse if above the table or not 
      #Inputs are the position of the cursor as a tuple of length 2 
      self.hitboxFunc = None

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

   def changeSize(self, pos):
      self.rect = pygame.Rect(self.rect.x, 
                              self.rect.y,
                              pos[0] - self.rect.x,
                              pos[1] - self.rect.y
                              )

   def draw(self, screen : pygame.Surface):

      match self.type:

         case "Round":
            pygame.draw.circle(screen, self.color, self.rect.center, self.rect.width)

         case "Rectangular":
            pygame.draw.rect(screen, self.color, self.rect)
   
   def getMouseTouching(self, pos) :
      return self.hitboxFunc(pos, self)


class Person:

   def __init__(self, pos, text, FONT, scale):

      #Color
      self.color = {
         "Main" : (150, 150, 150),
         "Outline" : (0, 0, 0),
         "Text" : (0, 0, 0),
         "Selected" : (60, 60, 232)
      }

      #Text
      self.text : str = text
      self.FontSize = 14 *scale["Font"]["People"]
      self.Font : pygame.font.Font = pygame.font.SysFont(FONT, self.FontSize)
      self.name : pygame.Surface = self.Font.render(text, True, self.color["Text"]).convert_alpha()
      
      #Outline
      self.outlineWidth = 2*scale["People"]      
      self.outlineRadius : float = 10* scale["People"]

      #Rect
      self.rect = pygame.Rect(0, 0, self.name.get_size()[0] + 10*scale["People"], self.name.get_size()[1] + 10*scale["People"])
      self.rect.center = pos

      #Selected
      self.selected = False


   def draw(self, screen:pygame.Surface):   

      surface = pygame.surface.Surface(self.rect.size).convert_alpha()
      surface.fill((0, 0, 0, 0))

      r = surface.get_rect()

      #Changes Main color when selected            
      if self.selected:
         c = self.color["Selected"]
      else:
         c = self.color["Main"]
      #Main Rect 
      pygame.draw.rect(surface,                          #Surface
                       c,                                #Color
                       r,                                #Pos and Size / rect
                       border_radius=self.outlineRadius  #Radius of corners
                       )
      

      #Rect Outline 
      pygame.draw.rect(surface,                          #Surface
                       self.color["Outline"],            #Color
                       r,                                #Pos and Size / rect
                       self.outlineWidth,                #Width of outline
                       self.outlineRadius                #Radius of corners 
                       )

      surface.blit(self.name, 
                   [ 
                     r.centerx - self.name.get_size()[0]/2, #X 
                     r.centery - self.name.get_size()[1]/2  #Y
                   ]
                  )

      screen.blit(surface, self.rect)


   def changeName(self, text:str, scale):

      self.text = text

      self.name : pygame.Surface = self.Font.render(text, True, self.color["Text"]).convert_alpha()

      self.rect = pygame.Rect(self.rect.x, self.rect.y, self.name.get_size()[0] + 10*scale["People"], self.name.get_size()[1] + 10*scale["People"])



class Tavla:

   def __init__(self, pos, size, FONT, scale=1):
      self.rect = pygame.Rect(pos[0] *scale, pos[1] *scale, size[0] *scale, size[1] *scale)

      self.color = (0, 0, 0)

      self.EdgeWidth = 10*scale

      self.FontSize = 20*scale
      self.Font = pygame.font.SysFont(FONT, self.FontSize)
      self.text : pygame.Surface = self.Font.render("Tavla", True, (255, 255, 255))

   def getMouseTouching(self, pos):
      if mouseCollision(pos, self.rect):
         if not mouseCollision(pos, pygame.Rect( self.rect.topleft, ( self.rect.width - self.EdgeWidth, self.rect.height - self.EdgeWidth ) ) ):
            return True, "Edge"
         return True, "Normal"
      return False, ""

   def draw(self, screen:pygame.surface.Surface):
      self.surface = pygame.surface.Surface(self.rect.size)
      self.surface.fill(self.color)

      self.surface.blit(self.text, [ self.surface.get_size()[0]/2 - self.text.get_size()[0]/2, self.surface.get_size()[1]/2 - self.text.get_size()[1]/2 ])

      screen.blit(self.surface, self.rect.topleft)