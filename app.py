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
        self.Tables = [Objects.ClassTable(200, 200, 300, 300, self.FONT), Objects.ClassTable(200, 300, 25, 50, self.FONT)]
        self.Seats =[Objects.ClassSeat(200, 240, self.FONT)]
        self.mouse = Objects.ClassMouse()
        self.typingMode = [False, None]
    def events(self):
        if pygame.event.get(QUIT, False):
            self.running = False
        if self.typingMode[0]:
            return
        for event in pygame.event.get(KEYDOWN, False):
            if event.key == K_c:
                self.createAnotherSeat()

    def variableUpdate(self):
        self.mouse.update()
        
        for table in self.Tables:
            self.typingMode = self.typingCheck(table)
            if self.typingMode[0] == True:
                break
        
        if self.typingMode[0]:
            for event in pygame.event.get(KEYDOWN, False):
                if event.key == K_RETURN:
                    self.typingMode[0] = False
                elif event.key == K_BACKSPACE:
                    self.typingMode[1].text = self.typingMode[1].text[:-1]
                else:
                    self.typingMode[1].text += event.unicode

    def createAnotherSeat (self):
        self.Seats.append(Objects.ClassSeat(self.mouse.pos[0], self.mouse.pos[1], self.FONT))



    def typingCheck(self, table : Objects.ClassTable):
        e = pygame.event.get(MOUSEBUTTONDOWN, False)
        for event in e:
            
            if event.button == 1:

                for seat in self.Seats:
            
                    if not mouseCollision(self.mouse.pos[0], self.mouse.pos[1], seat.pos[0], seat.pos[1], seat.diameter, seat.diameter):
                        return [False, None]
            
                    if self.typingMode[0] == True:
                        return [False, None]
                    
                return [True, seat]
        return [False, None]
    
    def MoveDetection(self):
        
        for table in self.Tables:
            self.mouse.holding = self.followCheck(table)
            if self.mouse.holding[0] != None:
                return
            if self.mouse.holding[0] == None:
                for seat in table.Seats:
                    self.mouse.holding = self.SeatFollowCheck(table, seat)
                    if self.mouse.holding[0] != None:
                        return
                

        
    
    def followCheck(self, table : Objects.ClassTable) -> list:
        if not pygame.key.get_pressed()[K_LCTRL]:
            return [None, None, None]
        if not pygame.mouse.get_pressed(3)[0]:
            return [None, None, None]
        if not mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.y, table.rect.width, table.rect.height):
            return self.mouse.holding
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        return [table, 
                mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.bottom - 10, table.rect.w, 10), 
                mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.right-10, table.rect.y, 10, table.rect.h)]
        
    def SeatFollowCheck(self, table : Objects.ClassTable, seat) -> list:
        if not pygame.key.get_pressed()[K_LSHIFT]:
            return [None, None, None]
        if not pygame.mouse.get_pressed(3)[0]:
            return [None, None, None]
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        if not mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x+seat.pos[0], table.rect.y+seat.pos[1], seat.diameter, seat.diameter):
            return self.mouse.holding
        return [seat, None, None]


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
        app.MoveDetection()
        pygame.event.get() #Clearing event list to work around https://github.com/pygame/pygame/issues/3229
        app.draw()
        app.displayUpdate()
        pygame.event.pump()
    pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())