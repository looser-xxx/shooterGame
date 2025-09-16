# --- Standard Library Imports ---
import random  # Used for generating random numbers for things like spawn positions.
from os import path  # Used for creating operating-system-independent file paths to load assets.

# --- Third-Party Imports ---
import pygame  # The core library used to create the game window, handle graphics, and manage events.

# --- Local Application Imports ---
# Imports all game-wide constants and settings from the local gameSettings.py file.
import gameSettings as gS

def loadingAssets(fileName):
    """
    A helper function to load an image from the 'images' directory.

    This centralizes the asset loading process and ensures file paths
    are constructed in an operating-system-independent way.

    Args:
        fileName (str): The name of the image file to load (e.g., 'player.png').

    Returns:
        pygame.Surface: The loaded and optimized image surface.
    """
    # 1. Construct the full file path to the image.
    # This creates a path like '../images/your_image.png' relative to 'main.py'.
    imagePath = path.join(path.dirname('main.py'), '..', 'images', fileName)

    # 2. Load the image and optimize it for the game.
    # .convert_alpha() creates a copy of the Surface with a pixel format
    # that's optimized for fast drawing (biting) and preserves transparency.
    return pygame.image.load(imagePath).convert_alpha()


def randGenForProb(n):
    """
    Takes a number 'n' and returns a new, slightly randomized version of it.

    This function applies a random variance to the input number based on
    the 'randomProbability' value from the game settings. For example, it
    can turn a fixed spawn time into a slightly unpredictable one.

    Args:
        n (float): The base number to randomize (e.g., a spawn rate).

    Returns:
        float: The new, randomized number.
    """
    # 1. Scale the number up to work with integers for more precise calculations.
    n *= 1000

    # 2. Calculate the lower and upper bounds for the random range.
    # This creates a range around 'n' based on the percentage from game settings.
    randSmall = n - gS.randomProbability / 100 * n
    randLarge = n + gS.randomProbability / 100 * n

    # 3. Pick a random integer within the calculated bounds.
    randomValue = random.randint(int(randSmall), int(randLarge))

    # 4. Scale the result back down to its original magnitude and return it.
    return randomValue / 1000

class Shooter:
    def __init__(self):
        # 1. Core Engine Setup
        # Initializes Pygame's modules and sets up the main game clock and loop control.
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()

        # 2. Display Setup
        # Creates the main game window where everything will be drawn.
        self.screenColor = gS.screenColor
        self.displaySurface = pygame.display.set_mode(gS.screenSize)

        # 3. Game Object Instantiation
        # Loads assets and creates instances of the main game objects.
        self.stars = Stars(loadingAssets('star.png'))
        self.player = Player(loadingAssets('player.png'))
        self.ui = UI(loadingAssets('sideBars.png'))
        self.sfx = Sound()

        # 4. Sprite Group Setup
        # Creates containers to hold and manage different types of game objects (sprites).
        self.allSprites = pygame.sprite.Group()  # Master group for drawing and updating all sprites.
        self.lasers = pygame.sprite.Group()      # For the player's lasers.
        self.meteors = pygame.sprite.Group()     # For meteor objects.
        self.ammoG = pygame.sprite.Group()       # For ammo power-ups.
        self.healthG = pygame.sprite.Group()     # For health power-ups.
        self.lifeG = pygame.sprite.Group()       # For life power-ups.

        # Add initial, non-moving objects to the master sprite group
        self.allSprites.add(self.stars)
        self.allSprites.add(self.player)

        # 5. Game State & Timers
        # Variables that track the player's status and control game events over time.
        self.gameTime = 0
        self.ammo = gS.ammo
        self.meteorTimer = 0
        self.ammoTimer = 0
        self.healthTimer = 0
        self.lifeTimer = 0
        self.difficultyTime = gS.difficultyTime

        # 6. Gameplay & Difficulty Parameters
        #  Configure the spawn rates of various objects, which can be modified during play.
        self.meteorSpawnRate = gS.meteorSpawnRate
        self.ammoSpawnRate = gS.ammoSpawnRate
        self.ammoIncrement = gS.ammoIncrement
        self.healthSpawnRate = gS.healthSpawnRate
        self.lifeSpawnRate = gS.lifeSpawnRate

    # Add these two methods inside your Shooter class

    def reset(self):
        """
        Resets the entire game state to its initial values for a new session.
        This includes player stats, score, difficulty, and all on-screen objects.
        """
        # 1. Reset Game State & Timers
        self.gameTime = 0
        self.meteorTimer = 0
        self.ammoTimer = 0
        self.healthTimer = 0
        self.lifeTimer = 0

        # 2. Reset Player Attributes
        self.player.health = 100
        self.player.rect.center = (gS.screenWidth / 2, gS.screenHeight - 200)
        self.ammo = gS.ammo

        # 3. Reset Gameplay & Difficulty Parameters to their defaults
        self.difficultyTime = gS.difficultyTime
        self.meteorSpawnRate = gS.meteorSpawnRate
        self.ammoSpawnRate = gS.ammoSpawnRate
        self.healthSpawnRate = gS.healthSpawnRate
        self.lifeSpawnRate = gS.lifeSpawnRate
        self.ammoIncrement = gS.ammoIncrement

        # 4. Clear all dynamic sprites from the previous game session
        self.meteors.empty()
        self.lasers.empty()
        self.ammoG.empty()
        self.healthG.empty()
        self.lifeG.empty()

        # Reset the main sprite group to only contain the essential sprites
        self.allSprites.empty()
        self.allSprites.add(self.player, self.stars)

    def _load_highscore(self):
        """
        Loads the high score from 'highscore.txt'.
        If the file doesn't exist or is invalid, it returns 0.
        """
        try:
            with open("highscore.txt", "r") as f:
                score = int(f.read())
                return score
        except (FileNotFoundError, ValueError):
            # File doesn't exist or is empty/corrupt
            return 0

    def _save_highscore(self, score):
        """
        Saves a new high score to 'highscore.txt'.
        """
        with open("highscore.txt", "w") as f:
            f.write(str(int(score)))

    # Add this method inside your Shooter class
    def gameOverScreen(self):
        """
        Displays the game over screen with scores and a retry button.
        This function runs a separate loop to wait for player input.
        """
        # --- High Score Logic ---
        # 1. Capture the final score before it gets reset.
        finalScore = int(self.gameTime)

        # 2. Load the existing high score from the file.
        highScore = self._load_highscore()

        # 3. Check if the current score is a new high score.
        newHighscore = finalScore > highScore
        if newHighscore:
            # If it is, save the new high score and update the display variable.
            self._save_highscore(finalScore)
            highScore = finalScore

        # --- Screen & Button Setup ---
        textColor = (255, 255, 255)
        buttonColor = (0, 100, 0)
        buttonHoverColor = (0, 150, 0)
        newHighscoreColor = (255, 215, 0)  # Gold color

        buttonWidth = 200
        buttonHeight = 50
        buttonX = (gS.screenWidth / 2) - (buttonWidth / 2)
        buttonY = gS.screenHeight / 2 + 100
        retryButton = pygame.Rect(buttonX, buttonY, buttonWidth, buttonHeight)

        # --- Main Loop for this Screen ---
        waiting = True
        while waiting:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'QUIT'  # Signal to quit the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and retryButton.collidepoint(event.pos):
                        self.reset()
                        return 'RETRY'  # Signal to retry

            # Drawing
            self.displaySurface.fill(self.screenColor)

            # Display "Game Over" text
            self.ui.drawText(self.displaySurface, "Game Over", (gS.screenWidth / 2, gS.screenHeight / 4),
                             color=textColor)

            # Display the player's final score
            finalScoreText = f"Your Score: {finalScore}"
            self.ui.drawText(self.displaySurface, finalScoreText, (gS.screenWidth / 2, gS.screenHeight / 3),
                             color=textColor)

            # Display the High Score
            highScoreText = f"High Score: {highScore}"
            self.ui.drawText(self.displaySurface, highScoreText, (gS.screenWidth / 2, gS.screenHeight / 3 + 50),
                             color=textColor)

            # If a new high score was achieved, display a special message.
            if newHighscore:
                self.ui.drawText(self.displaySurface, "New High Score!",
                                 (gS.screenWidth / 2, gS.screenHeight / 3 + 100), color=newHighscoreColor)

            # Draw Retry Button with hover effect
            mousePos = pygame.mouse.get_pos()
            if retryButton.collidepoint(mousePos):
                pygame.draw.rect(self.displaySurface, buttonHoverColor, retryButton)
            else:
                pygame.draw.rect(self.displaySurface, buttonColor, retryButton)

            self.ui.drawText(self.displaySurface, "Retry", retryButton.center, color=textColor)

            # Update the display
            pygame.display.flip()
            self.clock.tick(gS.fps)



    def difficulty(self):
        """
        Increases the game's difficulty by uniformly scaling all spawn rates.
        This makes the overall pace of the game faster.
        """
        # 1. Update the timer for the next difficulty increase
        self.difficultyTime += gS.difficultyTime

        # 2. Calculate the difficulty multiplier (e.g., 0.9)
        difficulty = (100 - gS.difficultyIncrement) / 100

        # 3. Apply the multiplier to all spawn rates
        # This shortens the time interval for everything equally.
        self.meteorSpawnRate *= difficulty
        self.ammoSpawnRate *= difficulty
        self.healthSpawnRate *= difficulty
        self.lifeSpawnRate *= difficulty

        # 4. Slightly increase the amount of ammo received per pack
        self.ammoIncrement += self.ammoIncrement * gS.difficultyIncrement / 100

    def run(self):
        # This is the main game loop that keeps the game running.
        self.sfx.play('bgm')

        while self.running:
            # 1. Timing and Difficulty
            # Calculate delta time for frame-rate independent physics.
            dt = self.clock.tick(gS.fps) / 1000
            self.gameTime += dt

            # Check if it's time to increase the game difficulty.
            if self.gameTime >= self.difficultyTime:
                self.difficulty()

            # 2. Object Spawning
            # Use timers to control when new objects are created.

            # Meteor spawning
            self.meteorTimer += dt
            if self.meteorTimer >= randGenForProb(self.meteorSpawnRate):
                self.spawnObjects('meteor')
                self.meteorTimer = 0

            # Ammo spawning
            self.ammoTimer += dt
            if self.ammoTimer >= randGenForProb(self.ammoSpawnRate):
                self.spawnObjects('ammo')
                self.ammoTimer = 0

            # Health spawning
            self.healthTimer += dt
            if self.healthTimer >= randGenForProb(self.healthSpawnRate):
                self.spawnObjects('health')
                self.healthTimer = 0

            # Life spawning
            self.lifeTimer += dt
            if self.lifeTimer >= randGenForProb(self.lifeSpawnRate):
                self.spawnObjects('life')
                self.lifeTimer = 0

            # 3. Event Handling and Updates
            # Process user input and update the state of all game objects.
            self.handleEvents(dt)
            self.allSprites.update(dt)

            # 4. Collision Detection
            # Check for collisions between different groups of sprites.
            playerCollision = pygame.sprite.spritecollide(self.player, self.meteors, True, pygame.sprite.collide_mask)
            laserCollision = pygame.sprite.groupcollide(self.lasers, self.meteors, True, True,
                                                        pygame.sprite.collide_mask)
            ammoCollision = pygame.sprite.spritecollide(self.player, self.ammoG, True, pygame.sprite.collide_mask)
            healthCollision = pygame.sprite.spritecollide(self.player, self.healthG, True, pygame.sprite.collide_mask)
            lifeCollision = pygame.sprite.spritecollide(self.player, self.lifeG, True, pygame.sprite.collide_mask)

            # 5. Collision Handling
            #  Responds to any collisions that were detected.
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

            # 6. Rendering
            #  Draws all game elements to the screen and updates the display.
            self.draw()
            self.boundary()
            pygame.display.flip()

    def spawnObjects(self, spawn):
        # 1. Determine the spawn position
        # Generate a random horizontal position within the playable area.
        x = random.randint(gS.playSpace[0], gS.playSpace[1])
        # Use a fixed vertical position just above the screen.
        y = gS.droppingSpawnPosition

        # 2. Call the appropriate spawn method based on the 'spawn' type
        # This block checks the 'spawn' string and calls the specific
        # function responsible for creating that object.
        if spawn == 'ammo':
            self.spawnAmmo(x, y)

        if spawn == 'meteor':
            self.spawnMeteor(x, y)

        if spawn == 'health':
            self.spawnHealth(x, y)

        if spawn == 'life':
            self.spawnLife(x, y)

    def spawnMeteor(self, x, y):
        """Creates a new meteor and adds it to the game."""
        newMeteor = Meteor(loadingAssets('meteor.png'), x, y)
        self.meteors.add(newMeteor)
        self.allSprites.add(newMeteor)

    def spawnAmmo(self, x, y):
        """Creates a new ammo pack and adds it to the game."""
        newAmmo = Ammo(loadingAssets('ammo.png'), x, y)
        self.ammoG.add(newAmmo)
        self.allSprites.add(newAmmo)

    def spawnHealth(self, x, y):
        """Creates a new health pack and adds it to the game."""
        newHealth = Health(loadingAssets('health.png'), x, y)
        self.healthG.add(newHealth)
        self.allSprites.add(newHealth)

    def spawnLife(self, x, y):
        """Creates a new life pack and adds it to the game."""
        newLife = Health(loadingAssets('life.png'), x, y)
        self.lifeG.add(newLife)
        self.allSprites.add(newLife)

    def draw(self):
        """
        Handles all drawing operations for the game.
        This method is called once per frame to render the game state.
        The order of operations is important for correct visual layering.
        """
        # 1. Clear the Screen
        # Fill the display with a solid color to erase everything from the last frame.
        self.displaySurface.fill(self.screenColor)
        # self.displaySurface.blit(loadingAssets('background.png'), self.displaySurface.get_rect())

        # 2. Draw the Background Elements
        # The starfield is drawn first so all other objects appear on top of it.
        self.stars.draw(self.displaySurface)

        # 3. Draw All Game Sprites
        # Loop through the master sprite group to draw each object.
        for sprite in self.allSprites:
            # This checks if a sprite has a special drawing method (e.g., the player's health bar).
            if hasattr(sprite, 'draw'):
                # If it does, use its custom draw method.
                sprite.draw(self.displaySurface)
            else:
                # Otherwise, use the standard method to draw the sprite's image.
                self.displaySurface.blit(sprite.image, sprite.rect)

        # 4. Draw the User Interface (UI)
        # Draw the static sidebar background image.
        self.displaySurface.blit(self.ui.image, (0, 0))

        # Call the UI's own draw method to render dynamic text (score, health, etc.)
        # over the sidebars.
        self.ui.draw(
            self.displaySurface,
            self.gameTime,
            self.player.health,
            self.ammo
        )

    def handleEvents(self, dt):
        """
        Handles all user input, including window events, mouse clicks,
        and continuous keyboard or mouse movement.
        """
        # 1. Process Event Queue
        # This loop handles discrete, one-time events like clicks or quitting.
        for event in pygame.event.get():
            # Check if the user clicked the 'X' to close the window.
            if event.type == pygame.QUIT:
                self.running = False

            # Check for a mouse button press (for shooting).
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the left mouse button (button 1) is pressed and the player has ammo.
                if event.button == 1 and self.ammo > 0:
                    self.sfx.play('laser')
                    self.ammo -= 1

                    # Create a new laser instance at the player's position.
                    laser = Laser(
                        loadingAssets('laser.png'),
                        self.player.rect.centerx,
                        self.player.rect.top
                    )

                    # Add the new laser to its group and the main sprite group.
                    self.lasers.add(laser)
                    self.allSprites.add(laser)

        # 2. Process Continuous Input
        # This block handles actions that happen every frame a key is held
        # down or the mouse is moved.

        # Check which control scheme is active (mouse or keyboard).
        if gS.mouse:
            # Player's position is directly set to the mouse cursor's position.
            self.player.rect.center = pygame.mouse.get_pos()
        else:
            # Check for currently held-down keyboard keys for player movement.
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
        """
        Handles the game logic for different types of collision events.
        This method is called when a collision is detected in the main game loop.
        """
        match collisionType:
            # Case for when the player collects an ammo pack.
            case 'ammo':
                self.sfx.play('ammo')
                self.ammo += self.ammoIncrement

            # Case for when a laser hits a meteor.
            case 'laser':
                self.sfx.play('explosion')

            # Case for when the player collides with a meteor.
            case 'player':
                self.sfx.play('damage')
                self.player.health -= gS.healthLossByCollision
                # If the player's health drops to zero or below, end the game.
                if self.player.health <= 0:
                    self.gameOverScreen()

            # Case for when the player collects a health pack.
            case 'health':
                self.sfx.play('health')
                self.player.health += gS.healthIncrement
                # Cap the player's health at 100 to prevent it from going over the maximum.
                if self.player.health > 100:
                    self.player.health = 100

            # Case for when the player collects a life pack.
            case 'life':
                self.sfx.play('life')
                # Instantly restore the player to full health.
                self.player.health = 100

            # Default case to catch any unexpected collision types for debugging.
            case _:
                print(f"Warning: Unknown collision type '{collisionType}'")

    def boundary(self):
        """
        Ensures the player sprite stays within the designated screen and play space boundaries.
        This method is called every frame to clamp the player's position.
        """
        # --- Vertical Boundary Checks ---

        # Prevent the player from moving above the top edge of the screen.
        if self.player.rect.top < 0:
            self.player.rect.top = 0

        # Prevent the player from moving below the bottom edge of the screen.
        if self.player.rect.bottom > gS.screenHeight:
            self.player.rect.bottom = gS.screenHeight

        # --- Horizontal Boundary Checks ---

        # Prevent the player from moving past the left boundary of the play space.
        if self.player.rect.left < gS.playSpace[0]:
            self.player.rect.left = gS.playSpace[0]

        # Prevent the player from moving past the right boundary of the play space.
        if self.player.rect.right > gS.playSpace[1]:
            self.player.rect.right = gS.playSpace[1]


class Stars(pygame.sprite.Sprite):
    """
    Manages the static starfield background.

    This class creates a fixed set of stars that do not move,
    giving the illusion of a distant starfield. The positions are
    randomized but consistent between game sessions.
    """

    def __init__(self, image):
        """Initializes the Stars object."""
        super().__init__()
        # Store the image that will be used for each individual star.
        self.image = image
        # Get the rectangle of the image (though not used for positioning here).
        self.rect = self.image.get_rect()
        # A list to hold the randomly generated (x, y) coordinates for each star.
        self.randStarPose = []

    def starPose(self):
        """Generates and stores a list of random star positions."""
        # Use a fixed seed to ensure the star pattern is identical every time.
        random.seed(gS.randomSeed)

        # Loop to create the specified number of stars.
        for i in range(gS.numberOfStars):
            # Generate random coordinates within the playable game area.
            x = random.randint(340, gS.screenWidth - 355)
            y = random.randint(0, gS.screenHeight)
            # Add the new star's position tuple to the list.
            self.randStarPose.append((x, y))

    def draw(self, displaySurface):
        """Draws the entire starfield onto the provided surface."""
        # This check ensures that the star positions are generated only once,
        # the very first time this draw method is called.
        if not self.randStarPose:
            self.starPose()

        # Loop through the list of stored positions and draw a star at each one.
        for pos in self.randStarPose:
            displaySurface.blit(self.image, pos)


class Player(pygame.sprite.Sprite):
    """
    Represents the player-controlled spaceship.

    This class manages the player's position, movement, health,
    and custom drawing, which includes the ship and its health bar.
    """

    def __init__(self, image):
        """Initializes the Player object."""
        super().__init__()
        # The visual representation (image) of the player's ship.
        self.image = image
        # A float-based rectangle for precise positioning, starting near the bottom-center.
        self.rect = self.image.get_frect(center=(gS.screenWidth / 2, gS.screenHeight - 200))
        # The player's movement speed, loaded from game settings.
        self.speed = gS.playerSpeed
        # The player's health, starting at a default of 100.
        self.health = 100
        # A pixel-perfect mask generated from the image for accurate collision detection.
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, keyPressed, dt):
        """
        Updates the player's position based on keyboard input.
        Movement is multiplied by delta time (dt) to be frame-rate independent.
        """
        # Move the player based on which WASD key is pressed.
        if keyPressed == 'w':
            self.rect.top -= self.speed * dt
        elif keyPressed == 'a':
            self.rect.left -= self.speed * dt
        elif keyPressed == 's':
            self.rect.bottom += self.speed * dt
        elif keyPressed == 'd':
            self.rect.right += self.speed * dt

    def draw(self, displaySurface):
        """
        Draws the player's ship and a health bar directly below it.
        """
        # --- 1. Draw the Player Ship ---
        displaySurface.blit(self.image, self.rect)

        # --- 2. Draw the Health Bar ---
        # Define the health bar's height and position relative to the player.
        healthBarHeight = 5
        healthBarY = self.rect.bottom + 5

        # Draw the red background bar, representing the total possible health.
        pygame.draw.rect(displaySurface, (255, 0, 0), [self.rect.x, healthBarY, self.rect.width, healthBarHeight])

        # Calculate the width of the green bar based on the current health percentage.
        healthWidth = int(self.rect.width * (self.health / 100))

        # Draw the green foreground bar, representing the player's current health.
        pygame.draw.rect(displaySurface, (0, 255, 0), [self.rect.x, healthBarY, healthWidth, healthBarHeight])


class Laser(pygame.sprite.Sprite):
    """
    Represents a laser projectile fired by the player.

    This class manages the laser's initial position, its constant upward movement,
    and its automatic removal once it goes off-screen.
    """

    def __init__(self, image, x, y):
        """
        Initializes the Laser object at a specific starting position.

        Args:
            image: The pygame.Surface to use for the laser's image.
            x (int): The initial horizontal center for the laser.
            y (int): The initial vertical bottom for the laser.
        """
        super().__init__()
        # The visual representation of the laser bolt.
        self.image = image
        # A float-based rectangle for precise positioning.
        self.rect = self.image.get_frect()
        # Set the starting position to where the player fired it from.
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self, dt):
        """
        Moves the laser up the screen each frame and handles its lifecycle.

        Args:
            dt (float): Delta time, used for frame-rate independent movement.
        """
        # Move the laser vertically upwards at a constant speed.
        self.rect.bottom -= gS.laserSpeed * dt

        # Check if the laser has moved completely off the top of the screen.
        if self.rect.bottom < 0:
            # If so, remove the laser from all sprite groups to save memory and processing power.
            self.kill()


class Droppings(pygame.sprite.Sprite):
    """
    A base class for all objects that fall from the top of the screen.

    This class handles the shared logic for movement and screen boundary checks.
    It is intended to be inherited by other classes (like Meteor, Ammo, etc.)
    and not used directly.
    """

    def __init__(self, itemType, image, x, y, speed):
        """
        Initializes a dropping object.

        Args:
            itemType (str): A string identifier for the object (e.g., 'meteor').
            image (pygame.Surface): The image for the sprite.
            x (int): The initial horizontal center position.
            y (int): The initial vertical center position.
            speed (float): The downward movement speed.
        """
        super().__init__()
        # A string to identify the type of dropping (used for collision logic).
        self.itemType = itemType
        # The visual representation of the object.
        self.image = image
        # A float-based rectangle for precise positioning.
        self.rect = self.image.get_frect(center=(x, y))
        # The constant downward speed of the object.
        self.speed = speed
        # A pixel-perfect mask for accurate collision detection.
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        """
        Moves the object down the screen and removes it if it goes off-screen.

        Args:
            dt (float): Delta time, for frame-rate independent movement.
        """
        # Move the object vertically downwards.
        self.rect.bottom += self.speed * dt

        # If the object has moved completely past the bottom edge of the screen...
        if self.rect.top > gS.screenHeight:
            # ...remove it from all sprite groups to save memory.
            self.kill()


# --- Subclasses that inherit from Droppings ---

class Meteor(Droppings):
    """Represents a meteor enemy."""

    def __init__(self, image, x, y):
        # Sets the properties for a meteor, including its unique speed.
        super().__init__('meteor', image, x, y, gS.meteorSpeed)


class Ammo(Droppings):
    """Represents a collectible ammo pack."""

    def __init__(self, image, x, y):
        # Sets the properties for an ammo pack, including its unique speed.
        super().__init__('ammo', image, x, y, gS.ammoSpeed)


class Health(Droppings):
    """Represents a collectible health pack."""

    def __init__(self, image, x, y):
        # Sets the properties for a health pack, including its unique speed.
        super().__init__('health', image, x, y, gS.healthSpeed)


class Life(Droppings):
    """Represents a collectible life pack (full heal)."""

    def __init__(self, image, x, y):
        # Sets the properties for a life pack, including its unique speed.
        super().__init__('life', image, x, y, gS.healthSpeed)


class Sound:
    """
    A sound manager class for preloading and playing all game audio.

    This class handles initializing the sound system, loading all sound
    effects and music into memory, and providing a simple method to
    play them by name.
    """

    def __init__(self):
        """Initializes the sound system and loads all audio files."""
        # Initialize Pygame's mixer module.
        pygame.mixer.init()

        # Determine the project's root directory to build reliable file paths.
        projectRoot = path.dirname(path.dirname(path.abspath(__file__)))

        # Preload all sound files into a dictionary for quick and efficient access.
        # The key is a short name, and the value is the loaded Sound object.
        self.sounds = {
            'ammo': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'ammo.wav')),
            'damage': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'damage.wav')),
            'explosion': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'explosion.wav')),
            'life': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'fullHealth.wav')),
            'bgm': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'gameMusic.wav')),
            'health': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'healthPack.wav')),
            'laser': pygame.mixer.Sound(path.join(projectRoot, 'audio', 'laser.wav')),
        }

        # Adjust the volume for specific sounds to balance the overall audio mix.
        self.sounds['bgm'].set_volume(0.1)
        self.sounds['explosion'].set_volume(0.35)

    def play(self, soundName, loops=0):
        """
        Plays a preloaded sound by its name.

        Args:
            soundName (str): The key for the sound in the self.sounds dictionary.
            loops (int): The number of times to repeat the sound. -1 means loop forever.
        """
        # Check if the requested sound name exists in the dictionary to prevent errors.
        if soundName in self.sounds:
            # If it exists, play the sound with the specified number of loops.
            self.sounds[soundName].play(loops)
        else:
            # If not, print a warning to the console for debugging.
            print(f"Warning: Sound '{soundName}' not found.")


class UI(pygame.sprite.Sprite):
    """
    Manages the game's User Interface (UI).

    This includes drawing the static sidebar background and rendering
    dynamic text elements like score, health, and ammo count.
    """

    def __init__(self, image):
        """Initializes the UI object."""
        super().__init__()
        # The background image for the UI, likely containing the sidebars.
        self.image = image
        # The rectangle for the UI background image.
        self.rect = self.image.get_rect()
        # Load the custom font that will be used for displaying all text.
        self.font = pygame.font.SysFont(path.join(path.dirname(__file__), '..', 'fonts', 'Arbedo-E4g3z.ttf'), 30)

    def drawText(self, surface, text, pos, color=(255, 255, 255)):
        """A reusable helper method to draw a single line of centered text."""
        # Step 1: Render the font into a new Surface with anti-aliasing.
        text_surface = self.font.render(text, True, color)
        # Step 2: Get the rectangle of the new text Surface and set its center position.
        text_rect = text_surface.get_rect(center=pos)
        # Step 3: Draw the text Surface onto the main display surface.
        surface.blit(text_surface, text_rect)

    def draw(self, surface, score, health, ammo):
        """Draws all UI elements, including the background and all text stats."""
        # 1. Draw the static UI background first to ensure it's behind the text.
        surface.blit(self.image, (0, 0))

        # 2. Draw all dynamic text elements using the helper method.

        # Display the current score, formatted as an integer.
        score_text = f"Score: {int(score)}"
        self.drawText(surface, score_text, (150, 100))

        # Display the player's current health with a green color.
        health_text = f"Health: {int(health)}"
        self.drawText(surface, health_text, (150, 150), color=(0, 255, 0))

        # Display the player's current ammo count with a yellow/orange color.
        ammo_text = f"Ammo: {ammo}"
        self.drawText(surface, ammo_text, (150, 200), color=(255, 200, 0))


if __name__ == "__main__":
    # This block of code only runs when the script is executed directly.
    # It sets up the main game loop and starts the game.

    # Initialize the Pygame display window.
    screen = pygame.display.set_mode(gS.screenSize)

    # Create an instance of the main game class.
    game = Shooter()

    # Start the game loop.
    game.run()







