#rewrite of the entire app.py script to hopefully make everything more 
import pygame
import RoomHandler
import SettingsHandler


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

      self.Room = RoomHandler.ReadRoom()
      

   def event(self):
      if pygame.event.get( pygame.QUIT ):
         self.running = False
      return
   def update(self):
      return
   def render(self):
      pygame.display.update()
      return
   def clean(self):
      RoomHandler.saveRoom()
      pygame.quit()
      return
   def fpsLimit(self):
      pygame.time.Clock().tick( self.screen["FPS"] )

def main():
   app = App()
   while app.running:
      app.event()
      app.update()
      app.render() 
      app.fpsLimit()
   app.clean()

main()
