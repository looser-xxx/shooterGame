# =====================================================================
# METEOR DODGER - GAME SETTINGS
# =====================================================================
# This file contains all the core constants and configuration
# variables for the game. Tweak these values to balance the gameplay.

# --- Environment & Display Settings ---
screenWidth = 1920
screenHeight = 1080
screenSize = (screenWidth, screenHeight)
screenCenter = (screenWidth / 2, screenHeight / 2)
fps = 120  # Target frames per second for the game loop.
screenColor = 'darkslategray'  # Background color of the game window.

# --- Gameplay Area Settings ---
# Defines the horizontal area where gameplay occurs, accounting for sidebars.
playSpace = (350, screenWidth - 350)
# The vertical position where meteors and power-ups start spawning (just off-screen).
droppingSpawnPosition = -50

# --- Background Starfield Settings ---
numberOfStars = 50  # The total number of stars to draw in the background.
randomSeed = 654523  # A fixed seed to make the star pattern consistent every game.

# --- Player Settings ---
playerSpeed = 600  # The movement speed of the player's ship in pixels per second.
healthLossByCollision = 15  # The amount of health lost when the player hits a meteor.
ammo = 10  # The player's starting ammo count.

# --- Laser Settings ---
laserSpeed = 1000  # The speed of the player's laser projectiles.

# --- Meteor (Enemy) Settings ---
meteorSpeed = 500  # The downward speed of meteors.
meteorSpawnRate = 0.5  # The base time in seconds between meteor spawns.

# --- Ammo Power-up Settings ---
ammoSpeed = 300  # The downward speed of ammo packs.
ammoSpawnRate = 10  # The base time in seconds between ammo pack spawns.
ammoIncrement = 2  # The amount of ammo gained from one pack.

# --- Health Power-up Settings ---
healthSpeed = 300  # The downward speed of health packs.
healthSpawnRate = 7.5  # The base time in seconds between health pack spawns.
healthIncrement = 10  # The amount of health restored by one pack.

# --- Life Power-up Settings ---
lifeSpeed = 300  # The downward speed of life packs.
lifeSpawnRate = 20  # The base time in seconds between life pack spawns.

# --- Gameplay Mechanic Settings ---
# The percentage of random variance to apply to spawn rates (e.g., 20 means +/- 20%).
randomProbability = 20
# The percentage by which to increase difficulty each time the threshold is met.
difficultyIncrement = 10
# The initial time in seconds before the first difficulty increase.
difficultyTime = 10

# --- Controls ---
# Determines the player's control scheme. False = Keyboard (WASD), True = Mouse.
mouse = False