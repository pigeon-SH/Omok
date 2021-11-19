import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = [400, 300]
screen = pygame.display.set_mode(size)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Drawing Circle")

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창 닫을 때
            done = True
    screen.fill(WHITE)  # background color
    pygame.draw.circle(screen, BLACK, [60, 250], 40, 2) # (scree, color, position, radius, only outline)
    pygame.draw.circle(screen, BLACK, [60, 100], 40)    # fill inside
    pygame.display.flip()   # draw screen



pygame.quit()