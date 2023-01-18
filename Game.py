import sys
import time


from Play import Play
from MancalaBoard import MancalaBoard, screen, brown


class Game:
    def __init__(self, state, playerSide):
        self.state = state
        self.playerSide = playerSide

    def gameOver(self):
        vide1 = True
        vide2 = True
        
        for i in self.state.indice_player1:
            if self.state.bord[i] > 0:
                vide1 = False

        for i in self.state.indice_player2:
            if self.state.bord[i] > 0:
                vide2 = False

        if vide1==True:
            for i in self.state.indice_player2:
                self.state.bord["M2"] = self.state.bord["M2"] + self.state.bord[i]
                return True

        if vide2==True:
            for i in self.state.indice_player1:
                self.state.bord["M1"] = self.state.bord["M1"] + self.state.bord[i]
                return True

    def findWinner(self):
        if self.playerSide == 1:
            if self.state.bord["M1"] > self.state.bord["M2"]:
                return "COMPUTER 1 WON !"
            else:
                return "COMPUTER 2 LOST :("
        else:
            if self.state.bord["M2"] > self.state.bord["M1"]:
                return "COMPUTER 2 WON !"
            else:
                return "COMPUTER 2 LOST :("

    def evaluate(self):
        n = self.state.bord["M1"] - self.state.bord["M2"]
        return n

    def getNBgraines(self, manca):
        nb=0
        if self.playerSide == 1:
            for i in manca.indice_player1:
                nb = nb + manca.bord[i]
        else:
            for i in manca.indice_player2:
                nb = nb + manca.bord[i]
        return nb

    def getFirstleftNoneEmptyFosse(self, manca, player):
        index = manca.possibleMoves(player)[0]
        return index

    def ourHeuristic(self, manca, player):
        # la logique de cet heuristique a été déduié après avoir jouer plusieurs parties
        # elle consiste a faire avancer les billes de la premiere fosse pleine toute a gauche
        # mais de ne pas depacer le magasin ( derniere bille au maximum elle sera dans le magasin du player )
        global n
        if self.playerSide == -1:  # dans le cas win computer = player 2
            indexfosseGauche = self.getFirstleftNoneEmptyFosse(manca, player)
            nbGraineDansFosseGauche = self.state.bord[indexfosseGauche]
            nbDeGraines = self.getNBgraines(manca)  # la somme des billes dans les fosses player
            nbFosseVide = len(manca.possibleMoves( player))
            nbGrainemagasin = self.state.bord["M2"]
            for i in manca.indice_player2:
                if manca.bord[i] < 7 - manca.indice_player2.index(
                        i) and nbDeGraines > nbGrainemagasin and nbFosseVide > 0:
                    n = 7 - manca.bord[i]
        else:
            indexfosseGauche = self.getFirstleftNoneEmptyFosse(manca, player)
            nbGraineDansFosseGauche = self.state.bord[indexfosseGauche]
            nbDeGraines = self.getNBgraines(manca)  # la somme des billes dans les fosses player
            nbFosseVide = len(manca.possibleMoves(player))
            nbGrainemagasin = self.state.bord["M1"]
            for i in manca.indice_player1:
                if nbDeGraines > nbGrainemagasin and nbFosseVide > 0 and manca.bord[
                    i] <= 7 - manca.indice_player1.index(i):
                    n = 7 - manca.bord[i]
        return n

    def bestMoveHeuristic(self, manca):
        # cette heuristic elle consiste a jouer the best move
        # c-a-d jouer les fosses qui leurs nombre de graine = pathToMagasin
        # exemple: fosse C contient 4 graines et de C au magasin le path = 4
        # le computer va verifier avant chaque move si cette heuristic est réalisable
        global move
        if self.playerSide == -1:
            for i in manca.indice_player1:
                pathTomagasin = manca.pathToMagasins1[i]
                if self.state.bord[i] == pathTomagasin:
                    move = i
                    return move
                else:
                    move = 0  # PAS_REALISABLE
            return move
        else:
            for i in manca.indice_player2:
                pathTomagasin = manca.pathToMagasins2[i]
                if self.state.bord[i] == pathTomagasin:
                    move = i
                    return move
                else:
                    move = 0  # PAS_REALISABLE
            return move

        # prochaine etape: essayer de jouer un move qui va contrer le best move pour l'adverssaire
    
    def getfosse(self,position, playerSide):
     x, y = position
     if playerSide == 1:
        if (224 <= x <= 283) and (413 <= y <= 483):return "A"
        if (311 <= x <= 369) and (439 <= y <= 512):return "B"
        if (407 <= x <= 468) and (459 <= y <= 525):return "C"
        if (521 <= x <= 582) and (461 <= y <= 524):return "D"
        if (621 <= x <= 684) and (444 <= y <= 508):return "E"
        if (710 <= x <= 775) and (417 <= y <= 474):return "F"

     else:
        if (224 <= x <= 283) and (413 <= y <= 483):return "L"
        if (311 <= x <= 369) and (439 <= y <= 512):return "K"
        if (407 <= x <= 468) and (459 <= y <= 525):return "J"
        if (521 <= x <= 582) and (461 <= y <= 524):return "I"
        if (621 <= x <= 684) and (444 <= y <= 508):return "H"
        if (710 <= x <= 775) and (417 <= y <= 474):return "G"

        
    def main(self):
        play = Play()
        bord = {"A": 4, "B": 4, "C": 4, "D": 4, "E": 4, "F": 4, "M1": 0, "G": 4, "H": 4, "I": 4, "J": 4, "K": 4, "L": 4,
                "M2": 0}
        manca = MancalaBoard(bord)
        while not self.gameOver():
            if self.playerSide == 1:
                manca.displayText(screen, "COMPUTER 1 !", 380, 30, brown, 28, True)
                Play.computerTurn2(play, self)
            else:
                manca.displayText(screen, "COMPUTER 2 !", 350, 30, brown, 28, True)
                Play.computerTurn(play, self)
        time.sleep(5)
        sys.exit()
