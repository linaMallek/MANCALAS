import math
import sys
import time

import pygame


from MancalaBoard import MancalaBoard, screen, red

Human = 1
Computer = -1
bord = {"A": 4, "B": 4, "C": 4, "D": 4, "E": 4, "F": 4, "M1": 0, "G": 4, "H": 4, "I": 4, "J": 4, "K": 4, "L": 4,
        "M2": 0}
manca = MancalaBoard(bord)


def getfosse(position, playerSide):
    x, y = position
    if playerSide == 1:
        if (224 <= x <= 283) and (413 <= y <= 483):
            return "A"
        if (311 <= x <= 369) and (439 <= y <= 512):
            return "B"
        if (407 <= x <= 468) and (459 <= y <= 525):
            return "C"
        if (521 <= x <= 582) and (461 <= y <= 524):
            return "D"
        if (621 <= x <= 684) and (444 <= y <= 508):
            return "E"
        if (710 <= x <= 775) and (417 <= y <= 474):
            return "F"

    else:
        if (224 <= x <= 283) and (413 <= y <= 483):
            return "L"
        if (311 <= x <= 369) and (439 <= y <= 512):
            return "K"
        if (407 <= x <= 468) and (459 <= y <= 525):
            return "J"
        if (521 <= x <= 582) and (461 <= y <= 524):
            return "I"
        if (621 <= x <= 684) and (444 <= y <= 508):
            return "H"
        if (710 <= x <= 775) and (417 <= y <= 474):
            return "G"


class Play:
    def humanTurn(self, game):
        global player
        move_made = False
        if not game.gameOver():
            while not move_made:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        fosse = getfosse(pos, game.playerSide)
                        if fosse in game.state.possibleMoves(game.playerSide):
                            player = game.state.doMove(game.playerSide, fosse)
                            move_made = True

            if player == game.playerSide:
                game.state.displayText(screen, "YOU PLAY AGAIN !", 380, 30,(139,69,19), 28, True)
                self.humanTurn(game)
            else:
                self.computerTurn(game)

        else:
            game.state.showGameOverText(game)

    def computerTurn(self, game):
        if not game.gameOver():
            alpha = -math.inf
            beta = math.inf
            time.sleep(1.5)
            #self.NegaMaxAlphaBetaPruning(game, Computer, 4, alpha, beta)
            # best move
            move = game.bestMoveHeuristic(game.state)
            if move != 0:
                thisplayer = game.state.doMove(game.playerSide, move)
                if thisplayer == game.playerSide:
                    self.humanTurn(game)
                else:
                    game.state.displayText(screen, "THE COMPUTER PLAYS AGAIN !", 380, 30,(139,69,19), 28, True)
                    self.computerTurn(game)
            else:
                # normal move
                self.NegaMaxAlphaBetaPruning(game, Computer, 4, alpha, beta)
                #self.minimax(4, Computer, game, alpha, beta)

        else:
            game.state.showGameOverText(game)

    def minimax(self, depth, Player, game, alpha, beta):
        MAX, MIN = 1000, -1000
        # Terminating condition
        # leaf node is reached
        if game.gameOver() or depth == 0:
            # return game.evaluate(), None
            return game.ourHeuristic(), None

        if Player == -game.playerSide:  # max
            best = MIN
            # Recur for left and right children
            for pit in game.state.possibleMoves(-game.playerSide):

                child_game = game
                # print(game.state)
                Player = child_game.state.doMove(-child_game.playerSide, pit)
                self.humanTurn(game)
                time.sleep(1)
                val = self.minimax(depth + 1, Player, child_game, MIN, MAX)
                best = max(best, val)
                alpha = max(alpha, best)
                self.humanTurn(game)
                time.sleep(1)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            print("best is" + str(best))
            return best

        else:
            best = MAX
            # Recur for left and
            # right children
            for pit in game.state.possibleMoves(-game.playerSide):
                child_game = game
                # print(game.state)
                Player = child_game.state.doMove(-game.playerSide, pit)
                self.humanTurn(game)
                time.sleep(1)
                val = self.minimax(depth + 1, Player, child_game, MIN, MAX)
                best = min(best, val)
                beta = min(beta, best)
                self.humanTurn(game)
                time.sleep(1)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best

    def NegaMaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        if game.gameOver() or depth == 1:
            bestValue = game.evaluate()
            #bestValue = game.ourHeuristic()
            bestPit = None
            if player == game.playerSide:
                bestValue = - bestValue

            return bestValue, bestPit

        bestValue = -math.inf
        bestPit = None
        for pit in game.state.possibleMoves(-game.playerSide):
            child_game = game
            child_game.state.doMove(-game.playerSide, pit)
            print(pit)
            self.humanTurn(game)
            time.sleep(1)
            value, _ = self.NegaMaxAlphaBetaPruning(child_game, -player, depth - 1, -beta, -alpha)
            value = - value
            self.humanTurn(game)
            time.sleep(1)
            if value > bestValue:
                bestValue = value
                bestPit = pit
            if bestValue > alpha:
                alpha = bestValue
            if beta <= alpha:
                break
        return bestValue, bestPit
