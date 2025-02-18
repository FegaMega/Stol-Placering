import sys
import math
import os

import pygame
from pygame.locals import *

import Objects

import OldJsonHandler



def mouseCollision(Ax, Ay, Bx, By, Bwidth, Bheight):
    return (Ax >= Bx and Ax <= Bx + Bwidth) and (Ay >= By and Ay <= Ay <= By + Bheight)

def mouseCircleCollision(Ax, Ay, Bc, Bd):
    Diffrence = [Bc[0]-Ax, Bc[1]-Ay]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2


class ClassApp:
    def __init__(self) -> None:
        self.FontName = "Helvetica-bold"

        try :
            self.settings = OldJsonHandler.GetJson("data/Settings.json")
        except FileNotFoundError:
            s = { 
                "RoomFile" : "data/Example-Room.json",
                "CurrentRoom" : 0,
                "ScreenSize" : [700, 700],
                "scale": {
                    "seat" : 1,
                    "table" : 1,
                    "GUI" : 1,
                    "Font" : {
                        "Seat": 1,
                        "Table": 1,
                        "GUI": 1
                    }
                }
            }
            OldJsonHandler.WriteJson("data/Settings.json", s)
            self.settings = OldJsonHandler.GetJson("data/Settings.json")

        self.FontSize = 20
        self.FONT = {
            "GUI" : pygame.font.SysFont(self.FontName, self.FontSize    *self.settings["scale"]["Font"]["GUI"]      *self.settings["scale"]["GUI"]),
            "Table" : pygame.font.SysFont(self.FontName, self.FontSize  *self.settings["scale"]["Font"]["Table"]    *self.settings["scale"]["table"]),
            "Seat" : pygame.font.SysFont(self.FontName, self.FontSize   *self.settings["scale"]["Font"]["Seat"]     *self.settings["scale"]["seat"])
        }
        self.running = True
        self.screen = pygame.display.set_mode( self.settings["ScreenSize"], vsync=1 )
        pygame.display.set_caption("Stol Placering av David Smidebrant")
        pygame.display.set_icon(pygame.image.load("data/Icon.png"))
        self.UIstate = None
        self.GUI = {
            "EscapeUI" : [
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-145, 100, 50, "RENAME", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-85, 100, 50, "OPEN", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-25, 100, 50, "NEW", scale=self.settings["scale"]["GUI"]),
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+35, 100, 50, "DELETE", scale=self.settings["scale"]["GUI"]),
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+95, 100, 50, "Export as PDF", scale=self.settings["scale"]["GUI"]),
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+155, 100, 50, "SETTINGS", scale=self.settings["scale"]["GUI"])
            ],
            "OPENUI" : [],
            "NEWUI" : [
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+5, 100, 50, "", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-45, 100, 50, "Name:", scale=self.settings["scale"]["GUI"])
            ],
            "RENAMEUI" : [
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+5, 100, 50, "", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton(self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-45, 100, 50, "Name:", scale=self.settings["scale"]["GUI"])
            ],
            "SETTINGSUI" : [
                Objects.ClassButtonSlider(self.screen.get_size()[0]/2, self.screen.get_size()[1]/2 - 85, 100, 50, 1, 3)
            ]

        }
        self.GUIRoomFill()
        json = OldJsonHandler.GetJson(self.settings["RoomFile"]).keys()
        if json:
            self.settings["CurrentRoom"] = next(iter(json))
            self.Room = OldJsonHandler.ReadRoom(self.settings["RoomFile"], self.settings["CurrentRoom"], self.FONT, self.settings["scale"])
        else:
            
            OldJsonHandler.CreateRoom(self.settings["RoomFile"], "Room1")
            self.changeRoom("Room1")
        self.mouse = Objects.ClassMouse()
        self.typingMode = [False, None]
        
    def GUIRoomFill(self):
        nr = 0
        self.GUI["OPENUI"] = []
        for room in OldJsonHandler.GetJson(self.settings["RoomFile"]).keys():
            self.GUI["OPENUI"].append(Objects.ClassButton(self.screen.get_size()[0]/2-50, 25*nr+50, 100, 20, room, scale=self.settings["scale"]["GUI"]))
            nr += 1     

    def changeRoom(self, RoomID):
        self.settings["CurrentRoom"] = RoomID
        self.Room = OldJsonHandler.ReadRoom(self.settings["RoomFile"], self.settings["CurrentRoom"], self.FONT, self.settings["scale"])

    def saveRoom(self):
        OldJsonHandler.WriteRoom(self.settings["RoomFile"], self.settings["CurrentRoom"], self.Room, self.settings["scale"])

    def NewRoom(self, ID):
        OldJsonHandler.CreateRoom(self.settings["RoomFile"], ID)

    def deleteRoom(self, ID):
        OldJsonHandler.RemoveRoom(self.settings["RoomFile"], ID)
    
    def renameRoom(self, ID, name):
        OldJsonHandler.RenameRoom(self.settings["RoomFile"], ID, name)

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
            if event.key == K_ESCAPE:
                if self.UIstate != "Escape":
                    self.UIstate = "Escape"
                else: 
                    self.UIstate = None
        self.ButtonCheck()
    def variableUpdate(self):
        self.mouse.update(self.Room["Tables"], self.Room["RoundTables"], self.settings["scale"])
        
        self.typingMode = self.typingCheck()
        
        if self.typingMode[0]:
            if type(self.typingMode[1]) == Objects.ClassSeat:
                self.typingMode[1].color = (255, 0, 0)
            for event in pygame.event.get(KEYDOWN, False):
                if event.key == K_RETURN:
                    self.typingMode[0] = False
                elif event.key == K_BACKSPACE:
                    self.typingMode[1].text = self.typingMode[1].text[:-1]
                else:
                    self.typingMode[1].text += event.unicode

    def createAnotherSeat (self):
        self.Room["Seats"].append(Objects.ClassSeat(self.mouse.pos[0], self.mouse.pos[1], self.FONT["Seat"], scale=self.settings["scale"]))
    def createAnotherTable (self):
        self.Room["Tables"].append(Objects.ClassTable(self.mouse.pos[0], self.mouse.pos[1], 100, 100, self.settings["scale"]["table"]))
    def createAnotherRoundTable (self):
        self.Room["RoundTables"].append(Objects.ClassRoundTable(self.mouse.pos[0], self.mouse.pos[1], 150, self.settings["scale"]["table"]))

    def deleteASeat(self):
        for seat in self.Room["Seats"]:
            if mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], [seat.rect.x+seat.diameter/2, seat.rect.y+seat.diameter/2], seat.diameter):
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

                    if mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], [seat.rect.x+seat.diameter/2, seat.rect.y+seat.diameter/2], seat.diameter):
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
        if not mouseCircleCollision(self.mouse.pos[0], self.mouse.pos[1], [seat.rect.x+seat.diameter/2, seat.rect.y+seat.diameter/2], seat.diameter):
            return self.mouse.holding

        return [seat, None, None]

    def ButtonCheck(self):
        if self.UIstate == "Escape":
            for button in self.GUI["EscapeUI"]:
                if not pygame.mouse.get_pressed(3)[0]:
                    continue
                if not mouseCollision(self.mouse.pos[0], self.mouse.pos[1], button.rect.x, button.rect.y, button.rect.w, button.rect.h):
                    continue
                else:
                    self.UIstate = button.text
                    break
        if self.UIstate == "OPEN":
            for button in self.GUI["OPENUI"]:
                if not pygame.mouse.get_pressed(3)[0]:
                    continue
                if not mouseCollision(self.mouse.pos[0], self.mouse.pos[1], button.rect.x, button.rect.y, button.rect.w, button.rect.h):
                    continue
                else:
                    self.saveRoom()
                    self.changeRoom(button.text)
                    self.UIstate = None
                    break
        if self.UIstate == "NEW":
            if self.typingMode[1] != self.GUI["NEWUI"][0]:
                self.typingMode[0] = True
                self.typingMode[1] = self.GUI["NEWUI"][0]
            elif self.typingMode[0] == False:
                self.UIstate = None
                self.saveRoom()
                self.NewRoom(self.GUI["NEWUI"][0].text)   
                self.changeRoom(self.GUI["NEWUI"][0].text)
                self.GUI["NEWUI"][0].text = ""
                self.GUIRoomFill()
        if self.UIstate == "DELETE":
            self.deleteRoom(self.settings["CurrentRoom"])
            self.changeRoom(self.GUI["OPENUI"][0].text)
            self.GUIRoomFill()
            self.UIstate = "OPEN"
        if self.UIstate == "RENAME":
            if self.typingMode[1] != self.GUI["RENAMEUI"][0]:
                self.typingMode[0] = True
                self.typingMode[1] = self.GUI["RENAMEUI"][0]
            elif self.typingMode[0] == False:
                self.UIstate = None
                self.renameRoom(self.settings["CurrentRoom"], self.GUI["RENAMEUI"][0].text)
                self.changeRoom(self.GUI["RENAMEUI"][0].text)
                self.GUI["RENAMEUI"][0].text = ""
                self.GUIRoomFill()
        if self.UIstate == "Export as PDF":
            self.UIstate = None
            self.draw()
            pygame.image.save(self.screen, "data/"+self.settings["CurrentRoom"] + ".png")
                

    def draw(self):
        self.screen.fill((100, 100, 100))
        for table in self.Room["Tables"]:
            table.draw(self.screen)
        for table in self.Room["RoundTables"]:
            table.draw(self.screen)
        for seat in self.Room["Seats"]:
            seat.draw(self.screen, self.FONT["Seat"])        
        self.Room["Tavla"].draw(self.screen, self.FONT["Table"])
        if (self.UIstate == "Escape" or 
            self.UIstate == "OPEN" or 
            self.UIstate == "NEW" or
            self.UIstate == "RENAME" or
            self.UIstate == "SETTINGS"
            ):
            for Element in self.GUI[self.UIstate + "UI"]:
                Element.draw(self.screen, self.FONT["GUI"])

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
    app.saveRoom()
    OldJsonHandler.WriteJson("data/Settings.json", app.settings)
    pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())