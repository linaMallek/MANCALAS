import random
import sys
import time

import pygame

width = 1000
height = 700
screen = pygame.display.set_mode((width, height))

boardImage1 = pygame.image.load('images/BoardPlayer1.png')
boardImage2 = pygame.image.load('images/BoardPlayer2.png')

graine1 = pygame.image.load('images/graine1.png')
graine2 = pygame.image.load('images/graine2.png')
graine3 = pygame.image.load('images/graine3.png')
graine4 = pygame.image.load('images/graine4.png')

images = [graine1, graine2, graine3, graine4]

brown = (79, 60, 44)
red = (255, 0, 0)
yellow = (255, 255, 0)


class MancalaBoard:

    def __init__(self, bord):
        self.bord = bord
        self.indice_player1 = ("A", "B", "C", "D", "E", "F")
        self.indice_player2 = ("G", "H", "I", "J", "K", "L")

        self.suivant_player1 = {"A": "B", "B": "C", "C": "D", "D": "E", "E": "F", "F": "M1", "M1": "L", "L": "K",
                                "K": "J","J": "I", "I": "H", "H": "G", "G": "A"}

        self.suivant_player2 = {"A": "B", "B": "C", "C": "D", "D": "E", "E": "F", "F": "L", "L": "K", "K": "J",
                                "J": "I", "I": "H", "H": "G", "G":"M2", "M2": "A"}

        self.opposer_player1 = {"A": "G", "B": "H", "C": "I", "D": "J", "E": "K", "F": "L"}
        self.opposer_player2 = {"L": "F", "K": "E", "J": "D", "I": "C", "H": "B", "G": "A"}

        self.spotAreaPositions1 = {"A": [(224, 413), (283, 483)], "B": [(311, 439), (369, 512)],
                                   "C": [(407, 459), (468, 525)], "D": [(521, 461), (582, 524)],
                                   "E": [(621, 444), (684, 508)], "F": [(710, 417), (775, 474)],
                                   "M1": [(796, 281), (879, 427)], "G": [(225, 225), (284, 286)],
                                   "H": [(313, 194), (368, 257)], "I": [(410, 176), (467, 241)],
                                   "J": [(527, 174), (579, 243)], "K": [(628, 191), (680, 259)],
                                   "L": [(719, 215), (767, 287)], "M2": [(121, 277), (201, 428)]}

        self.spotAreaPositions2 = {"L": [(224, 413), (283, 483)], "K": [(311, 439), (369, 512)],
                                   "J": [(407, 459), (468, 525)], "I": [(521, 461), (582, 524)],
                                   "H": [(621, 444), (684, 508)], "G": [(710, 417), (775, 474)],
                                   "M2": [(796, 281), (879, 427)], "F": [(225, 225), (284, 286)],
                                   "E": [(313, 194), (368, 257)], "D": [(410, 176), (467, 241)],
                                   "C": [(527, 174), (579, 243)], "B": [(628, 191), (680, 259)],
                                   "A": [(719, 215), (767, 287)], "M1": [(121, 277), (201, 428)]}

        self.pathToMagasins1 = {"A": 6, "B": 5, "C": 4, "D": 3, "E": 2, "F": 1}
        self.pathToMagasins2 = {"L": 6, "K": 5, "J": 4, "I": 3, "H": 2, "G": 1}

    def drawBoard(self, bord):
        f = open("player-side.txt", "r")
        playerside = f.read()
        if int(playerside) == 1:
            screen.blit(boardImage1, (0, 0))
            self.displayText(screen, str(self.bord["M1"]), 900, 50, red, 28, False)
            self.displayText(screen, str(self.bord["M2"]), 100, 50, red, 28, False)
        else:
            screen.blit(boardImage2, (0, 0))
            self.displayText(screen, str(self.bord["M1"]), 100, 50, red, 28, False)
            self.displayText(screen, str(self.bord["M2"]), 900, 50, red, 28, False)
        for i in bord:
            if int(playerside) == 1:
                (posX1, posY1), (posX2, posY2) = self.spotAreaPositions1[i]
            else:
                (posX1, posY1), (posX2, posY2) = self.spotAreaPositions2[i]
            for _ in range(bord[i]):
                n = random.randint(0, 3)
                screen.blit(images[1],
                            (random.randint(posX1, posX2 - 20), random.randint(posY1, posY2 - 20)))
            pygame.draw.circle(screen, brown, ((posX1 + posX2) / 2, posY2), 20)
            self.displayText(screen, str(self.bord[i]), ((posX1 + posX2) / 2) - 5, posY2 - 15, yellow, 20, False)
        pygame.display.update()

    def showGameOverText(self, game):
        window_rect = pygame.Surface((width, height))
        window_rect.set_alpha(100)  # transparence
        pygame.draw.rect(window_rect, brown, window_rect.get_rect())
        screen.blit(window_rect, (0, 0))
        text_rect = pygame.Surface((width, 170))
        text_rect.set_alpha(200)  # transparence
        pygame.draw.rect(text_rect, brown, text_rect.get_rect())
        screen.blit(text_rect, (0, 220))
        # pygame.draw.rect(screen, (239, 223, 187), pygame.Rect(0, 220, width, 170))
        self.displayText(screen, f"GAME OVER ! {game.findWinner()}", 200, 300, (239, 223, 187), 60, True)
        time.sleep(4)
        sys.exit()

    def displayText(self, screen, text, x, y, color, size, center):
        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans MS", size)
        text = font.render(text, False, color)
        if center:
            text_rect = text.get_rect(center=(width // 2, y))
            screen.blit(text, text_rect)
        else:
            screen.blit(text, (x, y))
        pygame.display.update()

    def possibleMoves(self, player):

      
        indice_possible = []
        if player == 1:
            for i in self.indice_player1:
                if self.bord[i] > 0:
                    indice_possible.append(i)

        if player == -1:
            for i in self.indice_player2:
                if self.bord[i] > 0:
                    indice_possible.append(i)
        return indice_possible

    def doMove(self, player, i):
        if player == 1:
            suivant = self.suivant_player1
            indice = self.indice_player1
            opposer = self.opposer_player1
            Mag = "M1"
        else:
            suivant = self.suivant_player2
            indice = self.indice_player2
            opposer = self.opposer_player2
            Mag = "M2"
        j = i
        for x in range(self.bord[i]):
            self.bord[suivant[j]] += 1
            j = suivant[j]
            self.bord[i] = self.bord[i]-1
            time.sleep(0.5)
            self.drawBoard(self.bord)
            

       
        print(self.bord)
        if j != "M1" and j != "M2":
            
            if self.bord[j] == 1 and (j in indice) :
                self.bord[Mag] = self.bord[Mag] + self.bord[opposer[j]] + self.bord[j]
                self.bord[opposer[j]] = 0
                self.bord[j] = 0
                self.drawBoard(self.bord)
            return -player
        else:
            #self.bord[Mag] = self.bord[Mag] + 1
            self.drawBoard(self.bord)
            return player

    def doMove2(self, player, i):
        if player == 1:
            suivant = self.suivant_player1
            indice = self.indice_player1
            opposer = self.opposer_player1
            Mag = "M1"
        else:
            suivant = self.suivant_player2
            indice = self.indice_player2
            opposer = self.opposer_player2
            Mag = "M2"
        j = i
        for x in range(self.bord[i]):
            self.bord[suivant[j]] += 1
            j = suivant[j]
            self.bord[i] = self.bord[i]-1
            

        print("bord ni niden ")
        print(self.bord)
        if j != "M1" and j != "M2":
            
            if self.bord[j] == 1 and (j in indice) :
                self.bord[Mag] = self.bord[Mag] + self.bord[opposer[j]] + self.bord[j]
                self.bord[opposer[j]] = 0
                self.bord[j] = 0
              
            return -player
        else:
            return player