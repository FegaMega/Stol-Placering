import os
os.system("pip install pygame")
os.system("pip3 install pygame")
import pygame
from pygame.locals import *
import Objects

import sys


class ClassApp:
    def __init__(self) -> None:
        self.running = True
        self.screen = pygame.display.set_mode( ( 700, 700 ) )
        self.Tables = [Objects.ClassTable(200, 200, 50, 50), Objects.ClassTable(200, 300, 10, 50)]
    
    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    
    def draw(self):
        for table in self.Tables:
            table.draw(self.screen)
    
    def displayUpdate(self):
        pygame.display.update()
        pygame.time.Clock().tick(60)
def main() -> int:
    pygame.init()
    app = ClassApp()
    while app.running:
        app.events()
        app.draw()
        app.displayUpdate()
    pygame.quit()
    return 0


sys.exit(main())