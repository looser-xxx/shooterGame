# Import the necessary modules from the Python Standard Library
from os import path
import pygame
import random

# Import a custom module that contains game-wide settings and variables
import gameSettings as gS


def loadingAssets(fileName):
    # This function loads an image file from the 'images' directory.
    # It ensures the path is correct regardless of the operating system.

    # Construct the file path to the image
    image_path = path.join(path.dirname('main.py'), '..', 'images', fileName)

    # Load the image and convert it for faster biting with transparency.
    return pygame.image.load(image_path).convert_alpha()


def randGenForProb(n):
    return n
    # n*=1000
    # randSmall=n-gS.randomProbability/100*n
    # randLarge=n+gS.randomProbability/100*n
    # randomValue=random.randint(int(randSmall), int(randLarge))
    # return randomValue/1000

class Shooter:
    def __init__(self):
        # Initialize Pygame and set up the main game window
        self.gameScore = 0
        pygame.init()
        self.running = True  # Controls the main game loop
        self.clock = pygame.time.Clock()  # Manages game speed (FPS)

        # Set up the display surface for drawing
        self.screenColor = gS.screenColor
        self.displaySurface = pygame.display.set_mode(gS.screenSize)

        # Create game objects by loading assets and initializing their classes
        self.stars = Stars(loadingAssets('star.png'))
        self.player = Player(loadingAssets('player.png'))
        self.ui = UI(loadingAssets('sideBars.png'))
        self.sfx = Sound()

        # Create sprite groups to manage different types of objects
        self.lasers = pygame.sprite.Group()  # Group for laser sprites
        self.meteors = pygame.sprite.Group()  # Group for meteor sprites
        self.ammoG = pygame.sprite.Group()
        self.healthG = pygame.sprite.Group()
        self.lifeG= pygame.sprite.Group()


        # Create a master group for all sprites to simplify updates and drawing
        self.allSprites = pygame.sprite.Group()

        # Add initial game objects to the master sprite group
        self.allSprites.add(self.stars)
        self.allSprites.add(self.player)

        # Meteor spawning timer
        self.meteorTimer = 0

        # Ammo of the spaceShip
        self.ammo = gS.ammo
        self.ammoTimer = 0
        self.healthTimer = 0
        self.lifeTimer=0

    def spawnMeteor(self):
        # Randomize the starting x-position
        x = random.randint(gS.playSpace[0], gS.playSpace[1])
        # The meteor starts just above the screen
        y = gS.droppingSpawnPosition
        # Create a new meteor instance
        newMeteor = Meteor(loadingAssets('meteor.png'), x, y)
        # Add the meteor to both the meteors group and the main group
        self.meteors.add(newMeteor)
        self.allSprites.add(newMeteor)

    def spawnAmmo(self):
        # Randomize the starting x-position
        x = random.randint(gS.playSpace[0], gS.playSpace[1])
        # The meteor starts just above the screen
        y = gS.droppingSpawnPosition
        # Create a new meteor instance
        newAmmo = Ammo(loadingAssets('ammo.png'), x, y)
        # Add the meteor to both the meteors group and the main group
        self.ammoG.add(newAmmo)
        self.allSprites.add(newAmmo)

    def spawnHealth(self):
        # Randomize the starting x-position
        x = random.randint(gS.playSpace[0], gS.playSpace[1])
        # The meteor starts just above the screen
        y = gS.droppingSpawnPosition
        # Create a new meteor instance
        newHealth = Health(loadingAssets('health.png'), x, y)
        # Add the meteor to both the meteors group and the main group
        self.healthG.add(newHealth)
        self.allSprites.add(newHealth)

    def spawnLife(self):
        # Randomize the starting x-position
        x = random.randint(gS.playSpace[0], gS.playSpace[1])
        y = gS.droppingSpawnPosition
        # Create a new meteor instance
        newLife = Health(loadingAssets('life.png'), x, y)
        # Add the meteor to both the meteors group and the main group
        self.lifeG.add(newLife)
        self.allSprites.add(newLife)



    def draw(self):
        # Fills the entire screen with a solid color to erase the previous frame.
        self.displaySurface.fill(self.screenColor)
        # self.displaySurface.blit(loadingAssets('background.png'), self.displaySurface.get_rect())

        # Draws the star background. We draw this first so other objects appear on top.
        self.stars.draw(self.displaySurface)

        # Manually iterate through all sprites to handle custom drawing logic.
        for sprite in self.allSprites:
            # Check if the sprite has a custom 'draw' method.
            if hasattr(sprite, 'draw'):
                # If it does, call that custom method (e.g., for the Player's health bar).
                sprite.draw(self.displaySurface)
            else:
                # If it does not, just use the standard blit to draw the sprite's image.
                self.displaySurface.blit(sprite.image, sprite.rect)

        self.displaySurface.blit(self.ui.image, (0, 0))
        self.ui.draw(
                    self.displaySurface,
                    self.gameScore,
                    self.player.health,
                    self.ammo
                    )



    def handleEvents(self, dt):
        # Process all events in the Pygame event queue.
        for event in pygame.event.get():
            # Check if the user clicked the 'X' to close the window.
            if event.type == pygame.QUIT:
                self.running = False

            # Check for a mouse button press
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the left mouse button (button 1) is pressed.
                if event.button == 1 and self.ammo > 0:
                    self.sfx.play('laser')
                    self.ammo -= 1
                    # Create a new laser instance at the player's position.a
                    laser = Laser(
                        loadingAssets('laser.png'),
                        self.player.rect.centerx,
                        self.player.rect.top
                    )
                    # Add the new laser to both the lasers group and the main sprite group.
                    self.lasers.add(laser)
                    self.allSprites.add(laser)

        # Check for pressed keyboard keys to handle continuous player movement.
        if gS.mouse:
            self.player.rect.center=pygame.mouse.get_pos()
        else:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move('w', dt)
            if keys[pygame.K_s]:
                self.player.move('s', dt)
            if keys[pygame.K_a]:
                self.player.move('a', dt)
            if keys[pygame.K_d]:
                self.player.move('d', dt)

    def collision(self, collisionType):
        match collisionType:
            case 'ammo':
                self.sfx.play('ammo')
                self.ammo += gS.ammoIncrement

            case 'laser':
                self.sfx.play('explosion')

            case 'player':
                self.sfx.play('damage')
                self.player.health -= gS.healthLossByCollision
                if self.player.health <= 0:
                    self.running = False

            case 'health':
                if self.player.health <= 0:
                    self.running = False
                self.sfx.play('health')
                self.player.health += gS.healthIncrement
                if self.player.health > 100:
                    self.player.health =100

            case 'life':
                self.sfx.play('life')
                self.player.health = 100

            case _:  # This is the default case, like in a switch
                print(f"Warning: Unknown collision type '{collisionType}'")

    def boundary(self):
        # This function prevents the player from moving off-screen.

        # Restrict the player's vertical movement to stay within the screen bounds.
        if self.player.rect.top < 0:
            self.player.rect.top = 0
        if self.player.rect.bottom > gS.screenHeight:
            self.player.rect.bottom = gS.screenHeight

        # Restrict the player's horizontal movement to stay within the screen bounds.
        if self.player.rect.left < gS.playSpace[0]:
            self.player.rect.left = gS.playSpace[0]
        if self.player.rect.right > gS.playSpace[1]:
            self.player.rect.right = gS.playSpace[1]

    def run(self):
        # This is the main game loop that keeps the game running.
        self.sfx.play('bgm')
        while self.running:
            # Calculate the time elapsed since the last frame.
            # This is essential for frame-rate independent movement.
            dt = self.clock.tick(gS.fps) / 1000
            self.gameScore += dt
            # Update the meteor timer



            self.meteorTimer += dt
            if self.meteorTimer >= randGenForProb(gS.meteorSpawnRate):
                self.spawnMeteor()  # Call the spawn method when the timer runs out.
                self.meteorTimer = 0  # Reset the timer.

            self.ammoTimer += dt
            if self.ammoTimer >= randGenForProb(gS.ammoSpawnRate):
                self.spawnAmmo()
                self.ammoTimer = 0

            self.healthTimer += dt
            if self.healthTimer >= randGenForProb(gS.healthSpawnRate):
                self.spawnHealth()
                self.healthTimer = 0

            self .lifeTimer += dt
            if self.lifeTimer >= randGenForProb(gS.lifeSpawnRate):
                self.spawnLife()
                self.lifeTimer = 0





            # Handle all user inputs and events (e.g., keyboard, mouse clicks).
            self.handleEvents(dt)

            # Update the state of all sprites in the game (e.g., movement, animation).
            self.allSprites.update(dt)

            playerCollision = pygame.sprite.spritecollide(self.player,
                                                          self.meteors,
                                                          True,
                                                          pygame.sprite.collide_mask
                                                          )
            # Check for collisions between lasers and meteors.
            laserCollision = pygame.sprite.groupcollide(self.lasers,
                                                        self.meteors,
                                                        True,
                                                        True,
                                                        pygame.sprite.collide_mask
                                                        )
            ammoCollision = pygame.sprite.spritecollide(self.player,
                                                        self.ammoG,
                                                        True,
                                                        pygame.sprite.collide_mask
                                                        )
            healthCollision = pygame.sprite.spritecollide(self.player,
                                                        self.healthG,
                                                        True,
                                                        pygame.sprite.collide_mask
                                                        )
            lifeCollision = pygame.sprite.spritecollide(self.player,
                                                        self.lifeG,
                                                        True,
                                                        pygame.sprite.collide_mask
                                                        )

            if playerCollision:
                self.collision('player')
            if laserCollision:
                self.collision('laser')
            if ammoCollision:
                self.collision('ammo')
            if healthCollision and self.player.health != 100:
                self.collision('health')
            if lifeCollision and self.player.health != 100:
                self.collision('life')

            # Draw all the game objects to the screen.
            self.draw()

            # Ensure the player stays within the game screen.
            self.boundary()

            # Update the full display Surface to the screen.
            pygame.display.flip()


class Stars(pygame.sprite.Sprite):
    def __init__(self, image):
        # Initializes the Stars sprite.
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.randStarPose = []  # A list to hold the random positions of the stars.

    def starPose(self):
        # Generates a set of random positions for the stars.
        # It uses a fixed seed to ensure the same star pattern every time.
        random.seed(gS.randomSeed)
        for i in range(gS.numberOfStars):
            x = random.randint(340, gS.screenWidth-355)
            y = random.randint(0, gS.screenHeight)
            self.randStarPose.append((x, y))

    def draw(self, displaySurface):
        # Draws all the stars on the screen.s
        # It generates star positions only on the first call.
        if not self.randStarPose:
            self.starPose()
        else:
            for pos in self.randStarPose:
                displaySurface.blit(self.image, pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        # Initializes the Player sprite.
        super().__init__()
        self.image = image
        # Creates a float-based rectangle for the player, centered on the screen.
        self.rect = self.image.get_frect(center=(gS.screenWidth/2, gS.screenHeight-200))
        self.speed = gS.playerSpeed  # Sets the player's movement speed.
        self.health = 100  # Add a health attribute

        # Create a pixel mask for accurate collisions
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, keyPressed, dt):
        # Moves the player based on the key pressed and delta time (dt).
        if keyPressed == 'w':
            self.rect.top -= self.speed * dt
        elif keyPressed == 'a':
            self.rect.left -= self.speed * dt
        elif keyPressed == 's':
            self.rect.bottom += self.speed * dt
        elif keyPressed == 'd':
            self.rect.right += self.speed * dt

    def draw(self, displaySurface):
        # Draws the player sprite onto the display surface.
        displaySurface.blit(self.image, self.rect)
        # Draw the health bar.
        # Health bar dimensions and position
        healthBarHeight = 5
        healthBarY = self.rect.bottom + 5  # Place the bar 5 pixels below the bottom of the player's sprite

        # This is the background of the health bar (e.g., black or red).
        pygame.draw.rect(displaySurface, (255, 0, 0), [self.rect.x, healthBarY, self.rect.width, healthBarHeight])

        # This is the current health portion of the bar (e.g., green).
        healthWidth = int(self.rect.width * (self.health / 100))
        pygame.draw.rect(displaySurface, (0, 255, 0), [self.rect.x, healthBarY, healthWidth, healthBarHeight])


class Laser(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        # Initializes the Laser sprite.
        super().__init__()
        self.image = image
        # Creates a float-based rectangle for the laser.
        self.rect = self.image.get_frect()
        # Sets the initial position of the laser.
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self, dt):
        # Moves the laser up the screen.
        self.rect.bottom -= gS.laserSpeed * dt
        # Removes the laser from all groups once it goes off-screen.
        if self.rect.bottom < 0:
            self.kill()


class Droppings(pygame.sprite.Sprite):
    def __init__(self, itemType, image, x, y, speed):
        super().__init__()
        self.itemType = itemType
        self.image = image
        self.rect = self.image.get_frect(center=(x, y))
        self.speed = speed

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.bottom += self.speed * dt

        if self.rect.top > gS.screenHeight:
            self.kill()


class Meteor(Droppings):
    def __init__(self, image, x, y):
        super().__init__('meteor', image, x, y, gS.meteorSpeed)



class Ammo(Droppings):
    def __init__(self, image, x, y):
        super().__init__('ammo',image,x,y,gS.ammoSpeed)



class Health(Droppings):
    def __init__(self, image, x, y):
        super().__init__('health',image,x,y,gS.healthSpeed)

class Life(Droppings):
    def __init__(self, image, x, y):
        super().__init__('life',image,x,y,gS.healthSpeed)



class Sound:
    def __init__(self):
        pygame.mixer.init()
        projectRoot = path.dirname(path.dirname(path.abspath(__file__)))
        self.sounds = {
            'ammo': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'ammo.wav')),
            'damage': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'damage.wav')),
            'explosion': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'explosion.wav')),
            'life': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'fullHealth.wav')),
            'bgm': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'gameMusic.wav')),
            'health': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'healthPack.wav')),
            'laser': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'laser.wav')),
        }
        self.sounds['bgm'].set_volume(0.1)
        self.sounds['explosion'].set_volume(0.35)

    def play(self, soundName):
        if soundName in self.sounds:
            self.sounds[soundName].play()
        else:
            print(f"{soundName} not found.")



class UI(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont(path.join(path.dirname(__file__), '..', 'fonts', 'Arbedo-E4g3z.ttf'), 30)

    def drawText(self, surface, text, pos, color=(255, 255, 255)):
        """A helper method to draw text on the screen."""
        # Render the text into a new surface
        text_surface = self.font.render(text, True, color)

        # Get the rectangle of the text surface to position it
        text_rect = text_surface.get_rect(center=pos)

        # Blit the text surface onto the main surface
        surface.blit(text_surface, text_rect)

    def draw(self, surface, score, health, ammo):
        """Draws all UI elements, including text."""
        # First, draw the static sidebar background image
        surface.blit(self.image, (0, 0))

        # --- Display Text on Sidebars ---
        # Note: The (x, y) coordinates are examples. Adjust them to fit your sidebars.

        # Display Score (e.g., centered in the left sidebar)
        score_text = f"Score: {int(score)}"
        self.drawText(surface, score_text, (150, 100))  # (x=150 is center of a 300px sidebar)

        # Display Health (e.g., in the left sidebar)
        health_text = f"Health: {int(health)}"
        self.drawText(surface, health_text, (150, 150), color=(0, 255, 0))  # Green color

        # Display Ammo (e.g., in the left sidebar)
        ammo_text = f"Ammo: {ammo}"
        self.drawText(surface, ammo_text, (150, 200), color=(255, 200, 0))  # Yellow/Orange color

if __name__ == "__main__":
    # This block of code only runs when the script is executed directly.
    # It sets up the main game loop and starts the game.

    # Initialize the Pygame display window.
    screen = pygame.display.set_mode(gS.screenSize)

    # Create an instance of the main game class.
    game = Shooter()

    # Start the game loop.
    game.run()







