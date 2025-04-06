from pygame import *
from random import *

# Initialize the game
init()

# Set up constants for the grid and tile size
TILE_SIZE = 30
GRID_WIDTH = 13
GRID_HEIGHT = 18

# Set up the display window
width = GRID_WIDTH * TILE_SIZE
height = GRID_HEIGHT * TILE_SIZE
screen = display.set_mode((width, height))
display.set_caption('Frogger')  # Giving the window a title

# Flag to track the game over state
endGame = False

# Load and scale images for the frog, cars, and logs
frogPic = image.load("frog.JPG")
frogPic = transform.scale(frogPic, (TILE_SIZE, TILE_SIZE))

carPic = image.load("car.JPG")
carPic = transform.scale(carPic, (TILE_SIZE * 2, TILE_SIZE))

logPic = image.load("log.JPG")
logPic = transform.scale(logPic, (TILE_SIZE * 3, TILE_SIZE))

# Define various grid areas (like the road, water, and safe zones)
end_zone = Rect(0, TILE_SIZE, width, TILE_SIZE * 2)  # Two rows high now for a bigger goal area
water = Rect(0, TILE_SIZE * 3, width, TILE_SIZE * 6)  # Water starts lower now
safe_zone = Rect(0, TILE_SIZE * 9, width, TILE_SIZE)  # Safe zone at the bottom
road = Rect(0, TILE_SIZE * 10, width, TILE_SIZE * 5)  # The road where the cars will move
curb1 = Rect(0, road.top - TILE_SIZE, width, TILE_SIZE)  # The top curb
curb2 = Rect(0, road.bottom, width, TILE_SIZE)  # The bottom curb

# Set the initial position of the frog (centered at the bottom of the screen)
frogRect = Rect(width // 2 - TILE_SIZE // 2, height - TILE_SIZE * 2, TILE_SIZE, TILE_SIZE)

# Define where the cars and logs will be placed (each lane)
CAR_LANES = [road.top + TILE_SIZE, road.top + TILE_SIZE * 3, road.top + TILE_SIZE * 5]
LOG_LANES = [water.top + TILE_SIZE * i for i in range(1, 7)]  # Logs originally float in the water here

# Add extra log row at the top and final log row that connects to the goal
LOG_LANES.insert(0, water.top + TILE_SIZE)
LOG_LANES.append(end_zone.bottom)

# Speed of the moving objects (cars and logs)
SPEED = 2

# Lists to store all cars and logs
cars = []
logs = []

# Function to generate cars with random speeds
def generate_cars():
    for lane in CAR_LANES:
        x = width + 100  # Place cars starting off the screen to the right
        while x > 0:
            speed = randint(1, 4)  # Random speed for each car
            cars.append({"rect": Rect(x, lane, TILE_SIZE * 2, TILE_SIZE), "speed": -speed})
            x -= TILE_SIZE * 5  # Place cars at intervals

# Function to generate logs with random speeds
def generate_logs():
    for lane in LOG_LANES:
        x = -200  # Place logs starting off the screen to the left
        while x < width:
            speed = randint(1, 3)  # Random speed for each log
            logs.append({"rect": Rect(x, lane, TILE_SIZE * 3, TILE_SIZE), "speed": speed})
            x += TILE_SIZE * 5  # Place logs at intervals

# Call the functions to generate the cars and logs
generate_cars()
generate_logs()

# Play background music
mixer.music.load("coolsong.mp3")
mixer.music.play(-1)  # Loop the song indefinitely

# Main game loop
while not endGame:
    for e in event.get():
        if e.type == QUIT:
            endGame = True  # End the game if the player closes the window

        if e.type == KEYDOWN:
            # Control frog's movement with arrow keys
            if e.key == K_DOWN:
                frogRect.move_ip(0, TILE_SIZE)
            if e.key == K_UP:
                frogRect.move_ip(0, -TILE_SIZE)
            if e.key == K_LEFT:
                frogRect.move_ip(-TILE_SIZE, 0)
            if e.key == K_RIGHT:
                frogRect.move_ip(TILE_SIZE, 0)

    # Keep the frog within the screen boundaries
    if frogRect.left < 0:
        frogRect.left = 0
    if frogRect.right > width:
        frogRect.right = width
    if frogRect.top < 0:
        frogRect.top = 0
    if frogRect.bottom > height:
        frogRect.bottom = height

    # Move cars and check for collisions with the frog
    for i, car in enumerate(cars):
        car["rect"].x += car["speed"]
        if car["rect"].x < -TILE_SIZE * 2:  # Reset car when it moves off-screen
            car["rect"].x = width + TILE_SIZE * 2
        if car["rect"].colliderect(frogRect):  # Frog hits a car, game over
            print("Game Over! You got hit by a car.")
            endGame = True

        # Handle car collisions and set speeds equal if cars overlap
        for j, other_car in enumerate(cars):
            if i != j and car["rect"].colliderect(other_car["rect"]):
                car["speed"] = other_car["speed"] = car["speed"]

    # Move logs and check if the frog is on a log or not
    on_log = False
    log_speed = 0
    for i, log in enumerate(logs):
        log["rect"].x += log["speed"]
        if log["rect"].x > width:  # Reset log when it moves off-screen
            log["rect"].x = -TILE_SIZE * 3
        if log["rect"].colliderect(frogRect):  # Frog jumps on a log, moves with it
            on_log = True
            log_speed = log["speed"]
            frogRect.x += log_speed

        # Handle log collisions and set speeds equal if logs overlap
        for j, other_log in enumerate(logs):
            if i != j and log["rect"].colliderect(other_log["rect"]):
                log["speed"] = other_log["speed"] = log["speed"]

    # If the frog is in the water without a log, it's game over
    if water.colliderect(frogRect) and not on_log:
        print("Game Over! You fell in the water.")
        endGame = True

    # If the frog reaches the goal area, the player wins
    if end_zone.colliderect(frogRect):
        print("Congratulations! You won!")
        endGame = True

    # Draw everything on the screen
    screen.fill((0, 0, 0))  # Clear the screen with black
    draw.rect(screen, (0, 255, 0), end_zone)  # Draw the end zone (goal area)
    draw.rect(screen, (0, 0, 255), water)  # Draw the water area
    draw.rect(screen, (128, 128, 128), safe_zone)  # Draw the safe zone
    for log in logs:
        screen.blit(logPic, log["rect"])  # Draw the logs
    draw.rect(screen, (128, 128, 128), curb1)  # Draw the top curb
    draw.rect(screen, (128, 128, 128), curb2)  # Draw the bottom curb
    draw.rect(screen, (128, 128, 128), road)  # Draw the road
    for car in cars:
        screen.blit(carPic, car["rect"])  # Draw the cars
    screen.blit(frogPic, frogRect)  # Draw the frog

    display.update()  # Update the screen with all the drawings
    time.delay(30)  # Add a small delay to make the game run at a reasonable speed
