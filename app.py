#rewrite of the entire app.py script to hopefully make everything more 
import pygame
import RoomHandler
import SettingsHandler
import math

def mouseCollision(A, B:pygame.Rect):
    return (A[-1] >= B.x and A[0] <= B.x + B.width) and (A[1] >= B.y and A[1] <= B.y + B.height)

def mouseCircleCollision(A, Bc, Bd):
    Diffrence = [Bc[0]-A[0], Bc[1]-A[1]]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2

class App:
   def __init__(self):
      pygame.init()
      self.setting = SettingsHandler.getSettings()
      self.running = True
      self.FontName = "Helvetica-bold"
      self.screen = {
         "Display Port" : pygame.display.set_mode([700, 700]),
         "Display Size" : pygame.display.get_window_size(),
         "FPS" : 60
      }
   
      #Object the operator i holding, if None there is no object being held 
      self.mouseHolding = None

      self.Room = RoomHandler.getRoom(self.setting["RoomFile"], self.setting["CurrentRoom"], self.FontName, self.setting["scale"])      


#Main Functions
   def event(self):

      if pygame.event.get( pygame.QUIT ):
         self.running = False

      return
   

   def update(self):
      self.getHover()
      return
   

   def render(self):

      self.screen["Display Port"].fill((255, 255, 255))

      for person in self.Room["People"]:
         person.draw(self.screen["Display Port"])

      for table in self.Room["Tables"]:
         table.draw(self.screen["Display Port"])

      self.Room["Tavla"].draw(self.screen["Display Port"])

      pygame.display.update()

      return
   

   def fpsLimit(self) : pygame.time.Clock().tick( self.screen["FPS"] )


   def clean(self):

      RoomHandler.saveRoom(self.setting["RoomFile"], self.setting["CurrentRoom"], self.Room, self.setting["scale"])

      pygame.quit()

      return

#Daughter Functions
   def getHover(self):

      for person in self.Room["People"]:
         
         if mouseCollision(pygame.mouse.get_pos(), person.rect):
            return person
         
      for table in self.Room["Tables"]:

         if table.getMouseTouching(pygame.mouse.get_pos()):
            return table 
         
def main():#
   app = App()
   while app.running:
      app.event()
      app.update()
      app.render() 
      app.fpsLimit()
   app.clean()

main()
