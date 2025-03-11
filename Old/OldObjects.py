import pygame, Old.OldObjects as OldObjects, math

def mouseCollision(Ax, Ay, Bx, By, Bwidth, Bheight):
    return (Ax >= Bx and Ax <= Bx + Bwidth) and (Ay >= By and Ay <= Ay <= By + Bheight)

def mouseCircleCollision(Ax, Ay, Bc, Bd):
    Diffrence = [Bc[0]-Ax, Bc[1]-Ay]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2

def Snap(i: float, s : int) -> int:
    return i //s *s 

def GetAngle(Pos : tuple, Origin : tuple):

        x = (Pos[0] - Origin[0])
        if x == 0:
            x = 0.00001
        y = (Pos[1] - Origin[1])
        Angle = math.atan2(abs(y), abs(x)) 
        if x < 0:
            Angle = -Angle
            Angle -= math.radians(180)
        if y < 0: 
            Angle = -Angle
        return Angle

def GetPos(angle, radius):
    return [
            (math.cos(angle)*radius) + radius,
            (math.sin(angle)*radius) + radius
            ]





class ClassTable : 
    def __init__(self, Pos, Size, children=[], scale=1) -> None:
        self.rect = pygame.Rect(Pos[0] *scale, Pos[1] *scale, Size[0] *scale, Size[1] *scale)
        self.color = (0, 0, 0)
        self.children = children 
        
    def draw(self, screen, FONT):
        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)
        
        screen.blit(self.surface, self.rect.topleft)

        for child in self.children:
            child.draw(screen, FONT)





class ClassRoundTable:
    def __init__(self, Pos:list, d, children=[], scale=1) -> None:
        
        self.rect = pygame.Rect((Pos[0]*scale), (Pos[1]*scale), (d*scale), (d*scale))
        self.color = (0, 0, 0)
        self.diameter = d*scale
        self.children = children

    def draw(self, screen, FONT):
        self.surface = pygame.Surface((self.rect.w, self.rect.h)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surface, self.color, (self.diameter/2, self.diameter/2), self.diameter/2)
        screen.blit(self.surface, self.rect.topleft)
        for child in self.children:
            child.draw(screen, FONT)





class ClassButton:
    def __init__(self, Pos, Size, FuncText, color=(50, 50, 50), scale=1, text="") -> None:
        self.rect = pygame.Rect((Pos[0]*scale), (Pos[1]*scale), (Size[0]*scale), (Size[1]*scale))
        self.color = color
        self.FuncText = FuncText
        if text != "":
            self.text = FuncText
        else:
            self.text = FuncText            
        self.pressed = False

    def draw(self, screen, FONT):
        
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))

        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)
        pos = self.rect.w/2 - self.SurfaceText.get_size()[0]/2, self.rect.h/2 - self.SurfaceText.get_size()[1]/2
        self.surface.blit(self.SurfaceText, pos)
        
        screen.blit(self.surface, self.rect.topleft)





class ClassButtonSlider:
    def __init__(self, Pos, Size, value, maxvalue, color=(50, 50, 50), scale=1) -> None:
        self.rect = pygame.Rect((Pos[0]*scale), (Pos[1]*scale), (Size[0]*scale), (Size[1]*scale))
        self.color = color
        self.value = value         
        self.maxvalue = maxvalue
        self.pressed = False
        self.scale =scale
        self.SliderRect = pygame.Rect(10, 10, 10*scale, 10*scale)
    def draw(self, screen, FONT):

        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)

        self.SliderRect.center = (self.value*((self.rect.width-20*self.scale)*self.scale)/self.maxvalue, self.rect.h/2 - 10*self.scale)
        pygame.draw.circle(self.surface,(0, 0, 0), self.SliderRect.center, self.SliderRect.w)
        
        self.SurfaceText = FONT.render(str(self.value), True, (255, 255, 255))
        pos = self.rect.w/2 - self.SurfaceText.get_size()[0]/2, self.rect.h/2 - self.SurfaceText.get_size()[1]/2+10*self.scale
        self.surface.blit(self.SurfaceText, pos)

        screen.blit(self.surface, self.rect.topleft)





class ClassTavla : 
    def __init__(self, Pos, Size, FONT, scale) -> None:
        self.rect = pygame.Rect((Pos[0]*scale), (Pos[1]*scale), (Size[0]*scale), (Size[1]*scale))
        self.color = (0, 0, 0)
        self.text = "TAVLAN"
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.children = []

    def draw(self, screen, FONT):
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)
        pos = self.rect.w/2 - self.SurfaceText.get_size()[0]/2, self.rect.h/2 - self.SurfaceText.get_size()[1]/2
        self.surface.blit(self.SurfaceText, pos)
        
        screen.blit(self.surface, self.rect.topleft)





class ClassSeat:
    def __init__(self, Pos, FONT, parent=None, text="text", scale:dict={}) -> None:
        self.diameter = 40 * scale["seat"]
        self.scale = scale
        self.rect = pygame.rect.Rect(0, 0, self.diameter, self.diameter)
        self.rect.center = Pos
        if parent:
            if type(parent) == OldObjects.ClassTable:
                self.parentPos = [self.rect.centerx - parent.rect.x, self.rect.centery - parent.rect.y]
            elif type(parent) == OldObjects.ClassRoundTable:
                self.parentPos = [parent.diameter, GetAngle(self.rect.center, self.parent.rect.center)]
        else:
            self.parentPos = [0, 0]
        self.colorOG = (175, 175, 175)
        self.color = self.colorOG
        self.text = text
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.parent = parent

    def draw(self, drawsurface, FONT):
        if self.parent:
            if type(self.parent) == ClassTable:
                self.rect.centerx = self.parentPos[0] + self.parent.rect.x
                self.rect.centery = self.parentPos[1] + self.parent.rect.y
                if self.parentPos[0] > self.parent.rect.w:
                    self.parent = None
                elif self.parentPos[1] > self.parent.rect.h:
                    self.parent = None
            if type(self.parent) == ClassRoundTable:
                Pos = GetPos(self.parentPos[1], self.parent.diameter/2)
                self.rect.centerx = Pos[0] + self.parent.rect.center[0]
                self.rect.centery = Pos[1] + self.parent.rect.center[1]
                

        self.SurfaceText : pygame.Surface = FONT.render(self.text, True, (255, 255, 255))
        
        self.surface = pygame.surface.Surface((self.diameter, self.diameter)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))
        
        pygame.draw.circle(self.surface, self.color, (self.diameter/2, self.diameter/2), self.diameter/2)
        if self.SurfaceText.get_size()[0] > self.diameter:
            self.SurfaceText = pygame.transform.smoothscale(self.SurfaceText, [self.diameter, self.SurfaceText.get_size()[1]])
        pos = self.diameter/2 - self.SurfaceText.get_size()[0]/2, self.diameter/2 - self.SurfaceText.get_size()[1]/2
        self.surface.blit(self.SurfaceText, pos)
        
        drawsurface.blit(self.surface, self.rect)
        self.color = self.colorOG





class ClassMouse:
    def __init__(self):
        self.pos = pygame.mouse.get_pos()
        self.holding = [None, None, None]
        self.buttons = pygame.mouse.get_pressed(3)

    def update(self, tables, roundTables, scale):
        self.pos = pygame.mouse.get_pos()
        self.buttons = pygame.mouse.get_pressed(3)
        self.holdingUpdate(tables, roundTables, scale)

    def holdingUpdate(self, tables, roundTables, scale):
        if self.holding[0] == None:
            return
        tableSnapp = 50*scale["table"]
        gridSnapp = 25*scale["table"]
        if type(self.holding[0]) == OldObjects.ClassTable:
            if not self.holding[1] and not self.holding[2]:

                self.holding[0].rect.x = Snap(self.pos[0] - self.holding[0].rect.w/2+gridSnapp/2, gridSnapp)
                self.holding[0].rect.y = Snap(self.pos[1] - self.holding[0].rect.h/2+gridSnapp/2, gridSnapp)
            
            if self.holding[1]:
                self.holding[0].rect.h = Snap(self.pos[1] - self.holding[0].rect.y+tableSnapp/2, tableSnapp)
                if self.holding[0].rect.h <= tableSnapp:
                    self.holding[0].rect.h = tableSnapp
            
            if self.holding[2]:
                self.holding[0].rect.w = Snap(self.pos[0] - self.holding[0].rect.x+tableSnapp/2, tableSnapp)
                if self.holding[0].rect.w <= tableSnapp:
                    self.holding[0].rect.w = tableSnapp
        if type(self.holding[0]) == OldObjects.ClassTavla:
            if not self.holding[1] and not self.holding[2]:

                self.holding[0].rect.x = Snap(self.pos[0] - self.holding[0].rect.w/2+gridSnapp/2, gridSnapp)
                self.holding[0].rect.y = Snap(self.pos[1] - self.holding[0].rect.h/2+gridSnapp/2, gridSnapp)
            
            if self.holding[1]:
                self.holding[0].rect.h = Snap(self.pos[1] - self.holding[0].rect.y+gridSnapp/2, gridSnapp)
                if self.holding[0].rect.h <= gridSnapp:
                    self.holding[0].rect.h = gridSnapp
            
            if self.holding[2]:
                self.holding[0].rect.w = Snap(self.pos[0] - self.holding[0].rect.x+gridSnapp/2, gridSnapp)
                if self.holding[0].rect.w <= gridSnapp:
                    self.holding[0].rect.w = gridSnapp

        if type(self.holding[0]) == OldObjects.ClassRoundTable:
            if not self.holding[1]:
                self.holding[0].rect.x = Snap(self.pos[0] - self.holding[0].rect.w/2+gridSnapp/2, gridSnapp)
                self.holding[0].rect.y = Snap(self.pos[1] - self.holding[0].rect.h/2+gridSnapp/2, gridSnapp)
            else:
                diametercalk = Snap(math.sqrt((self.holding[0].rect.center[0]-self.pos[0])**2 + (self.holding[0].rect.center[1]-self.pos[1])**2)*2, gridSnapp)
                center = self.holding[0].rect.center
                self.holding[0].diameter = diametercalk
                self.holding[0].rect.w = diametercalk
                self.holding[0].rect.h = diametercalk
                self.holding[0].rect.center = center


        if type(self.holding[0]) == OldObjects.ClassSeat:

            self.holding[0].rect.x = Snap(self.pos[0] - self.holding[0].diameter/2+gridSnapp/2, gridSnapp)
            self.holding[0].rect.y = Snap(self.pos[1] - self.holding[0].diameter/2+gridSnapp/2, gridSnapp)
            self.holding[0].parent = None
            for table in tables:
                if not mouseCollision(self.pos[0], self.pos[1], table.rect.x, table.rect.y, table.rect.w, table.rect.h):
                    continue
                if self.pos[0] < table.rect.x + 15:
                    self.holding[0].rect.x = table.rect.x - self.holding[0].diameter/2
                    if table.rect.h > tableSnapp:
                        self.holding[0].rect.y = Snap(self.holding[0].rect.y, tableSnapp) +table.rect.y%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.y = table.rect.y + table.rect.h/2 - self.holding[0].diameter/2
                elif self.pos[0] > table.rect.right-15:
                    self.holding[0].rect.x = table.rect.right - self.holding[0].diameter/2
                    if table.rect.h > tableSnapp:
                        self.holding[0].rect.y = Snap(self.holding[0].rect.y, tableSnapp) +table.rect.y%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.y = table.rect.y + table.rect.h/2 - self.holding[0].diameter/2
                if self.pos[1] < table.rect.y + 15:
                    self.holding[0].rect.y = table.rect.y - self.holding[0].diameter/2
                    if table.rect.w > tableSnapp:
                        self.holding[0].rect.x = Snap(self.holding[0].rect.x, tableSnapp) +table.rect.x%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.x = table.rect.x + table.rect.w/2 - self.holding[0].diameter/2
                elif self.pos[1] > table.rect.bottom-15:
                    self.holding[0].rect.y = table.rect.bottom - self.holding[0].diameter/2
                    if table.rect.w > tableSnapp:
                        self.holding[0].rect.x = Snap(self.holding[0].rect.x, tableSnapp) +table.rect.x%tableSnapp + (tableSnapp-self.holding[0].diameter)/2
                    else:
                        self.holding[0].rect.x = table.rect.x + table.rect.w/2 - self.holding[0].diameter/2
                self.holding[0].parentPos[0] = self.holding[0].rect.centerx - table.rect.x
                self.holding[0].parentPos[1] = self.holding[0].rect.centery - table.rect.y
                self.holding[0].parent = table
            
            for table in roundTables:
                if not mouseCircleCollision(self.pos[0], self.pos[1], table.rect.center, table.diameter):
                    continue
                if not mouseCircleCollision(self.pos[0], self.pos[1], table.rect.center, table.diameter-75):
                    holdingAngle = GetAngle(self.pos, table.rect.center)
                    pos = GetPos(holdingAngle, table.diameter/2)
                    self.holding[0].pos = [
                        pos[0] + table.diameter/2,
                        pos[1] + table.diameter/2
                    ] 
                    
                    self.holding[0].parent = table
                    self.holding[0].parentPos = [table.diameter, holdingAngle]
                
