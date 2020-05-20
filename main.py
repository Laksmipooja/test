import random

import math

import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption(" Go Corona ", "Earthians stay safe")

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

bg = pygame.image.load("bg.jpg")

mixer.music.load("Frozen-Plasma__.wav")
mixer.music.play(-1)

playerimg = pygame.image.load('player.png')
playerx = 355
playery = 420
playerxchange = 0

enemyimg = []
enemyx = []
enemyy = []
enemyxchange = []
enemyychange = []
noofenemies = 10
for i in range(noofenemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 750))
    enemyy.append(random.randint(50, 150))
    enemyxchange.append(3)
    enemyychange.append(40)



score = 0
font = pygame.font.Font('font.ttf', 32)

cfont = pygame.font.Font('font.ttf', 32)

overfont = pygame.font.Font('icecube.ttf', 224)


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def firedrop(x, y):
    global dropstate
    dropstate = "fire"
    screen.blit(dropimg,(x+70,y-5))


def collision(enemyx, enemyy, dropx, dropy):
    dis = math.hypot(enemyx - dropx, enemyy - dropy)
    if dis < 40:
        return True
    else:
        return False


textx = 20
texty = 30


def showscore(x, y):
    score1 = font.render("SCORE :  " + str(score), True, (0, 0, 0))
    screen.blit(score1, (x, y))


gameOver = mixer.Sound('gameover.wav')
gameover = 1


def gameover():
    gameover1 = overfont.render("GAME OVER", True, (0, 0, 0))
    screen.blit(gameover1, (50, 100))




speed1 = 0


def setlevel(score, speed):
    speed1 = 2

    if score < 20:
        speed1 += 2
    elif score < 40:
        speed1 += 4
    elif score < 80:
        speed1 += 8
    else:
        speed1 += 10
    return speed1

dropimg = pygame.image.load('spray.png')
dropx = 0
dropy = 470
dropxchange = 0
dropychange = 25
dropstate = "ready"


playgameover: bool = True
running = True



while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerxchange = -6
            if event.key == pygame.K_RIGHT:
                playerxchange = 6
            if event.key == pygame.K_SPACE:
                if dropstate == "ready":
                    dropSound = mixer.Sound("watersplash.wav")
                    dropSound.play()
                    dropx = playerx
                    dropy=playery
                    firedrop(dropx, dropy)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerxchange = 0

    playerx += playerxchange
    if playerx <= 0:
        playerx = 0
    elif playerx >= 700:
        playerx = 700

    for i in range(noofenemies):
        speed = (setlevel(score, speed1))
        if enemyy[i] > 450:

            pygame.mixer.music.stop()
            if playgameover:
                playgameover: bool = False
                gameOver.play()

            for j in range(noofenemies):
                enemyy[j] = 2000
                gameover()
            break
        enemyx[i] += enemyxchange[i]
        if enemyx[i] <= 0:
            enemyxchange[i] = speed
            enemyy[i] += enemyychange[i]
        elif enemyx[i] >= 750:
            enemyxchange[i] = -(speed * speed / speed)
            enemyy[i] += enemyychange[i]

        coll = collision(enemyx[i], enemyy[i], dropx, dropy)
        if coll:
            collSound = mixer.Sound("destroy.wav")
            collSound.play()
            dropy = 480
            dropstate = "ready"
            score += 1
            enemyx[i] = random.randint(0, 750)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)

    if dropy <= 0:
        dropy = 480
        dropstate = "ready"
    if dropstate == "fire":
        firedrop(dropx, dropy)
        dropy -= dropychange

    player(playerx, playery)

    showscore(textx, texty)

    pygame.display.update()

    screen.blit(bg, [0, 0])
