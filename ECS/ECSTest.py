from Component import *

manager = Manager()

pygame.init()

font = pygame.font.SysFont("Helvetica", 20)

def mouseCollision(A, B:pygame.Rect):
    return (A[0] >= B.x and A[0] <= B.x + B.width) and (A[1] >= B.y and A[1] <= B.y + B.height)

class app:
   def __init__(self):
      self.Scene = self.getScene()
      self.mouseHolding = [None, ""]
      self.mouseSelected = None
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
      self.screen = pygame.display.set_mode((700, 700))
      self.Event = pygame.event.get()
      self.running = True

   def getHover(self) -> list:
      mousePos = pygame.mouse.get_pos()
      #Moves backwards so the top most person get picked first
      for x in range(len(self.Scene["People"])-1, -1, -1):
         
         transform = manager.getComponent(self.Scene["People"][x], TransformComponent)

         if mouseCollision(mousePos, transform.rect): return [self.Scene["People"][x], "Normal"]

   # #Moves backwards so the top most table get picked first   
   #  for x in range(len(Scene["Tables"])-1, -1, -1):
   #
   #     result, flag = Scene["Tables"][x].getMouseTouching(mousePos)
   #
   #     if result:
   #
   #         return Scene["Tables"][x], flag 
      return [None, ""]
   
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



   def getScene(self):
      #Placeholder function
      
      scene = {
         "People" : [],
         "Tables" : []
      }
      for i in range (0, 5):   
         t = manager.newEntity()
         rect = pygame.Rect(100*i, 100, 50,  50)
         manager.newComponent(t, TransformComponent, rect, False)
         manager.newComponent(t, SpriteComponent, (255, 255, 255), 10, (0, 0, 0), 2)
         manager.newComponent(t, TextComponent, "", (0, 0, 0), font)
         scene["People"].append(t)


      return scene


   
App = app()
while App.running:
   App.Event = pygame.event.get()
   for event in App.Event:
      if event.type == pygame.QUIT:
         App.running = False

   pygame.mouse.set_cursor(App.cursorIMG)
   App.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
   
   App.screen.fill((255, 255, 255))

   #draw
   for Person in App.Scene["People"]:
      draw(manager, Person, App.screen)

   App.mouseHolding = App.getHolding()
   if App.mouseHolding[0] != None:
      Hover = manager.getComponent(App.mouseHolding[0], TransformComponent)
      Hover.rect.center = pygame.mouse.get_pos()

   App.mouseSelected = App.getSelected()

   if App.mouseSelected != None:
      r = changeName(manager, App.mouseSelected, App.Event)
      if r == 1:
         App.mouseSelected == None
   pygame.display.update()
   pygame.time.Clock().tick(60)