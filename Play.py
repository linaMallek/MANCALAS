import math
import sys
import time
from copy import deepcopy
import pygame


from MancalaBoard import MancalaBoard, screen, red


bord = {"A": 4, "B": 4, "C": 4, "D": 4, "E": 4, "F": 4, "M1": 0, "G": 4, "H": 4, "I": 4, "J": 4, "K": 4, "L": 4,
        "M2": 0}
manca = MancalaBoard(bord)

class Play:
    def humanTurn(self, game):
        global player
        move_made = False
        if not game.gameOver():
            while not move_made:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        position = pygame.mouse.get_pos()
                        fosse = game.getfosse(position, game.playerSide)
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
            #best move 
            move = game.bestMoveHeuristic(game.state)
            if move != 0:
                thisplayer = game.state.doMove(-game.playerSide, move)
                if thisplayer == game.playerSide:
                    self.computerTurn2(game)
                else:
                    game.state.displayText(screen, "THE COMPUTER 2 PLAYS AGAIN !", 380, 30,(139,69,19), 28, True)
                    self.computerTurn(game)
            else:
                # normal move
                move , best_move=self.minmaxAlphaBetaPruning(4,-game.playerSide, game, alpha, beta)
                thisplayer = game.state.doMove(-game.playerSide, best_move)
                if thisplayer == game.playerSide:
                    self.computerTurn2(game)
                else:
                    game.state.displayText(screen, "THE COMPUTER 2 PLAYS AGAIN !", 380, 30,(139,69,19), 28, True)
                    self.computerTurn(game)            

        else:
            game.state.showGameOverText(game)


    def computerTurn2(self, game):
         if not game.gameOver():
            alpha = -math.inf
            beta = math.inf
            time.sleep(1.5)
            #best move 
            
                # normal move
            move , best_move=self.minmaxAlphaBetaPruning2(6,game.playerSide, game, alpha, beta)
            thisplayer = game.state.doMove(game.playerSide, best_move)

            if thisplayer == -game.playerSide:
                    self.computerTurn(game)
            else:
                    game.state.displayText(screen, "COMPUTER 1 PLAYS AGAIN !", 380, 30,(139,69,19), 28, True)
                    self.computerTurn2(game)            

         else:
            game.state.showGameOverText(game)    


  
  

    def NegaMaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        if game.gameOver() or depth == 1:
            #bestValue = game.evaluate()
            bestValue = game.ourHeuristic()
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

    def minmaxAlphaBetaPruning(self, depth, Player, game, alpha, beta):
        if   depth == 0 or game.gameOver():
            return game.ourHeuristic(game.state,Player), None

        if Player == -game.playerSide :
            best_value = -math.inf
            best_move = None
            for move in game.state.possibleMoves(Player):
                new_game = deepcopy(game)
                Player=new_game.state.doMove2(Player, move)
                value, _ = self.minmaxAlphaBetaPruning(depth - 1,Player,new_game, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            return best_value, best_move
        else:
            best_value = math.inf
            best_move = None
            for move in game.state.possibleMoves(Player):
                new_game = deepcopy(game)
                Player=new_game.state.doMove2(Player, move)
                value, _ = self.minmaxAlphaBetaPruning(depth - 1,Player,new_game, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
            return best_value, best_move

    def minmaxAlphaBetaPruning2(self, depth, Player, game, alpha, beta):
        if   depth == 0 or game.gameOver():
            return game.evaluate(), None

        if Player == game.playerSide :
            best_value = -math.inf
            best_move = None
            for move in game.state.possibleMoves(Player):
                new_game = deepcopy(game)
                Player=new_game.state.doMove2(Player, move)
                value, _ = self.minmaxAlphaBetaPruning(depth - 1,Player,new_game, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            return best_value, best_move
        else:
            best_value = math.inf
            best_move = None
            for move in game.state.possibleMoves(Player):
                new_game = deepcopy(game)
                Player=new_game.state.doMove2(Player, move)
                value, _ = self.minmaxAlphaBetaPruning(depth - 1,Player,new_game, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
            return best_value, best_move