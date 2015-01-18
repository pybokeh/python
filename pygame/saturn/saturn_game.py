import pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0 , 0)

SIZE = (800, 600)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('My First Saturn Pygame')
background_image = pygame.image.load('saturn_family.jpg').convert()
player1_image    = pygame.image.load('playerShip1_orange.png').convert()
player1_image.set_colorkey(BLACK)
click_sound = pygame.mixer.Sound('laser5.ogg')

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
            click_sound.play()

    player_position = pygame.mouse.get_pos()
    x = player_position[0]
    y = player_position[1]

    screen.blit(background_image, [0,0])
    screen.blit(player1_image, [x-50,y-37])
    

    # Limit to 60 frames per second
    clock.tick(120)
    
    # Go ahead and update the screen with what we've drawn
    pygame.display.update()
