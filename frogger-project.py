from pygame import *

init()
width = 600
height = 400
screen = display.set_mode((width, height))
display.set_caption('Frogger')
endGame = False

frogPic = image.load("frog.JPG")
frogPic = transform.scale(frogPic, (40,40))
carPic = image.load("car.JPG")
carPic = transform.scale(carPic, (75,40))
curb1 = Rect(0, height - 50, width, 10)
curb2 = Rect(0, height - 170, width, 10)

frogRect = Rect (width // 2 - 20,height - 40,40,40)

mixer.music.load("coolsong.mp3")
mixer.music.play(-1)

while endGame == False:
    for e in event.get():
        if e.type == QUIT:
            endGame = True
        if e.type == KEYDOWN:
            if e.key == K_s:
                frogRect.move_ip(0,40)
            if e.key == K_w:
                frogRect.move_ip(0,-40)
            if e.key == K_a:
                frogRect.move_ip(-40,0)
            if e.key == K_d:
                frogRect.move_ip(40,0)
    screen.fill((0,0,0))
    draw.rect(screen, (255,255,255), (0,0,width,20))
    screen.blit(frogPic, frogRect)
    screen.blit(carPic, (350,275))
    draw.rect(screen, (128, 128, 128), curb1)
    draw.rect(screen, (128, 128, 128), curb2)
    display.update()
    time.delay(30)