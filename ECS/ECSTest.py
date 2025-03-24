from Component import *


pygame.init()


def getCenter(surface:pygame.Surface):
   return (surface.get_width()/2, surface.get_height()/2)

def getRoomCursorPos(RoomTopLeft):
   return (
      pygame.mouse.get_pos()[0] - RoomTopLeft[0],
      pygame.mouse.get_pos()[1] - RoomTopLeft[1]

   )

def mouseCollision(A, B:pygame.Rect):
    return (A[0] >= B.x and A[0] <= B.x + B.width) and (A[1] >= B.y and A[1] <= B.y + B.height)

class app:
   def __init__(self):
      self.manager = Manager()
      self.font = pygame.font.SysFont("Helvetica", 20)
      self.Room = self.getScene()
      self.mouseHolding = [None, ""]
      self.mouseSelected = None
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
      self.screen  = {
         "Viewport" : pygame.display.set_mode((700, 700), vsync=1),
         "Room" : pygame.Surface((500, 500))
         }
      self.RoomPos = (0, 0)
      self.Event = pygame.event.get()
      self.running = True
      
      
      self.debugObj = self.manager.newEntity()
      self.manager.newComponent(self.debugObj, TransformComponent, pygame.Rect(200, 200, 100, 100))
      self.manager.newComponent(self.debugObj, VertexComponent, [(0, 0), (50, 0), (25, 25), (50, 50), (0, 50)], 1)

      seats = [
         {
            "Pos" : (25, 0),
            "Occupied" : -1
         },
         {
            "Pos" : (25, 25),
            "Occupied" : -1
         },
         {
            "Pos" : (25, 50),
            "Occupied" : -1
         },
         {
            "Pos" : (0, 25),
            "Occupied" : -1
         }
      ]

      self.manager.newComponent(self.debugObj, SeatComponent, seats, 2)


#Main Functions
   def event(self):

      self.Event = pygame.event.get()

      for event in self.Event:

         if event.type == pygame.QUIT:

            self.running = False


   def Update(self):

      pygame.mouse.set_cursor(self.cursorIMG)
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
      mousePos = getRoomCursorPos(self.RoomPos)

      self.mouseHolding = self.getHolding()   

      if self.mouseHolding[0] != None:
         
         transform = self.manager.getComponent(self.mouseHolding[0], TransformComponent)
         match self.mouseHolding[1]:
            case "Normal":

               transform.rect.center = mousePos

               DebugObjRect = self.manager.getComponent(self.debugObj, TransformComponent).rect
               seats = self.manager.getComponent(self.debugObj, SeatComponent).getViewportRelativeSeats(2, DebugObjRect)
               
               Snap = self.manager.getComponent(self.mouseHolding[0], SnapComponent)
               print(seats)

               if Snap.ID[0] != None:

                  Rect = self.manager.getComponent(Snap.ID[0], TransformComponent).rect
                  Seats = self.manager.getComponent(Snap.ID[0], SeatComponent).getViewportRelativeSeats(2, Rect)
                  
                  if not mouseCollision(Seats[Snap.ID[1]]["Pos"], transform.rect):
                     Seats[Snap.ID[1]]["Occupied"] = -1
                     Snap.ID = (None, -1)

                  else:
                     transform.rect.center = Seats[Snap.ID[1]]["Pos"]

                     Seats[Snap.ID[1]]["Occupied"] = self.mouseHolding[0]
               
               else:
                  
                  for x in range(0, len(seats)):
                     if mouseCollision(seats[x]["Pos"], transform.rect) and seats[x]["Occupied"] == -1:
                        Snap.ID = [self.debugObj, x]
                        seats[x]["Occupied"] = self.mouseHolding[0]


            case "Edge":
               transform.rect.size = [max(mousePos[0] - transform.rect.x, 25), max(mousePos[1] - transform.rect.y, 25)]
               
               if self.manager.hasComponent(self.mouseHolding[0], CollisionComponent):
               
                  Collision = self.manager.getComponent(self.mouseHolding[0], CollisionComponent)

                  if Collision.negativeEdge != None:

                     Collision.negativeEdge.size = [ transform.rect.width - 10, transform.rect.height - 10 ]


      self.mouseSelected = self.getSelected()

      if self.mouseSelected != None:

         r = self.manager.changeName(self.mouseSelected, self.Event)

         if r == 1:

            self.mouseSelected == None

      return 

   def Render(self):
      self.screen["Viewport"].fill((0, 0, 0))
      self.screen["Room"].fill((255, 255, 255))

      #draw

      transform:TransformComponent = self.manager.getComponent(self.debugObj, TransformComponent)
      Vertex = self.manager.getComponent(self.debugObj, VertexComponent)

      surf = pygame.Surface(transform.rect.size).convert_alpha()
      surf.fill((0, 0, 0, 0))

      pygame.draw.polygon(surf, (255, 0, 0), Vertex.getScaledVertex(2))

      self.screen["Room"].blit(surf, transform.rect)

      for Table in self.Room["Tables"]:
         self.manager.draw(Table, self.screen["Room"])

      for Person in self.Room["People"]:
         self.manager.draw(Person, self.screen["Room"])


      self.RoomPos = (
         getCenter(self.screen["Viewport"])[0] - getCenter(self.screen["Room"])[0],
         getCenter(self.screen["Viewport"])[1] - getCenter(self.screen["Room"])[1]
         )
      self.screen["Viewport"].blit(self.screen["Room"], self.RoomPos)


      return
   

#Daughter functions 
   def getHover(self) -> tuple:
      mousePos = getRoomCursorPos(self.RoomPos)

      #Moves backwards so the top most person get picked first
      for x in range(len(self.Room["People"])-1, -1, -1):
         
         result, flag = self.manager.CheckCollision(self.Room["People"][x], mousePos)
         
         if result: return self.Room["People"][x], flag

    #Moves backwards so the top most table get picked first   
      for x in range(len(self.Room["Tables"])-1, -1, -1):
   
         result, flag = self.manager.CheckCollision(self.Room["Tables"][x], (mousePos))
    
         if result:
    
             return self.Room["Tables"][x], flag 

      return None, ""
   

   def getHolding(self) -> object:

      hover = self.getHover()
      #Nice Cursor change for ease of use 
      if hover[0] != None:

         if hover[1] == "Edge":
            self.cursorIMG = pygame.SYSTEM_CURSOR_SIZENWSE

         else:
            self.cursorIMG = pygame.SYSTEM_CURSOR_SIZEALL      
      
      #Left mouse button
      if not pygame.mouse.get_pressed()[0]:
         return None, ""
      
      #If already holding something
      if self.mouseHolding[0] != None:

         if self.mouseHolding[1] == "Edge":
            self.cursorIMG = pygame.SYSTEM_CURSOR_SIZENWSE
         else:
            self.cursorIMG = pygame.SYSTEM_CURSOR_SIZEALL      

         return self.mouseHolding

      return hover


   def getSelected(self) -> object:

      #Deselects if left mouse button is pressed
      if pygame.mouse.get_pressed()[0]:
         return None
      
      #If something already selected
      if self.mouseSelected != None:
         return self.mouseSelected

      #Select if right mouse button is pressed
      if pygame.mouse.get_pressed()[2]:
         return self.getHover()[0]


   def createPerson(self, rect, text=""):

      t = self.manager.newEntity()
      
      self.manager.newComponent(t, TransformComponent, rect, False)
      
      self.manager.newComponent(t, SpriteComponent, (255, 255, 255), 10, (0, 0, 0), 2)
      
      self.manager.newComponent(t, TextComponent, text, (0, 0, 0), self.font)

      self.manager.newComponent(t, SnapComponent, False, [None, -1])
      
      self.Room["People"].append(t)
   

   def createTable(self, rect):

      t = self.manager.newEntity()

      self.manager.newComponent(t, TransformComponent, rect, True)

      self.manager.newComponent(t, SpriteComponent, (0, 0, 0), 10)

      rect2 = pygame.Rect(rect.topleft, rect.size)
      rect2.size = [rect.width - 10, rect.height - 10]

      self.manager.newComponent(t, CollisionComponent, pygame.Mask(rect.size), rect2)

      self.manager.newComponent(t, SnapComponent, False, [None, -1])

      self.Room["Tables"].append(t)



   def getScene(self):
      #Placeholder function
      
      self.Room = {
         "People" : [],
         "Tables" : []
      }

      for i in range (0, 5):   

         rect = pygame.Rect(100*i, 100, 50,  25)        
         self.createPerson(rect)         

      for i in range(0, 2):

         rect = pygame.Rect(150*i, 200, 50, 100)
         self.createTable(rect)
         
      return self.Room


   
App = app()
while App.running:

   App.event()
   
   App.Update()

   App.Render()

   pygame.display.update()
   pygame.time.Clock().tick(60)