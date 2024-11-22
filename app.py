import sys

import pygame
from pygame.locals import *

import Objects



def mouseCollision(Ax, Ay, Bx, By, Bwidth, Bheight):
    return (Ax >= Bx and Ax <= Bx + Bwidth) and (Ay >= By and Ay <= Ay <= By + Bheight)

class ClassApp:
    def __init__(self) -> None:
        self.FONT = pygame.font.SysFont("Helvetica-bold", 24)
        self.running = True
        self.screen = pygame.display.set_mode( ( 700, 700 ) )
        self.Tables = [Objects.ClassTable(200, 200, 50, 50, self.FONT), Objects.ClassTable(200, 300, 25, 50, self.FONT)]
        self.mouse = Objects.ClassMouse()
        self.typingMode = [False, None]
    def events(self):
        if pygame.event.get(QUIT, False):
            self.running = False
        for event in pygame.event.get(KEYDOWN):
            if self.typingMode[0]:
                if event.key == K_RETURN:
                    self.typingMode[0] = False
                elif event.key == K_BACKSPACE:
                    self.typingMode[1].text = self.typingMode[1].text[:-1]
                else:
                    self.typingMode[1].text += event.unicode

    def variableUpdate(self):
        self.mouse.update()
        
        

        for table in self.Tables:
            break

    
    def collisionChecks(self):
        for table in self.Tables:
            x = self.followCheck(table)
            if x[0] != None:
                self.mouse.holding = x
                break
            self.typingMode = self.typingCheck(table)

    def typingCheck(self, table : Objects.ClassTable):
        if not pygame.event.get(MOUSEBUTTONDOWN, False):
            return self.typingMode
        if mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.y, table.rect.width, table.rect.height):
            if self.typingMode[0] == False:
                return [True, table]
            
        return [False, None]
    
    def followCheck(self, table : Objects.ClassTable) -> list:
        if not pygame.key.get_pressed()[K_LCTRL]:
            self.mouse.holding[0] = None
            return [None, None, None]
        if not pygame.mouse.get_pressed(3)[0]:
            self.mouse.holding[0] = None
            return [None, None, None]
        if not mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.y, table.rect.width, table.rect.height):
            return [None, None, None]
        if self.mouse.holding[0] != None:
            return [None, None, None]
        return [table, 
                mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.bottom - 10, table.rect.w, 10), 
                mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.right-10, table.rect.y, 10, table.rect.h)]
        
    def draw(self):
        self.screen.fill((100, 100, 100))
        for table in self.Tables:
            table.draw(self.screen, self.FONT)
        

    def displayUpdate(self):
        pygame.display.update()
        pygame.time.Clock().tick(60)



def main() -> int:
    pygame.init()
    app = ClassApp()
    while app.running:
        app.events()
        app.variableUpdate()
        app.collisionChecks()
        app.draw()
        app.displayUpdate()
        pygame.event.pump()
    pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())