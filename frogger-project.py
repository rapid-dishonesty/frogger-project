from pygame import *
from random import *

init()

width = 600
height = 400
screen = display.set_mode((width, height))
display.set_caption('Frogger')
endGame = False

frogPic = image.load("frog.JPG")
frogPic = transform.scale(frogPic, (40,40))

carPic = image.load("car.JPG")
carPic = transform.scale(carPic, (70,35))

curb1 = Rect(0, height - 50, width, 10)
curb2 = Rect(0, height - 170, width, 10)
frogRect = Rect (width // 2 - 20,height - 40,40,40)

road_top = curb2.bottom
road_bottom = curb1.top - 40

cars = [Rect(randint(600, 800), road_top + 10,70,35), Rect(randint(600, 800),road_top + 60, 70, 35), Rect(randint(600, 800),road_bottom - 60, 70, 35)]
cars.append(Rect(350,275,70,35))

mixer.music.load("coolsong.mp3")
mixer.music.play(-1)

while endGame == False:
    for e in event.get():
        if e.type == QUIT:
            endGame = True

        if e.type == KEYDOWN:
            if e.key == K_DOWN:
                frogRect.move_ip(0,40)
            if e.key == K_UP:
                frogRect.move_ip(0,-40)
            if e.key == K_LEFT:
                frogRect.move_ip(-40,0)
            if e.key == K_RIGHT:
                frogRect.move_ip(40,0)

    for car in cars:
        car.x -= randint(3, 6)  # Cars move at slightly different speeds
        if car.x < -75:  # If car leaves screen, reset to right side
            car.x = randint(600, 800)

    for c in cars:
        if c.colliderect(frogRect):
            print("you're dead, oopsie")
            endGame = True

    screen.fill((0,0,0))
    for c in cars:
      draw.rect(screen, (255,255,255),c)
    draw.rect(screen, (255,255,255), (0,0,width,20))

    for car in cars:
        screen.blit(carPic, car)

    screen.blit(frogPic, frogRect)
    #screen.blit(carPic, (350,275))
    draw.rect(screen, (128, 128, 128), curb1)
    draw.rect(screen, (128, 128, 128), curb2)
    display.update()
    time.delay(30)
