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

#If you are confused about some weird names, just ask Nalani

class app:
   def __init__(self):
      self.manager = Manager()
      self.font = pygame.font.SysFont("Helvetica", 15)
      self.TableTypes = {
         "Rectangular" : {
            "Vertex" : [
               (0, 0), 
               (100, 0), 
               (100, 50), 
               (0, 50)
            ],
            "Seats" : [
               {
                  "Pos" : (25, 0),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : (75, 0),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : (100, 25),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : (75, 50),
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
         },
         "Trapezoid" : {
            "Vertex" : [
               (50, 0), 
               (150, 0),
               (200, 100), 
               (0, 100)
            ],
            "Seats" : [
               {
                  "Pos" : (100, 0),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : (50, 100),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : (150, 100),
                  "Occupied" : -1
               }
            ]
         }
      }
      self.Room = self.getScene()
      self.mouseHolding = [None, ""]
      self.mouseSelected = None
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
      self.screen  = {
         "Viewport" : pygame.display.set_mode((700, 700), vsync=1),
         "Room" : pygame.Surface((700, 700))
         }
      

      self.RoomPos = (0, 0)
      self.Event = pygame.event.get()
      self.running = True
      

#Main Functions
   def Felicia(self): # Formaly known as event

      self.Event = pygame.event.get()

      for event in self.Event:

         if event.type == pygame.QUIT:

            self.running = False


   def Morot(self): # Formaly known as Update

      pygame.mouse.set_cursor(self.cursorIMG)
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
      mousePos = getRoomCursorPos(self.RoomPos)

      self.mouseHolding = self.getHolding()   

      if self.mouseHolding[0] != None:
         
         transform : TransformComponent = self.manager.getComponent(self.mouseHolding[0], TransformComponent)
         match self.mouseHolding[1]:
            case "Normal":   
               transform.rect.center = mousePos

               if self.manager.hasComponent(self.mouseHolding[0], SnapComponent): 
                  self.handleSnap(self.mouseHolding[0])

               #If the object has seats
               if self.manager.hasComponent(self.mouseHolding[0], SeatComponent):
                  
                  for seat in self.manager.getComponent(self.mouseHolding[0], SeatComponent).getViewportRelativeSeats(transform.getScale(), transform.rect):
                     
                     #If seat is not empty
                     if seat["Occupied"] != -1:

                        #Move occupant to new position
                        occuRect = self.manager.getComponent(seat["Occupied"], TransformComponent).rect
                        occuRect.center = seat["Pos"]


            case "Edge":
               transform.rect.size = [max(mousePos[0] - transform.rect.x, 25), max(mousePos[1] - transform.rect.y, 25)]
               
               if self.manager.hasComponent(self.mouseHolding[0], CollisionComponent):
               
                  Collision = self.manager.getComponent(self.mouseHolding[0], CollisionComponent)

                  if Collision.negativeEdge != None:

                     Collision.negativeEdge.size = [ transform.rect.width - 10, transform.rect.height - 10 ]
               
               #If the object has seats
               if self.manager.hasComponent(self.mouseHolding[0], SeatComponent):
                  
                  for seat in self.manager.getComponent(self.mouseHolding[0], SeatComponent).getViewportRelativeSeats(transform.getScale(), transform.rect):
                     
                     #If seat is not empty
                     if seat["Occupied"] != -1:

                        #Move occupant to new position
                        occuRect = self.manager.getComponent(seat["Occupied"], TransformComponent).rect
                        occuRect.center = seat["Pos"]


      self.mouseSelected = self.getSelected()

      if self.mouseSelected != None:

         r = self.manager.changeName(self.mouseSelected, self.Event)


         #If Selected Object is snapped to another object it should still be centered on it
         if self.manager.hasComponent(self.mouseSelected, SnapComponent):

            #Get Snap Component
            Snap = self.manager.getComponent(self.mouseSelected, SnapComponent)

            #Get Transform of EntID
            transform = self.manager.getComponent(self.mouseSelected, TransformComponent)
            
            if Snap.ID[0] != None:

               #Get the Snapped to objects rect and seats
               SnappedTransform : TransformComponent = self.manager.getComponent(Snap.ID[0], TransformComponent)

               SeatComp : SeatComponent = self.manager.getComponent(Snap.ID[0], SeatComponent)

               Seats = SeatComp.getViewportRelativeSeats(SnappedTransform.getScale(), SnappedTransform.rect)

               transform.rect.center = Seats[Snap.ID[1]]["Pos"]

         if r == 1:

            self.mouseSelected == None

      return 

   def Groda(self): #Formaly known as Render
      self.screen["Viewport"].fill((0, 0, 0))
      self.screen["Room"].fill((255, 255, 255))

      #draw

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
   

   def createTable(self, type, Rect):

      t = self.manager.newEntity()
      
      rect = pygame.draw.polygon(pygame.Surface((10000, 10000)), (0, 0, 0), self.TableTypes[type]["Vertex"])
      rect.topleft = Rect.topleft
      self.manager.newComponent(t, TransformComponent, rect)
      self.manager.newComponent(t, VertexComponent, self.TableTypes[type]["Vertex"])

      self.manager.newComponent(t, SeatComponent, self.TableTypes[type]["Seats"])
      rect2 = pygame.Rect(rect.topleft, rect.size)
      rect2.size = [rect.width - 10, rect.height - 10]

      self.manager.newComponent(t, CollisionComponent, pygame.Mask(rect.size), rect2)     
      self.manager.newComponent(t, SnapComponent)

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
         self.createTable("Trapezoid", rect)
         
      return self.Room

   def handleSnap(self, EntID):

      #Get Snap Component
      Snap = self.manager.getComponent(EntID, SnapComponent)

      #Get Transform of EntID
      transform = self.manager.getComponent(EntID, TransformComponent)
      
      if Snap.ID[0] != None:

         #Get the Snapped to objects rect and seats
         SnappedTransform : TransformComponent = self.manager.getComponent(Snap.ID[0], TransformComponent)

         SeatComp : SeatComponent = self.manager.getComponent(Snap.ID[0], SeatComponent)

         Seats = SeatComp.getViewportRelativeSeats(SnappedTransform.getScale(), SnappedTransform.rect)

         #If not touching the seat anymore
         if not mouseCollision(Seats[Snap.ID[1]]["Pos"], transform.rect):

            #Leave seat
            Seats[Snap.ID[1]]["Occupied"] = -1
            
            Snap.ID = (None, -1)

         else:

            transform.rect.center = Seats[Snap.ID[1]]["Pos"]

            Seats[Snap.ID[1]]["Occupied"] = self.mouseHolding[0]
            
         SeatComp.returnViewportRelativeSeats(SnappedTransform.getScale(), SnappedTransform.rect, Seats)

         return

      else:
         
         for table in self.Room["Tables"]:
            
            if not self.manager.hasComponent(table, SeatComponent):
               continue
               
            TableTransform : TransformComponent = self.manager.getComponent(table, TransformComponent)
            SeatComp : SeatComponent = self.manager.getComponent(table, SeatComponent)
            seats : list = SeatComp.getViewportRelativeSeats(TableTransform.getScale(), TableTransform.rect)
            
            for x in range(0, len(seats)):

               if mouseCollision(seats[x]["Pos"], transform.rect) and seats[x]["Occupied"] == -1 and self.mouseHolding[0] != table:

                  Snap.ID = [table, x]

                  seats[x]["Occupied"] = self.mouseHolding[0]

                  SeatComp.returnViewportRelativeSeats(TableTransform.getScale(), TableTransform.rect, seats)

                  return


def NalaniÄrBäst(): #Formaly known as Main

   App = app()
   
   while App.running:

      App.Felicia() #Formaly known as Event
      
      App.Morot() #Formaly known as Update

      App.Groda() #Formaly known as Render

      pygame.display.update()
      pygame.time.Clock().tick(60)

NalaniÄrBäst()