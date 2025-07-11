import pygame
import math


class Vertices:
   def __init__(self, Vertices):

      self._Vertices = []

      for Vertex in Vertices:
         
         if type(Vertex) != pygame.Vector2:
            Vertex = pygame.Vector2(Vertex)

         self._Vertices.append(Vertex.as_polar())

   @property
   def Vertices(self):
      
      V = []
      for Vertex in self._Vertices:
         
         V.append(pygame.Vector2.from_polar(Vertex))

      return V
   
   @property
   def PolarVertices(self):
      return self._Vertices
   
   @Vertices.setter
   def Vertices(self, new_Vertices):

      for Vertex in new_Vertices:
         
         if type(Vertex) != pygame.Vector2:
            Vertex = pygame.Vector2(Vertex)

         self._Vertices.append(Vertex.as_polar())

   @Vertices.setter
   def PolarVertices(self, new_Vertices):
      
      self._Vertices = new_Vertices

   def __str__(self):
      string = "Vertices : {\n"

      for Vertex in self.Vertices:

         string += "   " + str(Vertex.xy)  

         if Vertex != self.Vertices[-1]:
            string += ",\n"
      
      string += "\n}"

      return string

   def __eq__(self, value):

      if isinstance(value, (list, tuple)):
         
         if len(value[0]) == 2: value = Vertices(value)
            
         else: return False
         
      if not isinstance(value, Vertices):
         return False


      if isinstance(self, (list, tuple)):
         
         if len(self[0]) == 2: self = Vertices(self)
            
         else: return False
         
      if not isinstance(self, Vertices): return False

      
      if len(self.Vertices) != len(value.Vertices): return False
      
      for x in range(0, len(self.Vertices)-1):
         
         if self.Vertices[x] != value.Vertices[x]:
         
            return False
      
      return True
   
V = Vertices([(0, 0), (60, 0), (100, 25), (50, 25)])
print(V)