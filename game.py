import sys

import main
from player import *
import time
import math


class Game:

    def __init__(self, player1, player2):
        self.move_history = []
        self.player1 = player1
        self.player2 = player2
        self.moves_considered_p1, self.moves_considered_p2 = 0, 0
        self.time_elapsed_p1, self.time_elapsed_p2 = 0, 0
        self.total_time = 0
        self.results = {'P1: ' + player1.label: 0, 'P2: ' + player2.label: 0, 'Draw': 0}
        self.board = Board()

    def playGame(self):
        board = self.board
        main.drawBoard()
        self.player1.moves_considered, self.player2.moves_considered = 0, 0
        print(self.player1.label + " vs. " + self.player2.label)
        time_start_p1 = None

        while not board.game_over:
            move = None
            if board.turn == 1:
                time_start_p1 = time.time() if time_start_p1 is None else time_start_p1
                # If user playing manually
                if self.player1.label == 'Manual':
                    for event in main.pygame.event.get():
                        if event.type == main.pygame.MOUSEMOTION:
                            x = event.pos[0]
                            main.drawHoveringPiece(x, main.RED)
                        elif event.type == main.pygame.MOUSEBUTTONDOWN:
                            x = event.pos[0]
                            col = int(math.floor(x / main.SQUARE_SIZE))
                            print(col)
                            move = self.player1.findMove(board.move_history, col)
                            print("Move: " + str(move))
                            # Move valid, continue onwards
                            if move is not None:
                                break
                # AI as Player 1
                else:
                    move = self.player1.findMove(board.move_history)
                    print(move)
                if move is not None:
                    time_end_p1 = time.time()
                    print(time_start_p1)
                    print(time_end_p1)
                    self.time_elapsed_p1 += time_end_p1 - time_start_p1
                    print(self.time_elapsed_p1)
                    main.drawPiece(move, board.getMoveRow(move), main.RED)
                    time_start_p1 = None
                    print("Player 1 move: " + str(move))
            if board.turn == 2:
                print("Player 2 turn")
                time_start_p2 = time.time()
                move = self.player2.findMove(board.move_history)
                time_end_p2 = time.time()
                self.time_elapsed_p2 += time_end_p2 - time_start_p2
                print("Player 2 move: " + str(move))
                main.drawPiece(move, board.getMoveRow(move), main.YELLOW)
            if move is not None:
                # print(move)
                board.makeMove(move)
                # board.printBoard()

                self.moves_considered_p1 += self.player1.moves_considered
                self.moves_considered_p2 += self.player2.moves_considered

                if board.winner == 1:
                    print("Player 1 wins.")
                elif board.winner == 2:
                    print("Player 2 wins.")
                elif board.winner == 0:
                    print("Draw.")
                if board.winner is not None:
                    self.recordResult(board.winner)

    def recordResult(self, result):
        if result == 1:
            self.results['P1: ' + self.player1.label] += 1
        elif result == 2:
            self.results['P2: ' + self.player2.label] += 1
        else:
            self.results["Draw"] += 1
        self.moves_considered_p1 += self.player1.moves_considered
        self.moves_considered_p2 += self.player2.moves_considered

    # def testSuite(self, n):
    #     randPlayer = PlayerRandom()
    #     minimaxPlayer = PlayerMM(3, 1)  # Uses depth 3 and heuristic 1 by default
    #     alphaBetaPlayer = PlayerAB(3, 1)  # Uses depth 3 and heuristic 1 by default
    #     monteCarloPlayer = PlayerMC(100)  # Performs 100 test games by default
    #     players = [randPlayer, minimaxPlayer, alphaBetaPlayer, monteCarloPlayer]
    #     games = []
    #     matchups = []
    #
    #     # Generate a Game for all possible matchups given the Player instances we have
    #     for player in players:
    #         # Random doesn't deserve to be player 1
    #         if player.label == "Random":
    #             continue
    #         for otherPlayer in players:
    #             # Avoid putting Player against itself
    #             if otherPlayer != player:
    #                 matchup = player.label + "/" + otherPlayer.label
    #                 reversedMatchup = otherPlayer.label + "/" + player.label
    #                 # Create Game for matchup if these two Players aren't already set to go against each other
    #                 if matchup not in matchups and reversedMatchup not in matchups:
    #                     matchups.append(matchup)
    #                     game = Game(player, otherPlayer)
    #                     games.append(game)
    #
    #     # Play each game in games n times
    #     for iteration in range(0, n):
    #         for game in games:
    #             game.playGame()
    #     self.printResults(games, n)

    @classmethod
    def getPlayer(cls, selection, depth=None, heuristic=None):
        player = None
        if selection == 1:
            player = ManualPlayer()
        elif selection == 2:
            player = PlayerRandom()
        elif selection == 3:
            player = PlayerMM(depth, heuristic)
        elif selection == 4:
            player = PlayerAB(depth, heuristic)
        elif selection == 5:
            player = PlayerMC(depth)
        return player

