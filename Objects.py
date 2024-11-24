import pygame, Objects, math
def mouseCollision(Ax, Ay, Bx, By, Bwidth, Bheight):
    return (Ax >= Bx and Ax <= Bx + Bwidth) and (Ay >= By and Ay <= Ay <= By + Bheight)
def mouseCircleCollision(Ax, Ay, Bc, Bd):
    Diffrence = [Bc[0]-Ax, Bc[1]-Ay]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2


def SeatRoundTableSnappCalc(Scenter, Tcenter, Tdiameter, snapp):
    O = Tdiameter * math.pi # circumfrance of table
    OpS = snapp * math.pi*2 /3 # distance between every seat position
    if O < OpS: # if there are less seat positions than seats return the spacing angle as 360 in radians
                # also helps to not divide by 0
        spaceing = math.pi*2
    else:
        spaceing = math.pi*2 / (O/OpS) # gives angle between seats
    x = (Scenter[0] - Tcenter[0]) 
    if x == 0: # So i dont divide by 0
        x = 0.00001
    y = (Scenter[1] - Tcenter[1])
    holdingAngle = math.atan2(abs(y), abs(x)) # should give the angle 
    
    
    if x < 0:
        holdingAngle = math.radians(180) - holdingAngle
    if y < 0: 
        holdingAngle = -holdingAngle
    holdingAngle = holdingAngle // spaceing * spaceing
    
    
    return [OpS, holdingAngle] 

class ClassTable : 
    def __init__(self, x, y, w, h) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        
        
    def draw(self, screen):
        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)
        
        screen.blit(self.surface, self.rect.topleft)

class ClassRoundTable:
    def __init__(self, x, y, d) -> None:
        self.rect = pygame.Rect(x, y, d, d)
        self.color = (0, 0, 0)
        self.diameter = d
    def draw(self, screen):
        self.surface = pygame.Surface((self.rect.w, self.rect.h)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surface, self.color, (self.diameter/2, self.diameter/2), self.diameter/2)
        screen.blit(self.surface, self.rect.topleft)

class ClassTavla : 
    def __init__(self, x, y, w, h, FONT) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.text = "TAVLAN"
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        
    def draw(self, screen, FONT):
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)
        pos = self.rect.w/2 - self.SurfaceText.get_size()[0]/2, self.rect.h/2 - self.SurfaceText.get_size()[1]/2
        self.surface.blit(self.SurfaceText, pos)
        
        screen.blit(self.surface, self.rect.topleft)

class ClassSeat:
    def __init__(self, x, y, FONT, parent=None, text="text") -> None:
        self.rect = pygame.rect.Rect(x, y, 40, 40)
        self.diameter = 40
        self.parentPos =[0, 0] 
        if parent:
            if type(parent) == Objects.ClassTable:
                self.parentPos = [x - parent.rect.x, y - parent.rect.y]
            if type(parent) == Objects.ClassRoundTable:
                self.parentPos = SeatRoundTableSnappCalc(self.rect.center, parent.rect.center, parent.diameter, 25)
                self.rect.center = [(math.cos(self.parentPos[1])*(parent.diameter/2)) + parent.rect.centerx,
                                    (math.sin(self.parentPos[1])*(parent.diameter/2)) + parent.rect.centery]
        self.colorOG = (175, 175, 175)
        self.color = self.colorOG
        self.text = text
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.parent = parent

    def draw(self, drawsurface, FONT):
        if self.parent:
            if type(self.parent) == ClassTable:
                self.rect.x = self.parentPos[0] + self.parent.rect.x
                self.rect.y = self.parentPos[1] + self.parent.rect.y
                if self.parentPos[0] > self.parent.rect.w:
                    self.parent = None
                elif self.parentPos[1] > self.parent.rect.h:
                    self.parent = None

            if type(self.parent) == ClassRoundTable:
                self.parentPos = SeatRoundTableSnappCalc(self.rect.center, self.parent.rect.center, self.parent.diameter, 25)
                self.rect.centerx = math.cos(self.parentPos[1]) * (self.parent.diameter/2) + self.parent.rect.center[0]
                self.rect.centery = math.sin(self.parentPos[1]) * (self.parent.diameter/2) + self.parent.rect.center[1]
                

        self.SurfaceText : pygame.Surface = FONT.render(self.text, True, (255, 255, 255))
        
        self.surface = pygame.surface.Surface((self.diameter, self.diameter)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        
        pygame.draw.circle(self.surface, self.color, (self.diameter/2, self.diameter/2), self.diameter/2)
        
        pos = self.diameter/2 - self.SurfaceText.get_size()[0]/2, self.diameter/2 - self.SurfaceText.get_size()[1]/2
        self.surface.blit(self.SurfaceText, pos)
        
        drawsurface.blit(self.surface, self.rect.topleft)
        self.color = self.colorOG
class ClassMouse:
    def __init__(self):
        self.pos = pygame.mouse.get_pos()
        self.holding = [None, None, None]
        self.buttons = pygame.mouse.get_pressed(3)
    def update(self, tables, roundTables):
        self.pos = pygame.mouse.get_pos()
        self.buttons = pygame.mouse.get_pressed(3)
        self.holdingUpdate(tables, roundTables)

    def holdingUpdate(self, tables, roundTables):
        if self.holding[0] == None:
            return
        tableSnapp = 50
        gridSnapp = 25
        if type(self.holding[0]) == Objects.ClassTable:
            if not self.holding[1] and not self.holding[2]:

                self.holding[0].rect.x = (self.pos[0] - self.holding[0].rect.w/2+gridSnapp/2) //gridSnapp *gridSnapp
                self.holding[0].rect.y = (self.pos[1] - self.holding[0].rect.h/2+gridSnapp/2) //gridSnapp *gridSnapp
            
            if self.holding[1]:
                self.holding[0].rect.h = (self.pos[1] - self.holding[0].rect.y+tableSnapp/2) //tableSnapp *tableSnapp
                if self.holding[0].rect.h <= tableSnapp:
                    self.holding[0].rect.h = tableSnapp
            
            if self.holding[2]:
                self.holding[0].rect.w = (self.pos[0] - self.holding[0].rect.x+tableSnapp/2) //tableSnapp *tableSnapp
                if self.holding[0].rect.w <= tableSnapp:
                    self.holding[0].rect.w = tableSnapp
        if type(self.holding[0]) == Objects.ClassTavla:
            if not self.holding[1] and not self.holding[2]:

                self.holding[0].rect.x = (self.pos[0] - self.holding[0].rect.w/2+gridSnapp/2) //gridSnapp *gridSnapp
                self.holding[0].rect.y = (self.pos[1] - self.holding[0].rect.h/2+gridSnapp/2) //gridSnapp *gridSnapp
            
            if self.holding[1]:
                self.holding[0].rect.h = (self.pos[1] - self.holding[0].rect.y+gridSnapp/2) //gridSnapp *gridSnapp
                if self.holding[0].rect.h <= gridSnapp:
                    self.holding[0].rect.h = gridSnapp
            
            if self.holding[2]:
                self.holding[0].rect.w = (self.pos[0] - self.holding[0].rect.x+gridSnapp/2) //gridSnapp *gridSnapp
                if self.holding[0].rect.w <= gridSnapp:
                    self.holding[0].rect.w = gridSnapp
        if type(self.holding[0]) == Objects.ClassRoundTable:
            if not self.holding[1]:
                self.holding[0].rect.x = (self.pos[0] - self.holding[0].rect.w/2+gridSnapp/2) //gridSnapp *gridSnapp
                self.holding[0].rect.y = (self.pos[1] - self.holding[0].rect.h/2+gridSnapp/2) //gridSnapp *gridSnapp
            else:
                diametercalk = (math.sqrt((self.holding[0].rect.center[0]-self.pos[0])**2 + (self.holding[0].rect.center[1]-self.pos[1])**2)*2)//gridSnapp *gridSnapp
                center = self.holding[0].rect.center
                self.holding[0].diameter = diametercalk
                self.holding[0].rect.w = diametercalk
                self.holding[0].rect.h = diametercalk
                self.holding[0].rect.center = center


        if type(self.holding[0]) == Objects.ClassSeat:

            self.holding[0].rect.x = (self.pos[0] - self.holding[0].diameter/2+gridSnapp/2)//gridSnapp *gridSnapp
            self.holding[0].rect.y = (self.pos[1] - self.holding[0].diameter/2+gridSnapp/2)//gridSnapp *gridSnapp
            self.holding[0].parent = None
            for table in tables:
                if not mouseCollision(self.pos[0], self.pos[1], table.rect.x, table.rect.y, table.rect.w, table.rect.h):
                    continue
                if self.pos[0] < table.rect.x + 15:
                    self.holding[0].rect.x = table.rect.x - self.holding[0].diameter/2
                    if table.rect.h > tableSnapp:
                        self.holding[0].rect.y = (self.holding[0].rect.y) // tableSnapp * tableSnapp +table.rect.y%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.y = table.rect.y + table.rect.h/2 - self.holding[0].diameter/2
                elif self.pos[0] > table.rect.right-15:
                    self.holding[0].rect.x = table.rect.right - self.holding[0].diameter/2
                    if table.rect.h > tableSnapp:
                        self.holding[0].rect.y = (self.holding[0].rect.y) // tableSnapp * tableSnapp +table.rect.y%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.y = table.rect.y + table.rect.h/2 - self.holding[0].diameter/2
                if self.pos[1] < table.rect.y + 15:
                    self.holding[0].rect.y = table.rect.y - self.holding[0].diameter/2
                    if table.rect.w > tableSnapp:
                        self.holding[0].rect.x = (self.holding[0].rect.x) // tableSnapp * tableSnapp +table.rect.x%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.x = table.rect.x + table.rect.w/2 - self.holding[0].diameter/2
                elif self.pos[1] > table.rect.bottom-15:
                    self.holding[0].rect.y = table.rect.bottom - self.holding[0].diameter/2
                    if table.rect.w > tableSnapp:
                        self.holding[0].rect.x = (self.holding[0].rect.x) // tableSnapp * tableSnapp +table.rect.x%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.x = table.rect.x + table.rect.w/2 - self.holding[0].diameter/2
                self.holding[0].parentPos[0] = self.holding[0].rect.x - table.rect.x
                self.holding[0].parentPos[1] = self.holding[0].rect.y - table.rect.y
                self.holding[0].parent = table
            
            for table in roundTables:
                if not mouseCircleCollision(self.pos[0], self.pos[1], table.rect.center, table.diameter):
                    continue
                if not mouseCircleCollision(self.pos[0], self.pos[1], table.rect.center, table.diameter-75):
                    self.holding[0].parent = table
                    self.holding[0].parentPos = SeatRoundTableSnappCalc(self.holding[0].rect.center, table.rect.center, table.diameter, gridSnapp)    
                    
                    self.holding[0].parent = table