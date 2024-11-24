import sys
import math

import pygame
from pygame.locals import *

import Objects

import JsonHandler



def mouseCollision(Ax, Ay, Bx, By, Bwidth, Bheight):
    return (Ax >= Bx and Ax <= Bx + Bwidth) and (Ay >= By and Ay <= Ay <= By + Bheight)

def mouseCircleCollision(Ax, Ay, Bc, Bd):
    Diffrence = [Bc[0]-Ax, Bc[1]-Ay]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2


class ClassApp:
    def __init__(self) -> None:
        self.FONT = pygame.font.SysFont("Helvetica-bold", 24)
        self.running = True
        self.jsonLink = "data/Rum.json"
        self.screen = pygame.display.set_mode( ( 700, 700 ) )
        jsonRoom = JsonHandler.ReadRoom(self.jsonLink, "Room1", self.FONT)
        self.Room = jsonRoom
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
            if event.key == K_r:
                self.createAnotherRoundTable()
            if event.key == K_t:
                self.createAnotherTable()
            if event.key == K_d or event.key == K_DELETE:
                if self.deleteASeat():
                    continue
                elif self.deleteATable():
                    continue
                self.deleteARoundTable()
    def variableUpdate(self):
        self.mouse.update(self.Room["Tables"], self.Room["RoundTables"])
        
        self.typingMode = self.typingCheck()
        
        if self.typingMode[0]:
            self.typingMode[1].color = (255, 0, 0)
            for event in pygame.event.get(KEYDOWN, False):
                if event.key == K_RETURN:
                    self.typingMode[0] = False
                elif event.key == K_BACKSPACE:
                    self.typingMode[1].text = self.typingMode[1].text[:-1]
                else:
                    self.typingMode[1].text += event.unicode

    def createAnotherSeat (self):
        self.Room["Seats"].append(Objects.ClassSeat(self.mouse.pos[0], self.mouse.pos[1], self.FONT))
    def createAnotherTable (self):
        self.Room["Tables"].append(Objects.ClassTable(self.mouse.pos[0], self.mouse.pos[1], 100, 100))
    def createAnotherRoundTable (self):
        self.Room["RoundTables"].append(Objects.ClassRoundTable(self.mouse.pos[0], self.mouse.pos[1], 150))
    def deleteASeat(self):
        for seat in self.Room["Seats"]:
            if mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], seat.rect.center, seat.diameter):
                self.Room["Seats"].pop(self.Room["Seats"].index(seat))
                return 1
        return 0
    def deleteATable(self):
        for table in self.Room["Tables"]:
            if mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.y, table.rect.w, table.rect.w):
                self.Room["Tables"].pop(self.Room["Tables"].index(table))
                return 1
        return 0
    def deleteARoundTable(self):
        for table in self.Room["RoundTables"]:
            if mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.center, table.diameter):
                self.Room["RoundTables"].pop(self.Room["RoundTables"].index(table))
                return 1
        return 0

    def typingCheck(self):
        if self.mouse.holding[0] != None:
            return [False, None]
        e = pygame.event.get(MOUSEBUTTONDOWN, False)
        for event in e:
            
            if event.button == 1:

                for seat in self.Room["Seats"]:

                    if mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], seat.rect.center, seat.diameter):
                        return [True, seat]
                    
                return [False, None]
        return self.typingMode
        
    def MoveDetection(self):
        if pygame.key.get_pressed()[K_LCTRL]:
            for table in self.Room["Tables"]:
                self.mouse.holding = self.followCheck(table)
                if self.mouse.holding[0] != None:
                    return
            for table in self.Room["RoundTables"]:
                self.mouse.holding = self.followRoundCheck(table)
                if self.mouse.holding[0] != None:
                    return
            self.mouse.holding = self.followCheck(self.Room["Tavla"])
        elif pygame.key.get_pressed()[K_LSHIFT]:
            for seat in self.Room["Seats"]:
                self.mouse.holding = self.SeatFollowCheck(seat)
                if self.mouse.holding[0] != None:
                    return
        else:
            self.mouse.holding = [None, None, None]
                

        
    
    def followCheck(self, table : Objects.ClassTable) -> list:
        
        if not pygame.mouse.get_pressed(3)[0]:
            return [None, None, None]
        if not mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.y, table.rect.width, table.rect.height):
            return self.mouse.holding
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        return [table, 
                mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.x, table.rect.bottom - 10, table.rect.w, 10), 
                mouseCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.right-10, table.rect.y, 10, table.rect.h)]
        
    def followRoundCheck(self, table : Objects.ClassRoundTable) -> list:
        if not pygame.mouse.get_pressed(3)[0]:
            return [None, None, None]
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        if not mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.center, table.diameter):
            return self.mouse.holding
        return [table,
                not mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], table.rect.center, table.diameter-10),
                None]

    def SeatFollowCheck(self, seat) -> list:
        
        if not pygame.mouse.get_pressed(3)[0]:
            return [None, None, None]
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        if not mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], seat.rect.center, seat.diameter):
            return self.mouse.holding

        return [seat, None, None]


    def draw(self):
        self.screen.fill((100, 100, 100))
        for table in self.Room["Tables"]:
            table.draw(self.screen)
        for table in self.Room["RoundTables"]:
            table.draw(self.screen)
        for seat in self.Room["Seats"]:
            seat.draw(self.screen, self.FONT)        

        self.Room["Tavla"].draw(self.screen, self.FONT)

    def displayUpdate(self):
        pygame.display.update()
        pygame.time.Clock().tick(60)



def main() -> int:
    pygame.init()
    app = ClassApp()
    while app.running:
        app.events()
        app.MoveDetection()
        app.variableUpdate()
        pygame.event.get() #Clearing event list to work around https://github.com/pygame/pygame/issues/3229
        app.draw()
        app.displayUpdate()
        pygame.event.pump()
    JsonHandler.WriteRoom(app.jsonLink, "Room1", app.Room)
    pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())