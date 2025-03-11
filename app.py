import sys
import math
import os

import pygame
from pygame.locals import *

import Objects

import JsonHandler



def mouseCollision(A, B, Bs):
    return (A[0] >= B[0] and A[0] <= B[0] + Bs[0]) and (A[1] >= B[1] and A[1] <= B[1] + Bs[1])

def mouseCircleCollision(A, Bc, Bd):
    Diffrence = [Bc[0]-A[0], Bc[1]-A[1]]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2


class ClassApp:
    def __init__(self) -> None:
        self.FontName = "Helvetica-bold"

        try :
            self.settings = JsonHandler.GetJson("data/Settings.json")
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
            JsonHandler.WriteJson("data/Settings.json", s)
            self.settings = JsonHandler.GetJson("data/Settings.json")

        self.FontSize = 20
        self.FONT = {
            "GUI" : pygame.font.SysFont(self.FontName, self.FontSize    *self.settings["scale"]["Font"]["GUI"]      *self.settings["scale"]["GUI"]),
            "Tavla" : pygame.font.SysFont(self.FontName, self.FontSize  *self.settings["scale"]["Font"]["Table"]    *self.settings["scale"]["table"]),
            "Seat" : pygame.font.SysFont(self.FontName, self.FontSize   *self.settings["scale"]["Font"]["Seat"]     *self.settings["scale"]["seat"])
        }
        self.running = True
        self.screen = pygame.display.set_mode( self.settings["ScreenSize"], vsync=1 )
        pygame.display.set_caption("Stol Placering av David Smidebrant")
        pygame.display.set_icon(pygame.image.load("data/Icon.png"))
        self.UIstate = None
        self.GUI = {
            "EscapeUI" : [
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-145), (100, 50), "RENAME", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-85), (100, 50), "OPEN", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-25), (100, 50), "NEW", scale=self.settings["scale"]["GUI"]),
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+35), (100, 50), "DELETE", scale=self.settings["scale"]["GUI"]),
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+95), (100, 50), "Export as PDF", scale=self.settings["scale"]["GUI"]),
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+155), (100, 50), "SETTINGS", scale=self.settings["scale"]["GUI"])
            ],
            "OPENUI" : [],
            "NEWUI" : [
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+5), (100, 50), "", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-45), (100, 50), "Name:", scale=self.settings["scale"]["GUI"])
            ],
            "RENAMEUI" : [
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2+5), (100, 50), "", scale=self.settings["scale"]["GUI"]), 
                Objects.ClassButton((self.screen.get_size()[0]/2-50, self.screen.get_size()[1]/2-45), (100, 50), "Name:", scale=self.settings["scale"]["GUI"])
            ],
            "SETTINGSUI" : [
                Objects.ClassButtonSlider((self.screen.get_size()[0]/2, self.screen.get_size()[1]/2 - 85), (100, 50), 1, 3)
            ]

        }
        self.GUIRoomFill()
        json = JsonHandler.GetJson(self.settings["RoomFile"]).keys()
        if json:
            self.settings["CurrentRoom"] = next(iter(json))
            self.Room = JsonHandler.ReadRoom(self.settings["RoomFile"], self.settings["CurrentRoom"], self.FONT, self.settings["scale"])
        else:
            JsonHandler.CreateRoom(self.settings["RoomFile"], "Room1")
            self.changeRoom("Room1")
        self.mouse = Objects.ClassMouse()
        self.typingMode = [False, None]
        
    def GUIRoomFill(self):
        nr = 0
        self.GUI["OPENUI"] = []
        for room in JsonHandler.GetJson(self.settings["RoomFile"]).keys():
            self.GUI["OPENUI"].append(Objects.ClassButton((self.screen.get_size()[0]/2-50, 25*nr+50), (100, 20), room, scale=self.settings["scale"]["GUI"]))
            nr += 1     

    def changeRoom(self, RoomID):
        self.settings["CurrentRoom"] = RoomID
        self.Room = JsonHandler.ReadRoom(self.settings["RoomFile"], self.settings["CurrentRoom"], self.FONT, self.settings["scale"])

    def saveRoom(self):
        JsonHandler.WriteRoom(self.settings["RoomFile"], self.settings["CurrentRoom"], self.Room, self.settings["scale"])

    def NewRoom(self, ID):
        JsonHandler.CreateRoom(self.settings["RoomFile"], ID)

    def deleteRoom(self, ID):
        JsonHandler.RemoveRoom(self.settings["RoomFile"], ID)
    
    def renameRoom(self, ID, name):
        JsonHandler.RenameRoom(self.settings["RoomFile"], ID, name)

    def events(self):
        if pygame.event.get(QUIT, False):
            self.running = False
        if self.typingMode[0]:
            return
        for event in pygame.event.get(KEYDOWN, False):
            match event.key:
                case pygame.K_c:
                    self.Room["Seat"].append(self.create("Seat"))
                case pygame.K_r:
                    self.Room["RoundTable"].append(self.create("RoundTable"))
                case pygame.K_t:
                    self.Room["Table"].append(self.create("Table"))
                case pygame.K_d:
                    if self.deleteASeat():
                        continue
                    elif self.deleteATable():
                        continue
                    self.deleteARoundTable()
                case pygame.K_ESCAPE:
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

    def create(self, flag:str) -> object:
        match flag:
            case "Seat":
                return Objects.ClassSeat((self.mouse.pos[0], self.mouse.pos[1]), self.FONT["Seat"], scale=self.settings["scale"])
            case "Table":
                return Objects.ClassTable((self.mouse.pos[0], self.mouse.pos[1]), (100, 100), scale=self.settings["scale"]["table"])
            case "RoundTabel":
                return Objects.ClassRoundTable((self.mouse.pos[0], self.mouse.pos[1]), 150, scale=self.settings["scale"]["table"])
            case _:
                print("Func create() in app.py Flag Invalid", flag)
        
    def getHover(self) -> object:

        # Loose seats first
        for seat in self.Room["Seats"]:
            if mouseCircleCollision(self.mouse.pos, seat.rect.center, seat.diameter):
                return seat
            
        # Tables and their children
        for table in self.Room["Tables"]:
            #Table outer diameter
            outerDiameter = table.rect.size + 25*self.scale["seat"]

            if mouseCollision(self.mouse.pos, table.rect.topleft, outerDiameter):

                # Check children of table ( type : seats )  
                for seat in table.children:
                    if mouseCircleCollision(self.mouse.pos, seat.rect.center, seat.diameter):
                        return seat
                    
                # Check for the actual table 
                if mouseCollision(self.mouse.pos, table.rect.topleft, table.rect.size):
                    return table
        
        # Round tables and their children
        for table in self.Room["RoundTables"]:
            #Table outer diameter
            outerSize = [
                table.rect.width + 25*self.scale["seat"], 
                table.rect.height + 25*self.scale["seat"]
                ]
            
            if mouseCircleCollision(self.mouse.pos, table.rect.topleft, outerSize):

                # Check children of table ( type : seats )  
                for seat in table.children:
                    if mouseCircleCollision(self.mouse.pos, seat.rect.center, seat.diameter):
                        return seat
                    
                # Check for the actual table 
                if mouseCircleCollision(self.mouse.pos, table.rect.topleft, table.diameter):
                    return table
        return None
    def deleteASeat(self):
        for seat in self.Room["Seats"]:
            if mouseCircleCollision(self.mouse.pos, [seat.rect.x+seat.diameter/2, seat.rect.y+seat.diameter/2], seat.diameter):
                self.Room["Seats"].pop(self.Room["Seats"].index(seat))
                return 1
        return 0
    def deleteATable(self):
        for table in self.Room["Tables"]:
            if mouseCollision(self.mouse.pos, table.rect.topleft, table.rect.size):
                self.Room["Tables"].pop(self.Room["Tables"].index(table))
                return 1
        return 0
    def deleteARoundTable(self):
        for table in self.Room["RoundTables"]:
            if mouseCircleCollision(self.mouse.pos, table.rect.center, table.diameter):
                self.Room["RoundTables"].pop(self.Room["RoundTables"].index(table))
                return 1
        return 0

    def typingCheck(self):
        if self.mouse.holding[0] != None:
            return [False, None]
        e = pygame.event.get(MOUSEBUTTONDOWN, False)
        for event in e:
            #Check for left mouse button
            if event.button == 1:

                for seat in self.Room["Seats"]:
                    if mouseCircleCollision(self.mouse.pos, [seat.rect.x+seat.diameter/2, seat.rect.y+seat.diameter/2], seat.diameter):
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
        if not mouseCollision(self.mouse.pos, table.rect.topleft, table.rect.size):
            return self.mouse.holding
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        return [table, 
                mouseCollision(self.mouse.pos, [table.rect.x, table.rect.bottom - 10], [table.rect.w, 10]), 
                mouseCollision(self.mouse.pos, [table.rect.right-10, table.rect.y], [10, table.rect.h])]
        
    def followRoundCheck(self, table : Objects.ClassRoundTable) -> list:
        if not pygame.mouse.get_pressed(3)[0]:
            return [None, None, None]
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        if not mouseCircleCollision(self.mouse.pos, table.rect.center, table.diameter):
            return self.mouse.holding
        return [table,
                not mouseCircleCollision(self.mouse.pos, table.rect.center, table.diameter-10),
                None]

    def SeatFollowCheck(self, seat) -> list:
        
        if not pygame.mouse.get_pressed(3)[0]:
            return [None, None, None]
        if self.mouse.holding[0] != None:
            return self.mouse.holding
        if not mouseCircleCollision(self.mouse.pos, [seat.rect.x+seat.diameter/2, seat.rect.y+seat.diameter/2], seat.diameter):
            return self.mouse.holding

        return [seat, None, None]

    def ButtonCheck(self):
        if self.UIstate == "Escape":
            for button in self.GUI["EscapeUI"]:
                if not pygame.mouse.get_pressed(3)[0]:
                    continue
                if not mouseCollision(self.mouse.pos, button.rect.topleft, button.rect.size):
                    continue
                else:
                    self.UIstate = button.text
                    break
        if self.UIstate == "OPEN":
            for button in self.GUI["OPENUI"]:
                if not pygame.mouse.get_pressed(3)[0]:
                    continue
                if not mouseCollision(self.mouse.pos, button.rect.topleft, button.rect.size):
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
            table.draw(self.screen, self.FONT["Seat"])
        for table in self.Room["RoundTables"]:
            table.draw(self.screen, self.FONT["Seat"])
        for seat in self.Room["Seats"]:
            seat.draw(self.screen, self.FONT["Seat"])        
        self.Room["Tavla"].draw(self.screen, self.FONT["Tavla"])
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
    JsonHandler.WriteJson("data/Settings.json", app.settings)
    pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())