import pygame


class ClassTable : 
    def __init__(self, x, y, w, h, FONT) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.text = "test"
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
    def draw(self, screen, FONT):
        self.SurfaceText = FONT.render(self.text, True, (255, 255, 255))
        self.surface = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.color)
        self.surface.blit(self.SurfaceText, (5, 5))
        screen.blit(self.surface, self.rect.topleft)
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

            if not self.holding[1] and not self.holding[2]:

                self.holding[0].rect.x = (self.pos[0] - self.holding[0].rect.w/2+12.5) //25 *25
                self.holding[0].rect.y = (self.pos[1] - self.holding[0].rect.h/2+12.5) //25 *25
            
            if self.holding[1]:
                self.holding[0].rect.h = (self.pos[1] - self.holding[0].rect.y+12.5) //25 *25
            
            if self.holding[2]:
                self.holding[0].rect.w = (self.pos[0] - self.holding[0].rect.x+12.5) //25 *25

            
        