import pygame
import math

def mouseCollision(A, B:pygame.Rect):
    return (A[0] >= B.x and A[0] < B.x + B.width) and (A[1] >= B.y and A[1] < B.y + B.height)


def getTextEvent(text:str, Event):
   for event in Event:
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_RETURN:
            return 0
         elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
         else:
            text += event.unicode
   return text

class Entity:
   def __init__(self):
      self.Component = {}


class TransformComponent:
   def __init__(self, rect, Master=True):
      self.rect = rect
      self.isMaster = Master
   
class SpriteComponent:
   def __init__(self, color, radius=10, outlineColor=(0, 0, 0), outlineWidth=0):
      self.outlineAttributes = {
         "width" : outlineWidth,
         "radius" : radius,
         "color" : outlineColor
      }
      self.bodyAttributes = {
         "color" : color,
         "radius" : radius
      }

class CollisionComponent:
   def __init__(self, mask, negativeEdge:pygame.Rect=None):
      self.mask : pygame.Mask = mask
      self.negativeEdge = negativeEdge

class TextComponent:
   def __init__(self, Text:str, Color: tuple, Font:pygame.font.Font):
      self.Text = Text
      self.Color = Color
      self.Font = Font
      self.textReleave = 10
      self.Sprite = self.Font.render(self.Text, True, self.Color)
      self.rect = self.Sprite.get_rect()


class Manager:
   def __init__(self):
      self.Entitys = []

   #Main functions
   def newComponent(self, EntID: int, type, *args):
      
      T = type(*args)
      
      self.Entitys[EntID].Component[str(type)] = T

   def getComponent(self, EntID, type):
      return self.Entitys[EntID].Component[str(type)]
   
   def hasComponent(self, EntID, type):
      return str(type) in self.Entitys[EntID].Component
   
   def newEntity(self):

      ent = Entity()
      
      for slot in self.Entitys:
      
         if slot == None:
      
            slot = ent
      
            return self.Entitys.index(ent)

      self.Entitys.append(ent)
            
      return self.Entitys.index(ent)

   def delEntity(self, EntID):
      self.Entitys[EntID] = None
      return 0


   #System functions
   def CheckCollision(self, Ent, mousePos) -> tuple:

      if not self.hasComponent(Ent, TransformComponent):
         return 0
      
      transform = self.getComponent(Ent, TransformComponent)

      if mouseCollision(mousePos, transform.rect):
         
         if not self.hasComponent(Ent, CollisionComponent):
            return True, "Normal"

         collision : CollisionComponent = self.getComponent(Ent, CollisionComponent)

         maskPos = [mousePos[0] - transform.rect.x, mousePos[1] - transform.rect.y]

         if collision.mask.get_at(maskPos):

            if collision.negativeEdge == None:

               return True, "Normal"

            if mouseCollision(mousePos, collision.negativeEdge):
     
               return True, "Normal"
      
            return True, "Edge"
      
      return False, ""


   def draw(self, Ent, screen):

      #get Components
      if not self.hasComponent(Ent, TransformComponent):
         self.newComponent(Ent, TransformComponent, pygame.Rect(100, 100, 50, 50))
      transform = self.getComponent(Ent, TransformComponent)

      if not self.hasComponent(Ent, SpriteComponent):
         self.newComponent(Ent, SpriteComponent, (0, 0, 0))
      sprite = self.getComponent(Ent, SpriteComponent)

      
      #Prepares surface
      surface = pygame.Surface(transform.rect.size).convert_alpha()
      surface.fill((0, 0, 0, 0))   
      rect = surface.get_rect()


      #Draws main body
      pygame.draw.rect(surface, sprite.bodyAttributes["color"], rect, border_radius=sprite.bodyAttributes["radius"])

      pygame.draw.rect(surface, sprite.outlineAttributes["color"], rect, sprite.outlineAttributes["width"], sprite.outlineAttributes["radius"])
      

      #Draws Text if object has text
      if self.hasComponent(Ent, TextComponent):
         text = self.getComponent(Ent, TextComponent)
         
         surface.blit(text.Sprite, [rect.centerx - text.rect.width/2, rect.centery - text.rect.height/2])


      #If Obejct has a Collision mask it updates it now
      if self.hasComponent(Ent, CollisionComponent):
         Collision = self.getComponent(Ent, CollisionComponent)

         Collision.mask = pygame.mask.from_surface(surface)


      #Finaly draws object on screen
      screen.blit(surface, transform.rect)


def changeName(manager: Manager, Ent, Event):

   #Returns if object doesn't have a TextComponent
   if not manager.hasComponent(Ent, TextComponent):
      return -1
   
   #Gets component
   textComp:TextComponent  = manager.getComponent(Ent, TextComponent)
   
   #Gets changes in text from events
   text = getTextEvent(textComp.Text, Event)

   #Checks if end signal got returned
   if text == 0:
      return 1

   #Sets the objects text to the new one
   textComp.Text = text

   #Renders the text and creates the rect around the render
   textComp.Sprite = textComp.Font.render(textComp.Text, True, textComp.Color)
   textComp.rect = textComp.Sprite.get_rect()

   #Makes TransformComponent if object lack it
   if not manager.hasComponent(Ent, TransformComponent):
      manager.newComponent(Ent, TransformComponent, textComp.rect)
   
   #If transform component is not considerd master the text width changes the objects width
   transform : TransformComponent= manager.getComponent(Ent, TransformComponent)
   if transform.isMaster:
      transform.rect.width = max(transform.rect.width, textComp.rect.width + 2*textComp.textReleave)
   else:
      transform.rect.width = textComp.rect.width + 2*textComp.textReleave

   return 0