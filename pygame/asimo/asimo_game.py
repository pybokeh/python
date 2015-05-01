import pygame
import random

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)


# --- Classes
class Hunter(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load('hunter.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.going_right = True

    def update(self):
        """ Move head to the right or left depending on which side it bounced from"""
        if self.going_right:
            self.rect.x += 5
        else:
            self.rect.x -= 5

class Ford(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load('ford_logo_small.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.going_right = True

    def update(self):
        """ Move head to the right or left depending on which side it bounced from"""
        if self.going_right:
            self.rect.x += 5
        else:
            self.rect.x -= 5

class GM(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load('gm_logo_small.png').convert()
        #self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.going_right = True

    def update(self):
        """ Move head to the right or left depending on which side it bounced from"""
        if self.going_right:
            self.rect.x += 5
        else:
            self.rect.x -= 5

class Toyota(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load('toyota_logo_small.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.going_right = True

    def update(self):
        """ Move head to the right or left depending on which side it bounced from"""
        if self.going_right:
            self.rect.x += 5
        else:
            self.rect.x -= 5

class Hyundai(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load('hyundai_logo_small.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.going_right = True

    def update(self):
        """ Move head to the right or left depending on which side it bounced from"""
        if self.going_right:
            self.rect.x += 5
        else:
            self.rect.x -= 5

class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
        #self.image = pygame.Surface([20, 20])
        self.image = pygame.image.load('asimo.png').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0] - 50

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3

# --- Create the window
# Initialize Pygame
pygame.init()

click_sound = pygame.mixer.Sound('laser5.ogg')

# Set the height and width of the screen
screen_width  = 1200
screen_height = 675
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('My First ASIMO Pygame')

background_image = pygame.image.load('red_logo_1200_675.png').convert()

# --- Sprite lists
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites
for i in range(1):
    # This represents a block
    block = Hunter()

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height - 200)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

for i in range(1):
    # This represents a block
    block = Ford()

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height - 200)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

for i in range(1):
    # This represents a block
    block = GM()

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height - 200)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

for i in range(1):
    # This represents a block
    block = Toyota()

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height - 200)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

for i in range(1):
    # This represents a block
    block = Hyundai()

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height - 200)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a red player block
player = Player()
all_sprites_list.add(player)

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
bullet_count = 0
player.rect.y = 575

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
            # Fire a bullet if the user clicks the mouse button
            bullet = Bullet()
            click_sound.play()

            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x + 50
            bullet.rect.y = player.rect.y + 37

            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)

            bullet_count = bullet_count + 1
            print("Number of bullets fired: ", bullet_count)

    # --- Game logic
    # Call the update() method on all the sprites
    all_sprites_list.update()

    for block in block_list:
        if block.rect.x > 1150:
            block.going_right = False
        elif block.rect.x < 0:
            block.going_right = True

    # Calculate mechanics for each bullet
    for bullet in bullet_list:
        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            # score += 1
            # print(score)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    # --- Draw a frame
    # Clear the screen
    screen.fill(WHITE)

    screen.blit(background_image, [0,0])

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(80)
pygame.quit()
