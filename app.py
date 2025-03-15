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

      self.FontName = "Helvetica"

      self.screen = {
         "Display Port" : pygame.display.set_mode([1000, 1000], vsync=1),
         "Display Size" : pygame.display.get_window_size(),
         "FPS" : 60
      }
   
      #Object the operator i holding, if None there is no object being held 
      #First index is the object 
      #Second index is a flag
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW
      self.mouseHolding = [None, "None"]
      self.mouseSelected = None
      self.mouseSelectedMode = ""

      self.Room = RoomHandler.getRoom(self.setting["RoomFile"], self.setting["CurrentRoom"], self.FontName, self.setting["scale"])      


   #Main Functions
   def Event(self):
      self.event:list = pygame.event.get()
      
      for event in self.event:

         if event.type == pygame.QUIT:
            
            self.running = False

      return
   

   def update(self):
      pygame.mouse.set_cursor(self.cursorIMG)
      self.cursorIMG = pygame.SYSTEM_CURSOR_ARROW

      self.handleHeldObject()

      self.handleSelectedObject()
            

      return
   

   def render(self):

      self.screen["Display Port"].fill((100, 100, 100))

      for table in self.Room["Tables"]:
         table.draw(self.screen["Display Port"])

      self.Room["Tavla"].draw(self.screen["Display Port"])
      
      for person in self.Room["People"]:
         person.draw(self.screen["Display Port"])

      pygame.display.update()

      return
   

   def fpsLimit(self) : pygame.time.Clock().tick( self.screen["FPS"] )


   def clean(self):

      RoomHandler.saveRoom(self.setting["RoomFile"], self.setting["CurrentRoom"], self.Room, self.setting["scale"])

      pygame.quit()

      return


   #Daughter Functions
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

      return None
      

   def getHover(self) -> list:
      mousePos = pygame.mouse.get_pos()
      #Moves backwards so the top most person get picked first
      for x in range(len(self.Room["People"])-1, -1, -1):
         
         person = self.Room["People"][x]

         if mouseCollision(mousePos, person.rect): return person, "Normal"

      #Moves backwards so the top most table get picked first   
      for x in range(len(self.Room["Tables"])-1, -1, -1):

         result, flag = self.Room["Tables"][x].getMouseTouching(mousePos)

         if result:

            return self.Room["Tables"][x], flag 
      
      result, flag = self.Room["Tavla"].getMouseTouching(mousePos)
      if result: return self.Room["Tavla"], flag

      return [None, ""]


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


   def handleHeldObject(self):

      #[Held Object, Flag]
      self.mouseHolding = self.getHolding()

      match self.mouseHolding[1]:

         case "Normal":
            self.mouseHolding[0].rect.center = Snap ( pygame.mouse.get_pos(), 5 )

         case "Edge":
            self.mouseHolding[0].rect.width = Snap( max( pygame.mouse.get_pos()[0] - self.mouseHolding[0].rect.x, 25), 5 )
            self.mouseHolding[0].rect.height = Snap( max(pygame.mouse.get_pos()[1] - self.mouseHolding[0].rect.y, 25), 5 )


   def handleSelectedObject(self):
      #Reset Variables
      
      if self.mouseSelected.__class__ == Objects.Person:
         self.mouseSelected.selected = False

      #Get Object
      self.mouseSelected = self.getSelected()

      if self.mouseSelected.__class__ == Objects.Person:
         
         self.mouseSelected.selected = True
         
         match self.mouseSelectedMode:

            case "Menu":
               
               return

            case "Rename":
            #Change Variables            
               text = self.getTextEvent(self.mouseSelected.text)
               
               if text == 0:
                  
                  self.mouseSelected = (None, "")

                  return
               
               self.mouseSelected.changeName( text, self.setting["scale"] )


def main():
   app = App()
   while app.running:
      app.update()
      app.Event()
      app.render() 
      app.fpsLimit()
   app.clean()



main()