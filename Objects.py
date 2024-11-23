import pygame, Objects


class ClassTable : 
    def __init__(self, x, y, w, h, FONT) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.text = "test"
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.Seats = [ClassSeat(25, 25, FONT, self)]
    def draw(self, screen, FONT):
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)
        self.surface.blit(self.SurfaceText, (5, 5))
        for seat in self.Seats:
            seat.draw(self.surface, FONT)
        screen.blit(self.surface, self.rect.topleft)

class ClassSeat:
    def __init__(self, x, y, FONT, parent) -> None:
        self.pos = [x, y]
        self.diameter = 40
        self.color = (175, 175, 175)
        self.text = "text"
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.parent = parent

    def draw(self, drawsurface, FONT):

        self.SurfaceText : pygame.Surface = FONT.render(self.text, True, (255, 255, 255))
        
        self.surface = pygame.surface.Surface((self.diameter, self.diameter))
        
        pygame.draw.circle(self.surface, self.color, (self.diameter/2, self.diameter/2), self.diameter/2)
        
        pos = self.diameter/2 - self.SurfaceText.get_size()[0]/2, self.diameter/2 - self.SurfaceText.get_size()[1]/2
        self.surface.blit(self.SurfaceText, pos)
        
        drawsurface.blit(self.surface, self.pos)
class ClassMouse:
    def __init__(self):
        self.pos = pygame.mouse.get_pos()
        self.holding = [None, None, None]
        self.buttons = pygame.mouse.get_pressed(3)
    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.buttons = pygame.mouse.get_pressed(3)
        self.holdingUpdate()

    def holdingUpdate(self):
        if self.holding[0] != None:
            if type(self.holding[0]) == Objects.ClassTable:
                if not self.holding[1] and not self.holding[2]:

                    self.holding[0].rect.x = (self.pos[0] - self.holding[0].rect.w/2+12.5) //25 *25
                    self.holding[0].rect.y = (self.pos[1] - self.holding[0].rect.h/2+12.5) //25 *25
                
                if self.holding[1]:
                    self.holding[0].rect.h = (self.pos[1] - self.holding[0].rect.y+12.5) //25 *25
                    if self.holding[0].rect.h <= 25:
                        self.holding[0].rect.h = 25
                
                if self.holding[2]:
                    self.holding[0].rect.w = (self.pos[0] - self.holding[0].rect.x+12.5) //25 *25
                    if self.holding[0].rect.w <= 25:
                        self.holding[0].rect.w = 25
            if type(self.holding[0]) == Objects.ClassSeat:

                self.holding[0].pos[0] = (self.pos[0] - self.holding[0].parent.rect.x - self.holding[0].diameter/2)
                self.holding[0].pos[1] = (self.pos[1] - self.holding[0].parent.rect.y - self.holding[0].diameter/2)
        