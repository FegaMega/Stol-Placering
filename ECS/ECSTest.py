from Component import *


pygame.init()


def getCenter(surface:pygame.Surface):
   return (surface.get_width()/2, surface.get_height()/2)

def getRoomCursorPos(RoomTopLeft):
   return pygame.Vector2 (
      pygame.mouse.get_pos()[0] - RoomTopLeft[0],
      pygame.mouse.get_pos()[1] - RoomTopLeft[1]
   )

def rectCollision(A:pygame.Rect, B:pygame.Rect):
    return (A.x + A.width > B.x) and (A.x < B.x + B.width) and (A.y + A.height > B.y) and (A.y < B.y + B.height)

def pointCircleCollision(A, Bc, Bd):
    Diffrence = [Bc[0]-A.x, Bc[1]-A.y]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2

#If you are confused about some weird names, just ask Nalani

class app:
   def __init__(self):
      self.manager = Manager()
      self.font = pygame.font.SysFont("Helvetica", 15)
      self.TableTypes = {
         "Rectangular" : {
            "Vertex" : [
               pygame.Vector2(0, 0), 
               pygame.Vector2(100, 0), 
               pygame.Vector2(100, 50), 
               pygame.Vector2(0, 50)
            ],
            "Seats" : [
               {
                  "Pos" : pygame.Vector2(25, 0),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : pygame.Vector2(75, 0),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : pygame.Vector2(100, 25),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : pygame.Vector2(75, 50),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : pygame.Vector2(25, 50),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : pygame.Vector2(0, 25),
                  "Occupied" : -1
               }
            ]
         },
         "Trapezoid" : {
            "Vertex" : [
               pygame.Vector2(50, 0), 
               pygame.Vector2(150, 0),
               pygame.Vector2(200, 100), 
               pygame.Vector2(0, 100)
            ],
            "Seats" : [
               {
                  "Pos" : pygame.Vector2(100, 0),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : pygame.Vector2(50, 100),
                  "Occupied" : -1
               }, 
               {
                  "Pos" : pygame.Vector2(150, 100),
                  "Occupied" : -1
               }
            ]
         }
      }
      self.Room = self.getScene()
      self.mouseHolding = {"ID":0, "Tag": ""}
      self.mouseSelected = None
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
      self.screen  = {
         "Viewport" : pygame.display.set_mode((700, 700), vsync=1),
         "Room" : pygame.Surface((700, 700))
         }
      

      self.RoomPos = pygame.Vector2(0, 0)
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

      self.HandleMouse()

      for Table in self.Room["Tables"]:
         self.manager.SnapSeated(Table)


   def HandleMouse(self):
      
      mousePos = getRoomCursorPos(self.RoomPos)

      self.mouseSelected = self.getSelected()

      if self.mouseSelected != None:

         if self.mouseHolding["Tag"] == "":

            #Dropdown menu
            self.DropDownMenu(self.mouseSelected[0])
            
            return


         r = self.manager.changeName(self.mouseSelected, self.Event)



         if r == 1:

            self.mouseSelected == None
         return

      self.mouseHolding = self.getHolding()   
      
      if self.mouseHolding["ID"] != None and self.mouseSelected == None:
         
         transform : TransformComponent = self.manager.getComponent(self.mouseHolding["ID"], TransformComponent)

         match self.mouseHolding["Tag"]:

            case "Normal":   

               transform.rect.center = mousePos

               #If Seat
               if not self.manager.hasComponent(self.mouseHolding["ID"], SeatComponent):
                  self.SnappToSeat(self.mouseHolding["ID"])

               #If Table
               if self.manager.hasComponent(self.mouseHolding["ID"], VertexComponent):
                  self.SnappToVertex(self.mouseHolding["ID"])

               #If the object has seats
               if self.manager.hasComponent(self.mouseHolding["ID"], SeatComponent):
                  
                  for seat in self.manager.getComponent(self.mouseHolding["ID"], SeatComponent).getViewportRelativeSeats(transform.getScale(), transform.rect):
                     
                     #If seat is not empty
                     if seat["Occupied"] != -1:

                        #Move occupant to new position
                        occuRect = self.manager.getComponent(seat["Occupied"], TransformComponent).rect
                        occuRect.center = seat["Pos"].xy


            case "Edge":
               
               transform.rect.size = [max(mousePos.x - transform.rect.x, 25), max(mousePos.y - transform.rect.y, 25)]
               
               if self.manager.hasComponent(self.mouseHolding["ID"], CollisionComponent):
               
                  Collision = self.manager.getComponent(self.mouseHolding["ID"], CollisionComponent)

                  if Collision.negativeEdge != None:

                     Collision.negativeEdge.size = [ transform.rect.width - 10, transform.rect.height - 10 ]

               
               #If the object has seats
               if self.manager.hasComponent(self.mouseHolding["ID"], SeatComponent):
                  
                  self.manager.SnapSeated(self.mouseHolding["ID"])

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
         
         if result: return {"ID": self.Room["People"][x], "Tag" : flag}

    #Moves backwards so the top most table get picked first   
      for x in range(len(self.Room["Tables"])-1, -1, -1):
   
         result, flag = self.manager.CheckCollision(self.Room["Tables"][x], mousePos)
    
         if result:
    
             return {"ID": self.Room["Tables"][x], "Tag":flag }

      return {"ID" : None, "Tag" : ""}
   

   def getHolding(self) -> object:

      hover = self.getHover()
      #Nice Cursor change for ease of use 
      if hover["ID"] != None:

         if hover["Tag"] == "Edge":
            self.cursorIMG = pygame.SYSTEM_CURSOR_SIZENWSE

         else:
            self.cursorIMG = pygame.SYSTEM_CURSOR_SIZEALL      
      
      #Left mouse button
      if not pygame.mouse.get_pressed()[0]:
         return {"ID": None, "Tag":""}
      
      #If already holding something
      if self.mouseHolding["ID"] != None:

         if self.mouseHolding["Tag"] == "Edge":
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
         return self.getHover()[0], ""


   def createPerson(self, rect, text=""):

      t = self.manager.newEntity()
      
      self.manager.newComponent(t, TransformComponent, rect, False)
      
      self.manager.newComponent(t, SpriteComponent, (255, 255, 255), 10, (0, 0, 0), 2)
      
      self.manager.newComponent(t, TextComponent, text, (0, 0, 0), self.font)
      
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

      rect = pygame.Rect(250, 300, 50, 100)
      self.createTable("Rectangular", rect)

      return self.Room

   def SnappToSeat(self, heldEnt:int):

      TransformComp : TransformComponent = self.manager.getComponent(heldEnt, TransformComponent)

      for table in self.Room["Tables"]:
         
         if not self.manager.hasComponent(table, SeatComponent):
            continue
            
         TableTransform : TransformComponent = self.manager.getComponent(table, TransformComponent)
         SeatComp : SeatComponent = self.manager.getComponent(table, SeatComponent)
         seats : list = SeatComp.getViewportRelativeSeats(TableTransform.getScale(), TableTransform.rect)
         
         for x in range(0, len(seats)):

            if pointCollision(seats[x]["Pos"], TransformComp.rect):
               
               if seats[x]["Occupied"] == -1 and heldEnt != table:

                  seats[x]["Occupied"] = heldEnt

                  SeatComp.returnViewportRelativeSeats(TableTransform.getScale(), TableTransform.rect, seats)

                  return

            elif seats[x]["Occupied"] == heldEnt:
               
               seats[x]["Occupied"] = -1

               SeatComp.returnViewportRelativeSeats(TableTransform.getScale(), TableTransform.rect, seats)
            

   def SnappToVertex(self, heldEnt:int):

      ATransform : TransformComponent = self.manager.getComponent(heldEnt, TransformComponent)

      AVertexComp : VertexComponent = self.manager.getComponent(heldEnt, VertexComponent)


      for table in self.Room["Tables"]:
         
         if heldEnt == table:
            continue

         if not self.manager.hasComponent(table, VertexComponent):
            continue
         

         BTransform : TransformComponent = self.manager.getComponent(table, TransformComponent)

         BVertexComp : VertexComponent = self.manager.getComponent(table, VertexComponent)
         BVertices = BVertexComp.getViewportRelativeVertices(BTransform.getScale(), BTransform.rect)


         AVertices = AVertexComp.getViewportRelativeVertices(ATransform.getScale(), ATransform.rect)
         
         for AVertex in AVertices:
                           
            for BVertex in BVertices:

               if pointCircleCollision(AVertex, BVertex, 25):
               
                  #  Math! 
                  #  It's equivalent to 
                  #  AVertex.x = BVertex.x 
                  #  AVertex.y = BVertex.y
                  #  Though, this is what works as code

                  X = BVertex.x - AVertex.x + ATransform.rect.x
                  Y = BVertex.y - AVertex.y + ATransform.rect.y

                  ATransform.rect.topleft = X, Y

                  return
      return
   

   def DropDownMenu(self, ent):

      menu = self.CreateDropDown(ent)

   def CreateDropDown(self, ent):

      def createButton(rect, text, Font):

         B = self.manager.newEntity()
         surf = pygame.Surface(rect.size).convert_alpha()
         surf.fill((0, 0, 0))

         self.manager.newComponent(B, TransformComponent, rect)
         self.manager.newComponent(B, SpriteComponent, surf)
         self.manager.newComponent(B, TextComponent, text, (255, 255, 255), Font)

         return B

      DropDown = self.manager.newEntity()
      i = 0
      buttons = []
      if self.manager.hasComponent(ent, TextComponent):
         rect = pygame.Rect(0, 20*i, 50, 20)
         createButton(rect, "Rename", self.font)
         i += 1


def NalaniÄrBäst(): #Formaly known as Main

   App = app()
   
   while App.running:

      App.Felicia() #Formaly known as Event
      
      App.Morot() #Formaly known as Update
      
      App.Groda() #Formaly known as Render

      pygame.display.update()
      pygame.time.Clock().tick(60)
   
NalaniÄrBäst()