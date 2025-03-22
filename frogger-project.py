from pygame import *
from random import *

init()

# Grid setup
TILE_SIZE = 30
GRID_WIDTH = 13
GRID_HEIGHT = 18

# Screen setup
width = GRID_WIDTH * TILE_SIZE
height = GRID_HEIGHT * TILE_SIZE
screen = display.set_mode((width, height))
display.set_caption('Frogger')

# Game variables
endGame = False

# Load images and scale
frogPic = image.load("frog.JPG")
frogPic = transform.scale(frogPic, (TILE_SIZE, TILE_SIZE))

carPic = image.load("car.JPG")
carPic = transform.scale(carPic, (TILE_SIZE * 2, TILE_SIZE))

logPic = image.load("log.JPG")
logPic = transform.scale(logPic, (TILE_SIZE * 3, TILE_SIZE))

# Define grid sections
end_zone = Rect(0, TILE_SIZE, width, TILE_SIZE * 2)  # Made two rows tall
water = Rect(0, TILE_SIZE * 3, width, TILE_SIZE * 6)  # Water shifted down
safe_zone = Rect(0, TILE_SIZE * 9, width, TILE_SIZE)
road = Rect(0, TILE_SIZE * 10, width, TILE_SIZE * 5)
curb1 = Rect(0, road.top - TILE_SIZE, width, TILE_SIZE)
curb2 = Rect(0, road.bottom, width, TILE_SIZE)

# Starting frog position
frogRect = Rect(width // 2 - TILE_SIZE // 2, height - TILE_SIZE * 2, TILE_SIZE, TILE_SIZE)

# Define lanes
CAR_LANES = [road.top + TILE_SIZE, road.top + TILE_SIZE * 3, road.top + TILE_SIZE * 5]
LOG_LANES = [water.top + TILE_SIZE * i for i in range(1, 7)]  # Original log lanes

# Add extra log row above
LOG_LANES.insert(0, water.top + TILE_SIZE)  # Insert a new row at the top

# Add final log row that connects to the end zone
LOG_LANES.append(end_zone.bottom)  # Ensure the last row connects directly to the end zone

SPEED = 2

cars = []
logs = []

# Generate cars with random speed
def generate_cars():
    for lane in CAR_LANES:
        x = width + 100
        while x > 0:
            speed = randint(1, 4)  # Random speed between 1 and 4
            cars.append({"rect": Rect(x, lane, TILE_SIZE * 2, TILE_SIZE), "speed": -speed})
            x -= TILE_SIZE * 5

# Generate logs with random speed
def generate_logs():
    for lane in LOG_LANES:
        x = -200
        while x < width:
            speed = randint(1, 3)  # Random speed between 1 and 3
            logs.append({"rect": Rect(x, lane, TILE_SIZE * 3, TILE_SIZE), "speed": speed})
            x += TILE_SIZE * 5

generate_cars()
generate_logs()

# Background music
mixer.music.load("coolsong.mp3")
mixer.music.play(-1)

# Main game loop
while not endGame:
    for e in event.get():
        if e.type == QUIT:
            endGame = True

        if e.type == KEYDOWN:
            if e.key == K_DOWN:
                frogRect.move_ip(0, TILE_SIZE)
            if e.key == K_UP:
                frogRect.move_ip(0, -TILE_SIZE)
            if e.key == K_LEFT:
                frogRect.move_ip(-TILE_SIZE, 0)
            if e.key == K_RIGHT:
                frogRect.move_ip(TILE_SIZE, 0)

    # Move cars
    for car in cars:
        car["rect"].x += car["speed"]
        if car["rect"].x < -TILE_SIZE * 2:
            car["rect"].x = width + TILE_SIZE * 2
        if car["rect"].colliderect(frogRect):
            print("Game Over! You got hit by a car.")
            endGame = True

    # Move logs and check frog collision
    on_log = False
    for log in logs:
        log["rect"].x += log["speed"]
        if log["rect"].x > width:
            log["rect"].x = -TILE_SIZE * 3
        if log["rect"].colliderect(frogRect):
            on_log = True
            frogRect.x += log["speed"]

    # Check if frog is in water without a log
    if water.colliderect(frogRect) and not on_log:
        print("Game Over! You fell in the water.")
        endGame = True

    # Check if frog wins
    if end_zone.colliderect(frogRect):
        print("Congratulations! You won!")
        endGame = True

    # Draw everything
    screen.fill((0, 0, 0))
    draw.rect(screen, (0, 255, 0), end_zone)  # Two rows now!
    draw.rect(screen, (0, 0, 255), water)
    draw.rect(screen, (128, 128, 128), safe_zone)
    for log in logs:
        screen.blit(logPic, log["rect"])
    draw.rect(screen, (128, 128, 128), curb1)
    draw.rect(screen, (128, 128, 128), curb2)
    draw.rect(screen, (128, 128, 128), road)
    for car in cars:
        screen.blit(carPic, car["rect"])
    screen.blit(frogPic, frogRect)

    display.update()
    time.delay(30)
