import pygame
import math
from multipledispatch import dispatch

class angularPosition:

    def __init__(self, angle, radius):
        self.angle = angle
        self.radius = radius

@dispatch(float, float)
def AngularToLinearPosition(angle, radius) -> pygame.Vector2:

    pos = pygame.Vector2(0, 0)

    pos.x = math.cos(math.radians(angle))*radius
    pos.y = math.sin(math.radians(angle))*radius

    return pos

@dispatch(float, int)
def AngularToLinearPosition(angle, radius) -> pygame.Vector2:

    pos = pygame.Vector2(0, 0)

    pos.x = math.cos(math.radians(angle))*radius
    pos.y = -math.sin(math.radians(angle))*radius

    return pos

@dispatch(angularPosition)
def AngularToLinearPosition(angularPos : angularPosition) -> pygame.Vector2:

    pos = pygame.Vector2(0, 0)

    pos.x = math.cos(math.radians(angularPos.angle))*angularPos.radius
    pos.y = -math.sin(math.radians(angularPos.angle))*angularPos.radius

    return pos

@dispatch(tuple)
def LinearToAngluarPosition(Pos:tuple) -> angularPosition:

    Pos:list = list(Pos)
    #Don't know if this is correct math, but I hope it is 
    if Pos[0] == 0:
        Pos[0] = 0.00000001



    angle = math.degrees(math.atan(abs(Pos[1])/abs(Pos[0])))

    if Pos[0] < 0:
        angle = 180 - angle

    if Pos[1] < 0:
        angle = -angle
    

    radius = math.sqrt(Pos[0]**2 + Pos[1]**2)

    return angularPosition(angle, radius)

@dispatch(pygame.Vector2)
def LinearToAngluarPosition(Pos:pygame.Vector2) -> angularPosition:
    
    if Pos.x == 0:
        Pos.x = 0.00000001
    #Don't know if this is correct math, but I hope it is 


    angle = math.degrees(math.atan(abs(Pos.y)/abs(Pos.x)))

    if Pos.x < 0:
        angle = 180 - angle

    if Pos.y < 0:
        angle = -angle


    radius = math.sqrt(Pos.x**2 + Pos.y**2)

    return angularPosition(angle, radius)

def pointCollision(A : pygame.Vector2, B:pygame.Rect):
    return (A.x >= B.x and A.x < B.x + B.width) and (A.y >= B.y and A.y < B.y + B.height)

def distance(A : pygame.Vector2, B : pygame.Vector2):
   return math.sqrt((A.x - B.x)**2 + (A.x - B.x)**2)

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
      self.rect :pygame.Rect= rect
      self.angle = 45
      self.scale = 1
      self.isMaster = Master
   def getScale(self) -> tuple:
      return self.scale
   
class SpriteComponent:
   def __init__(self, color, radius=10, outlineColor=(0, 0, 0), outlineWidth=0):
      
      self.bodyAttributes = {
         "color" : color,
         "radius" : radius
      }
      
      self.outlineAttributes = {
         "width" : outlineWidth,
         "radius" : radius,
         "color" : outlineColor
      }


class VertexComponent:
   def __init__(self, Vertices):
      self.Vertices = Vertices

   def getScaledVertices(self, scale):

      scaledVertices = []

      for pos in self.Vertices:
         scaledVertices.append(pygame.Vector2(pos.x*scale, pos.y*scale))
      
      return scaledVertices
   
   def getViewportRelativeScaledAndRotatedVertices(self, scale, angle, rect):
      
      rect:pygame.Rect
      Vertices = []

      for pos in self.Vertices:
         Vertices.append(pygame.Vector2(pos.x*scale, pos.y*scale).rotate(angle) + rect.topleft)
      
      return Vertices
   
   def getScaledAndRotatedVertices(self, scale, angle):
      
      rect:pygame.Rect
      Vertices = []
      smallestPos = pygame.Vector2(0, 0)

      for vertex in self.Vertices:
         
         pos = pygame.Vector2(vertex.x*scale, vertex.y*scale).rotate(angle)
         
         Vertices.append(pos)

         if pos.x < smallestPos.x:
            smallestPos.x = pos.x
         
         if pos.y < smallestPos.y:
            smallestPos.y = pos.y

      for vertex in Vertices:
         vertex.x -= smallestPos.x
         vertex.y -= smallestPos.y
      
      return Vertices

   def getScaledAndRotatedSize(self, scale, angle):
      
      rect:pygame.Rect
      Vertices = []
      smallestPos = pygame.Vector2(0, 0)
      biggestPos = pygame.Vector2(0, 0)

      for vertex in self.Vertices:
         
         pos = pygame.Vector2(vertex.x*scale, vertex.y*scale).rotate(angle)

         if pos.x < smallestPos.x:
            smallestPos.x = pos.x
         
         if pos.y < smallestPos.y:
            smallestPos.y = pos.y
         
         if pos.x > biggestPos.x:
            biggestPos.x = pos.x
         
         if pos.y > biggestPos.y:
            biggestPos.y = pos.y
      
      return pygame.Vector2(biggestPos.x - smallestPos.x, biggestPos.y - smallestPos.y)
   
   def getRotatedSize(self, angle):
      
      rect:pygame.Rect
      Vertices = []
      smallestPos = pygame.Vector2(0, 0)
      biggestPos = pygame.Vector2(0, 0)

      for vertex in self.Vertices:
         
         pos = pygame.Vector2(vertex.x, vertex.y).rotate(angle)

         if pos.x < smallestPos.x:
            smallestPos.x = pos.x
         
         if pos.y < smallestPos.y:
            smallestPos.y = pos.y
         
         if pos.x > biggestPos.x:
            biggestPos.x = pos.x
         
         if pos.y > biggestPos.y:
            biggestPos.y = pos.y
      
      return pygame.Vector2(biggestPos.x - smallestPos.x, biggestPos.y - smallestPos.y)

   def getViewportRelativeVertices(self, scale, rect):
      relativeVertices = []

      for pos in self.Vertices:
         relativeVertices.append(pygame.Vector2(pos.x*scale+rect.x, pos.y*scale+rect.y))

      return relativeVertices

class CollisionComponent:
   def __init__(self, mask, negativeEdge:pygame.Rect=None):
      self.mask : pygame.Mask = mask
      self.negativeEdge = negativeEdge

class TextComponent:
   def __init__(self, Text:str, Color: tuple, Font:pygame.font.Font):
      self.Text = Text
      self.Color = Color
      self.Font = Font
      self.textReleave = 5
      self.Sprite = self.Font.render(self.Text, True, self.Color)
      self.rect = self.Sprite.get_rect()


class SeatComponent:
   def __init__(self, seats:list):
      self.Seats = seats

   def getViewportRelativeSeats(self, scale, Rect):

      self.scaledSeats = []

      for seat in self.Seats:
         self.scaledSeats.append(
            {
            "Pos": pygame.Vector2((seat["Pos"].x * scale) + Rect.x, (seat["Pos"].y * scale) + Rect.y), 
            "Occupied" : seat["Occupied"]
            })
      
      return self.scaledSeats

   def returnViewportRelativeSeats(self, scale, Rect, Seats):

      self.Seats = []
      for seat in Seats:
         self.Seats.append(
            {
            "Pos" : pygame.Vector2((seat["Pos"].x - Rect.x) / scale, (seat["Pos"].y - Rect.y) / scale),
            "Occupied" : seat["Occupied"]
            }
         )

      return 
   def getScaledSeats(self, scale):

      self.scaledSeats = []

      for seat in self.Seats:
         self.scaledSeats.append(
            {
            "Pos": (seat["Pos"].x*scale.x, seat["Pos"].y*scale.y), 
            "Occupied" : seat["Occupied"]
            })
      
      return self.scaledSeats

class ListEntitysComponent:
   def __init__(self, List, Type):
      
      self.List = List
      self.Type = Type

   def Remove(self, manager):
      for Ent in self.List:
         manager.delEntity(Ent)
      self.List = []
      self.Type = ""
         
         


class Manager:
   def __init__(self):
      self.Entitys = []

   #Main functions
   def newComponent(self, EntID: int, type, *args):
      if self.hasComponent(EntID, type):
         return

      T = type(*args)
      
      self.Entitys[EntID].Component[str(type)] = T

      return
   def getComponent(self, EntID, type:object) -> object:
      return self.Entitys[EntID].Component[str(type)]
   
   def hasComponent(self, EntID, type) -> bool:
      return str(type) in self.Entitys[EntID].Component
   
   def newEntity(self) -> int:

      ent = Entity()
      
      for slot in self.Entitys:
      
         if slot == None:
      
            slot = ent
      
            return self.Entitys.index(ent)

      self.Entitys.append(ent)
            
      return self.Entitys.index(ent)

   def delEntity(self, EntID):
      
      if self.hasComponent(EntID, ListEntitysComponent):
      
         listComp = self.getComponent(EntID, ListEntitysComponent)
         listComp.Remove()

      self.Entitys[EntID] = None
      return 0


   #System functions
   def CheckCollision(self, Ent, mousePos) -> tuple:

      if not self.hasComponent(Ent, TransformComponent):
         return 0, ""
      
      transform = self.getComponent(Ent, TransformComponent)

      if pointCollision(mousePos, transform.rect):
         
         if not self.hasComponent(Ent, CollisionComponent):
            return True, "Normal"

         collision : CollisionComponent = self.getComponent(Ent, CollisionComponent)

         maskPos = [mousePos[0] - transform.rect.x, mousePos[1] - transform.rect.y]

         if collision.mask.get_at(maskPos):

            if collision.negativeEdge == None:

               return True, "Normal"
            
            collision.negativeEdge.topleft = transform.rect.topleft

            if pointCollision(mousePos, collision.negativeEdge):
     
               return True, "Normal"
      
            return True, "Edge"
      
      return False, ""


   def draw(self, Ent, screen):

      #get Components
      if not self.hasComponent(Ent, TransformComponent):
         self.newComponent(Ent, TransformComponent, pygame.Rect(100, 100, 50, 50))
      transform : TransformComponent = self.getComponent(Ent, TransformComponent)

      if not self.hasComponent(Ent, SpriteComponent):
         self.newComponent(Ent, SpriteComponent, (0, 0, 0))
      sprite : SpriteComponent = self.getComponent(Ent, SpriteComponent)

      
      #Prepares surface
      surface = pygame.Surface(transform.rect.size).convert_alpha()
      surface.fill((0, 0, 0, 0))
      scale = transform.getScale()
      rect = surface.get_rect()


      if self.hasComponent(Ent, VertexComponent):
         Vertex : VertexComponent = self.getComponent(Ent, VertexComponent)

         pygame.draw.polygon(surface, (0, 0, 0), Vertex.getScaledAndRotatedVertices(transform.getScale(), transform.angle))

         transform.rect.size = Vertex.getScaledAndRotatedSize(scale, transform.angle)


      else:
         #Draws main body
         pygame.draw.rect(surface, sprite.bodyAttributes["color"], rect, border_radius=sprite.bodyAttributes["radius"])

         pygame.draw.rect(surface, sprite.outlineAttributes["color"], rect, sprite.outlineAttributes["width"], sprite.outlineAttributes["radius"])
         

      #Draws Text if object has text
      if self.hasComponent(Ent, TextComponent):
         text = self.getComponent(Ent, TextComponent)
         
         surface.blit(text.Sprite, [rect.centerx - text.rect.width/2, rect.centery - text.rect.height/2])


      #If Object has a Collision mask it updates it now
      if self.hasComponent(Ent, CollisionComponent):
         Collision = self.getComponent(Ent, CollisionComponent)

         Collision.mask = pygame.mask.from_surface(surface)


      #Finaly draws object on screen
      screen.blit(surface, transform.rect)

   def SnapSeated(self, table):

      transform : TransformComponent = self.getComponent(table, TransformComponent)

      for seat in self.getComponent(table, SeatComponent).getViewportRelativeSeats(transform.getScale(), transform.rect):
         
         #If seat is not empty
         if seat["Occupied"] != -1:

            #Move occupant to new position
            occuRect = self.getComponent(seat["Occupied"], TransformComponent).rect
            occuRect.center = seat["Pos"]

   def changeName(self, Ent, Event):

      #Returns if object doesn't have a TextComponent
      if not self.hasComponent(Ent, TextComponent):
         return -1
      
      #Gets component
      textComp:TextComponent  = self.getComponent(Ent, TextComponent)
      
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
      if not self.hasComponent(Ent, TransformComponent):
         self.newComponent(Ent, TransformComponent, textComp.rect)
      
      #If transform component is not considerd master the text width changes the objects width
      transform : TransformComponent= self.getComponent(Ent, TransformComponent)
      if transform.isMaster:
         transform.rect.width = max(transform.rect.width, textComp.rect.width + 2*textComp.textReleave)
      else:
         transform.rect.width = textComp.rect.width + 2*textComp.textReleave

      return 0

   