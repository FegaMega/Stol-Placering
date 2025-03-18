from Component import *


pygame.init()


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
      self.screen = pygame.display.set_mode((700, 700))
      self.Event = pygame.event.get()
      self.running = True


#Main Functions
   def event(self):

      self.Event = pygame.event.get()

      for event in self.Event:

         if event.type == pygame.QUIT:

            self.running = False


   def Update(self):

      pygame.mouse.set_cursor(self.cursorIMG)
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW


      self.mouseHolding = self.getHolding()   

      if self.mouseHolding[0] != None:
      
         transform = self.manager.getComponent(self.mouseHolding[0], TransformComponent)
         match self.mouseHolding[1]:
            case "Normal":
               transform.rect.center = pygame.mouse.get_pos()
            case "Edge":
               transform.rect.size = [pygame.mouse.get_pos()[0] - transform.rect.x, pygame.mouse.get_pos()[1] - transform.rect.y]


      self.mouseSelected = self.getSelected()

      if self.mouseSelected != None:

         r = changeName(self.manager, self.mouseSelected, self.Event)

         if r == 1:

            self.mouseSelected == None

      return 

   def Render(self):
      self.screen.fill((255, 255, 255))
      #draw
      for Person in self.Room["People"]:
         self.manager.draw(Person, self.screen)

      for Table in self.Room["Tables"]:
         self.manager.draw(Table, self.screen)

      return
   

#Daughter functions 
   def getHover(self) -> tuple:
      mousePos = pygame.mouse.get_pos()

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
      
      self.Room["People"].append(t)
   

   def createTable(self, rect):

      t = self.manager.newEntity()

      self.manager.newComponent(t, TransformComponent, rect, True)

      self.manager.newComponent(t, SpriteComponent, (0, 0, 0), 10)

      rect2 = rect
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
         self.createTable(rect)
         
      return self.Room


   
App = app()
while App.running:

   App.event()
   
   App.Update()

   App.Render()

   pygame.display.update()
   pygame.time.Clock().tick(60)