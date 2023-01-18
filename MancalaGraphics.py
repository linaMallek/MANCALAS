import pygame
import sys
from Game import Game
from MancalaBoard import MancalaBoard

width = 1000
height = 700
screen = pygame.display.set_mode((width, height))

gameOver = False

menuImage = pygame.image.load('images/m.png')
aroow = pygame.image.load('images/Arrow.png')

screen.blit(menuImage, (0, 0))

x = 635
y = 330
screen.blit(aroow, (x, y))
clock = pygame.time.Clock()

bord = {"A": 4, "B": 4, "C": 4, "D": 4, "E": 4, "F": 4, "M1": 0, "G": 4, "H": 4, "I": 4, "J": 4, "K": 4, "L": 4,
        "M2": 0}

manca = MancalaBoard(bord)


def player1():
    playerSide = 1
    f = open("player-side.txt", "w")
    f.write(str(playerSide))
    f.close()
    manca.drawBoard(manca.bord)
    pygame.display.update()
    game = Game(manca, playerSide)
    game.main()


def player2():
    playerSide = -1
    f = open("player-side.txt", "w")
    f.write(str(playerSide))
    f.close()
    manca.drawBoard(manca.bord)
    pygame.display.update()
    game = Game(manca, playerSide)
    game.main()


while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            posX, posY = pygame.mouse.get_pos()
            if (348 <= posX <= 633) and (304 <= posY <= 382):  # PLAYER1
                player1()
            if (355 <= posX <= 632) and (417 <= posY <= 495):  # PLAYER2
                player2()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        if y == 330:
            y += 120
            screen.blit(menuImage, (0, 0))
            screen.blit(aroow, (x, y))
    if keys[pygame.K_UP]:
        if y == 450:
            y -= 120
            screen.blit(menuImage, (0, 0))
            screen.blit(aroow, (x, y))

    if keys[pygame.K_RETURN] and y == 330:  # PLAYER1
        player1()

    if keys[pygame.K_RETURN] and y != 330:  # PLAYER1
        player2()

    pygame.display.update()
    clock.tick(30)

quit()
