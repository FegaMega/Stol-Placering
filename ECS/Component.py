import pygame
import math

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
      self.Master = Master
   
class SpriteComponent:
   def __init__(self, color, radius=10, outlineColor=(0, 0, 0), outlineWidth=0):
      self.outline = {
         "width" : outlineWidth,
         "radius" : radius,
         "color" : outlineColor
      }
      self.body = {
         "color" : color,
         "radius" : radius
      }


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


def draw(manager: Manager, Ent, screen):

   if not manager.hasComponent(Ent, TransformComponent):
      manager.newComponent(Ent, TransformComponent, pygame.Rect(100, 100, 50, 50))

   transform = manager.getComponent(Ent, TransformComponent)

   if not manager.hasComponent(Ent, SpriteComponent):
      manager.newComponent(Ent, SpriteComponent, (0, 0, 0))

   sprite = manager.getComponent(Ent, SpriteComponent)

   
   surface = pygame.Surface(transform.rect.size).convert_alpha()
   surface.fill((0, 0, 0, 0))   
   rect = surface.get_rect()

   pygame.draw.rect(surface, sprite.body["color"], rect, border_radius=sprite.body["radius"])

   pygame.draw.rect(surface, sprite.outline["color"], rect, sprite.outline["width"], sprite.outline["radius"])
   
   if manager.hasComponent(Ent, TextComponent):

      text = manager.getComponent(Ent, TextComponent)
      
      surface.blit(text.Sprite, [rect.centerx - text.rect.width/2, rect.centery - text.rect.height/2])

   screen.blit(surface, transform.rect)

def changeName(manager: Manager, Ent, Event):

   if not manager.hasComponent(Ent, TextComponent):
      return -1
   
   textComp:TextComponent  = manager.getComponent(Ent, TextComponent)
   
   text = getTextEvent(textComp.Text, Event)

   if text == 0:
      return 1

   textComp.Text = text

   textComp.Sprite = textComp.Font.render(textComp.Text, True, textComp.Color)
   textComp.rect = textComp.Sprite.get_rect()

   if not manager.hasComponent(Ent, TransformComponent):
      manager.newComponent(Ent, TransformComponent, textComp.rect)
   
   transform : TransformComponent= manager.getComponent(Ent, TransformComponent)
   if transform.Master:
      transform.rect.width = max(transform.rect.width, textComp.rect.width + 2*textComp.textReleave)
   else:
      transform.rect.width = textComp.rect.width + 2*textComp.textReleave

   return 0