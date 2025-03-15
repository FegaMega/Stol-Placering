from Component import *

manager = Manager()

pygame.init()

font = pygame.font.SysFont("Helvetica", 20)


Objects = {
   "People" : [],
   "Tables" : []
}

screen = pygame.display.set_mode((700, 700))
r = True
while r:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         r = False

   #draw
   screen.fill((0, 0, 0))

      
   pygame.display.update()
   pygame.time.Clock().tick(60)