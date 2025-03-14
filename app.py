#rewrite of the entire app.py script to hopefully make everything more 
import pygame
import RoomHandler
import SettingsHandler
import math
import Objects
from GeneralFuntions import *

class App:

   def __init__(self):

      pygame.init()

      self.running = True 

      self.setting = SettingsHandler.getSettings()

      self.FontName = "Helvetica-bold"

      self.screen = {
         "Display Port" : pygame.display.set_mode([700, 700], vsync=1),
         "Display Size" : pygame.display.get_window_size(),
         "FPS" : 60
      }
   
      #Object the operator i holding, if None there is no object being held 
      self.mouseHolding = None
      self.mouseSelected = None

      self.Room = RoomHandler.getRoom(self.setting["RoomFile"], self.setting["CurrentRoom"], self.FontName, self.setting["scale"])      


   #Main Functions
   def Event(self):
      self.event:list = pygame.event.get()
      
      for event in self.event:

         if event.type == pygame.QUIT:
            
            self.running = False

      return
   

   def update(self):

      #Resets changes incase the mouse is holding another object
      
      self.mouseHolding = self.getHolding()

      if self.mouseHolding:
         self.mouseHolding.rect.center = Snap ( pygame.mouse.get_pos(), 5 )
      
      self.mouseSelected = self.getSelected()

      if self.mouseSelected.__class__ == Objects.Person:
         
         print(self.mouseSelected.text)
         
         text = self.getTextEvent(self.mouseSelected.text)
         
         if text == 0:
            self.mouseSelected = None
            return
         
         self.mouseSelected.changeName( text, self.setting["scale"] )

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
   def getHolding(self) -> object:

      #Left mouse button
      if not pygame.mouse.get_pressed()[0]:
         return None
      
      #If already holding something
      if self.mouseHolding:
         return self.mouseHolding
      
      return self.getHover()


   def getSelected(self) -> object:
      
      #Deselects if left mouse button is pressed
      if pygame.mouse.get_pressed()[0]:
         return None
      
      if self.mouseSelected:
         return self.mouseSelected

      if pygame.mouse.get_pressed()[2]:
         return self.getHover() 

      return None
      

   def getHover(self) -> object:
      mousePos = pygame.mouse.get_pos()
      #Moves backwards so the top most person get picked first
      for x in range(len(self.Room["People"])-1, -1, -1):
         
         person = self.Room["People"][x]

         if mouseCollision(mousePos, person.rect): return person

      #Moves backwards so the top most table get picked first   
      for x in range(len(self.Room["Tables"])-1, -1, -1):
                  
         if self.Room["Tables"][x].getMouseTouching(mousePos): return self.Room["Tables"][x] 
      
      if self.Room["Tavla"].getMouseTouching(mousePos): return self.Room["Tavla"]

      return None

   def getTextEvent(self, text:str):
      for event in self.event:
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
               return 0
            elif event.key == pygame.K_BACKSPACE:
               text = text[:-1]
            else:
               text += event.unicode
      return text




def main():#
   app = App()
   while app.running:
      app.update()
      app.Event()
      app.render() 
      app.fpsLimit()
   app.clean()

main()