import pygame
import math

class Entity:
   def __init__(self):
      self.Component = {}


class TransformComponent:
   def __init__(self, rect):
      self.rect = rect
   
class TextComponent:
   def __init__(self, Text:str, Color: tuple, Font:pygame.font.Font):
      self.Text = Text
      self.Color = Color
      self.Font = Font
      self.Sprite = self.Font.render(self.Text, True, self.Color)
      self.rect = self.Sprite.get_rect()


class Manager:
   def __init__(self):
      self.Components = []
      self.Entitys = []

   def newComponent(self, EntID: int, type, *args):
      
      T = type(*args)

      self.Components.append(T)
      
      self.Entitys[EntID].Component[str(type)] = self.Components.index(T)

   def getComponent(self, EntID, type):
      id = self.Entitys[EntID].Component[str(type)]
      return self.Components[id]
   
   def hasComponent(self, EntID, type):
      return str(type) in self.Entitys[EntID].Component
   
   def newEntity(self):
      ent = Entity()
      for slot in self.Entitys:
         if slot == None:
            slot = ent
         return self.Entitys.index(ent)
      
      self.Entitys.append(ent)
            
      self.Entitys.index(ent)

   def delEntity(self, EntID):
      self.Entitys[EntID] = None
      return 0


def draw(manager, Ent, screen):

   if not manager.hasComponent(Ent, TransformComponent):
      manager.newComponent(Ent, TransformComponent, pygame.Rect(100, 100, 50, 50))

   transform = manager.getComponent(Ent, TransformComponent)
   
   surface = pygame.Surface(transform.rect.size)
   
   rect = surface.get_rect()

   pygame.draw.rect(surface, (255, 255, 255), rect)
   
   if manager.hasComponent(Ent, TextComponent):

      text = manager.getComponent(Ent, TextComponent)
      
      surface.blit(text.Sprite, [rect.centerx - text.rect.width/2, rect.centery - text.rect.height/2])

   screen.blit(surface, transform.rect)

