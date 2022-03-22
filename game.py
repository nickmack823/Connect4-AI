import sys

from player import *
import time
import pygame
import pygame_menu
import math

pygame.init()

BLUE = (0, 0, 255)
LIGHTBLUE = (0, 75, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHTGREY = (170, 170, 170)
DARKGREY = (100, 100, 100)

COLUMN_COUNT = 7
ROW_COUNT = 6

SQUARE_SIZE = 90
RADIUS = int(SQUARE_SIZE / 2 - 7)

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 2) * SQUARE_SIZE
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
screen.fill(LIGHTBLUE)

titleFont = pygame.font.SysFont('calibri', 50)
buttonFont = pygame.font.SysFont('arial', 30)


gameCount = 0
player1Selection = 1
player2Selection = 2
player1depth = None
player2depth = None
player1TestGamesMC = None
player2TestGamesMC = None


def showMainMenu():
    menuFontSize = 60
    menu = pygame_menu.Menu('Connect4 AI', width, height,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Run Game(s)', showConfigureGameMenu, font_size=menuFontSize)
    menu.add.button('Data', showData, font_size=menuFontSize)
    menu.add.button('Quit', pygame_menu.events.EXIT, font_size=menuFontSize)
    menu.mainloop(screen)


def showConfigureGameMenu():
    print("Showing Game Configuration Menu")

    menu = pygame_menu.Menu('Connect4 AI', width, height,
                            theme=pygame_menu.themes.THEME_BLUE)

    def updateGameCount():
        global gameCount
        inputBox = menu.get_widget('gameCount')
        if inputBox is not None:
            gameCount = inputBox.get_value()
        print(gameCount)

    menu.add.text_input('Number of Games: ', textinput_id='gameCount', onchange=updateGameCount)

    def updateP1Depth(input):
        global player1depth
        player1depth = int(input) if input.isnumeric() else None
        print(player1depth)
    def updateP2Depth(input):
        global player2depth
        player2depth = int(input) if input.isnumeric() else None
        print(player2depth)
    def updateP1TestGames(input):
        global player1TestGamesMC
        player1TestGamesMC = int(input) if input.isnumeric() else None
        print(player1TestGamesMC)
    def updateP2TestGames(input):
        print("UPDATE P2 TEST GAMES")
        global player2TestGamesMC
        player2TestGamesMC = int(input) if input.isnumeric() else None
        print(player2TestGamesMC)

    menu.add.text_input('Maximum Depth (P1): ', textinput_id='depthP1', onchange=updateP1Depth).hide()
    menu.add.text_input('Monte Carlo Test Games Per Move (P1): ', textinput_id='testGamesP1',
                        onchange=updateP1TestGames).hide()
    menu.add.text_input('Maximum Depth (P2): ', textinput_id='depthP2', onchange=updateP2Depth).hide()
    menu.add.text_input('Monte Carlo Test Games Per Move (P2): ', textinput_id='testGamesP2',
                        onchange=updateP2TestGames).hide()

    def updateP1(name, value):
        global player1Selection
        player1Selection = value
        # Show Minimax/Alpha-Beta setting
        if value == 3 or value == 4:
            menu.get_widget('depthP1').show()
            menu.get_widget('testGamesP1').hide()
        # Show Monte Carlo setting
        elif value == 5:
            menu.get_widget('testGamesP1').show()
            menu.get_widget('depthP1').hide()

    def updateP2(name, value):
        global player2Selection
        player2Selection = value
        if value == 3 or value == 4:
            menu.get_widget('depthP2').show()
            menu.get_widget('testGamesP2').hide()
        elif value == 5:
            menu.get_widget('testGamesP2').show()
            menu.get_widget('depthP2').hide()

    menu.add.selector('Player 1 ',
                      [('You', 1), ('Random', 2), ('MiniMax', 3), ('Alpha-Beta', 4), ('Monte Carlo', 5)],
                      selector_id='p1', onchange=updateP1)

    menu.add.selector('Player 2 ', [('Random', 2), ('MiniMax', 3), ('Alpha-Beta', 4), ('Monte Carlo', 5)],
                      selector_id='p2', onchange=updateP2)


    menu.add.button('', selection_effect=None)
    menu.add.button('Play', startGames, font_size=50, button_id='play')
    menu.mainloop(screen)


def startGames():
    print("Starting Game(s)")
    if player1Selection is not None and player2Selection is not None:
        p1Value = None
        p2Value = None
        if player1Selection == 3 or player1Selection == 4:
            p1Value = player1depth
            if p1Value is None:
                return
        elif player1Selection == 5:
            p1Value = player1TestGamesMC
            if p1Value is None:
                return
        if player2Selection == 3 or player2Selection == 4:
            p2Value = player2depth
            if p2Value is None:
                return
        elif player2Selection == 5:
            p2Value = player2TestGamesMC
            if p2Value is None:
                return
            print("P2 TEST GAMES: " + str(player2TestGamesMC))

        p1 = Game.getPlayer(player1Selection, p1Value)
        p2 = Game.getPlayer(player2Selection, p2Value)
        game = Game(p1, p2)
        game.playGame()


def showData():
    pass


def drawBoard():
    screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE*2, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                               int(r * SQUARE_SIZE + SQUARE_SIZE*3 - SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def drawPiece(column, row, color):
    pygame.draw.circle(screen, color, (int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
                                       int(row * SQUARE_SIZE + SQUARE_SIZE*3 - SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def drawHoveringPiece(x, color):
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
    pygame.draw.circle(screen, color, (x, int(SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


class Game:

    def __init__(self, player1, player2):
        self.move_history = []
        self.player1 = player1
        self.player2 = player2
        self.total_moves_p1, self.total_moves_p2 = 0, 0
        self.time_elapsed_p1, self.time_elapsed_p2 = 0, 0
        self.total_time = 0
        self.results = {player1.label: 0, player2.label: 0, 'Draw': 0}
        self.board = Board()

    def playGame(self):
        board = self.board
        drawBoard()
        self.player1.moves_considered, self.player2.moves_considered = 0, 0
        print(self.player1.label + " vs. " + self.player2.label)

        while not board.game_over:
            move = None
            if board.turn == 1:
                time_start = time.time()
                # If user playing manually
                if player1Selection == 1:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEMOTION:
                            x = event.pos[0]
                            drawHoveringPiece(x, RED)
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            x = event.pos[0]
                            col = int(math.floor(x / SQUARE_SIZE))
                            print(col)
                            move = self.player1.findMove(self.player1, board.move_history, col)
                            print("Move: " + str(move))
                            # Move valid, continue onwards
                            if move is not None:
                                break
                # AI as Player 1
                else:
                    move = self.player1.findMove(self.player1, board.move_history)
                    print(move)
                if move is not None:
                    time_end = time.time()
                    self.time_elapsed_p1 += time_end - time_start
                    drawPiece(move, board.getMoveRow(move), RED)
                    print("Player 1 move: " + str(move))
            if board.turn == 2:
                print("Player 2 turn")
                time_start = time.time()
                move = self.player2.findMove(board.move_history)
                time_end = time.time()
                self.time_elapsed_p2 += time_end - time_start
                print("Player 2 move: " + str(move))
                drawPiece(move, board.getMoveRow(move), YELLOW)
            if move is not None:
                print(move)
                board.makeMove(move)
                board.printBoard()

                self.total_moves_p1 += self.player1.moves_considered
                self.total_moves_p2 += self.player2.moves_considered

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
            self.results[self.player1.label] += 1
        elif result == 2:
            self.results[self.player2.label] += 1
        else:
            self.results["Draw"] += 1
        self.total_moves_p1 += self.player1.moves_considered
        self.total_moves_p2 += self.player2.moves_considered

    def testSuite(self, n):
        randPlayer = PlayerRandom()
        minimaxPlayer = PlayerMM(3, 1)  # Uses depth 3 and heuristic 1 by default
        alphaBetaPlayer = PlayerAB(3, 1)  # Uses depth 3 and heuristic 1 by default
        monteCarloPlayer = PlayerMC(100)  # Performs 100 test games by default
        players = [randPlayer, minimaxPlayer, alphaBetaPlayer, monteCarloPlayer]
        games = []
        matchups = []

        # Generate a Game for all possible matchups given the Player instances we have
        for player in players:
            # Random doesn't deserve to be player 1
            if player.label == "Random":
                continue
            for otherPlayer in players:
                # Avoid putting Player against itself
                if otherPlayer != player:
                    matchup = player.label + "/" + otherPlayer.label
                    reversedMatchup = otherPlayer.label + "/" + player.label
                    # Create Game for matchup if these two Players aren't already set to go against each other
                    if matchup not in matchups and reversedMatchup not in matchups:
                        matchups.append(matchup)
                        game = Game(player, otherPlayer)
                        games.append(game)

        # Play each game in games n times
        for iteration in range(0, n):
            for game in games:
                game.playGame()
        self.printResults(games, n)

    def printResults(self, games, n):
        for game in games:
            p1 = game.player1.label
            p2 = game.player2.label
            if len(games) == 1:
                game_number = " "
            else:
                game_number = " " + str(games.index(game) + 1) + " "
            print("\nGAME" + game_number + "RESULTS (" + p1 + " vs. " + p2 + ")\n")
            print(p1 + " vs. " + p2 + " (" + str(n) + " games)")
            if p1 == "Minimax" or p1 == "Alpha-Beta":
                print(p1 + " depth: " + str(game.player1.max_depth))
            if p2 == "Minimax" or p2 == "Alpha-Beta":
                print(p2 + " depth: " + str(game.player2.max_depth))
            if p1 == "Monte Carlo":
                print("Random games played per possible move (Monte Carlo): " + str(game.player1.test_total))
            elif p2 == "Monte Carlo":
                print("Random games played per possible move (Monte Carlo): " + str(game.player2.test_total))
            print("Results: " + str(game.results))
            print("\nPlayer 1 (" + p1 + ")")
            print("Total moves considered: " + "{:,}".format(game.total_moves_p1))
            print("Average moves considered per game: " + "{:,}".format(game.total_moves_p1 / n))
            print("Time spent considering moves: " + str(round(game.time_elapsed_p1, 2)) + " seconds")
            print("Average time spent per game: " + str(round(game.time_elapsed_p1 / n, 2)) + " seconds")
            print("\nPlayer 2 (" + p2 + ")")
            print("Total moves considered: " + "{:,}".format(game.total_moves_p2))
            print("Average moves considered per game: " + "{:,}".format(game.total_moves_p2 / n))
            print("Time spent considering moves: " + str(round(game.time_elapsed_p2, 2)) + " seconds")
            print("Average time spent per game: " + str(round(game.time_elapsed_p2 / n, 2)) + " seconds")

    @classmethod
    def getPlayer(cls, selection, parameterValue):
        player = None
        if selection == 1:
            player = ManualPlayer
        elif selection == 2:
            player = PlayerRandom
        elif selection == 3:
            player = PlayerMM(parameterValue)
        elif selection == 4:
            player = PlayerAB(parameterValue)
        elif selection == 5:
            print("MC value: " + str(parameterValue))
            player = PlayerMC(parameterValue)
        return player

    @classmethod
    def getOpponent(cls, selection):
        opponents = ["Random", "Minimax", "Alpha-Beta", "Monte Carlo"]
        for opponent in opponents:
            if opponents.index(opponent) == selection - 1:
                return opponent
        # Returns None if invalid input
        return None


# if __name__ == "__main__":
#     print("Welcome to Connect Four!")
#     print("Would you like to run the standard test suite (1), or would you like to customize your game (2)?")
#     game_suite = int(input())
#     if game_suite == 1:
#         print("Games to run in the test suite: ")
#         n = int(input())
#         g1 = Game(PlayerRandom(None), PlayerRandom(None))
#         total_time = time.time()
#         g1.testSuite(n)
#         total_time = time.time() - total_time
#         print("\nTOTAL TIME ELAPSED: " + str(round(total_time, 2)) + " seconds.")
#     else:
#         print("Please select your player type: (1) Minimax, (2) Alpha-Beta, (3) Monte Carlo, (4) Manual")
#         character = int(input())
#         # Get player type from input
#         player_type = Game.getPlayer(character)
#         if player_type is None:
#             print("You did not enter a valid option")
#         else:
#             if player_type == "Minimax" or player_type == "Alpha-Beta":
#                 depth = int(input("What do you want the maximum depth of your search to be: "))
#                 heuristic = int(input("Which heuristic do you want to use (1, 2, or 3): "))
#                 if player_type == "Minimax":
#                     player = PlayerMM(depth, heuristic)
#                 elif player_type == "Alpha-Beta":
#                     player = PlayerAB(depth, heuristic)
#             elif player_type == "Monte Carlo":
#                 tests = int(input("Monte Carlo test count per move: "))
#                 player = PlayerMC(tests)
#             else:
#                 player = ManualPlayer()
#             print("Please select your opponent: (1) Random, (2) Minimax, (3) Alpha-Beta, (4) Monte Carlo")
#             opponent = int(input())
#             opponent_type = Game.getOpponent(opponent)
#             if opponent_type is None:
#                 print("You did not enter a valid option")
#             else:
#                 if opponent_type == "Minimax" or opponent_type == "Alpha-Beta":
#                     opponent_depth = int(input("Opponent maximum depth: "))
#                     opponent_heuristic = int(input("Opponent heuristic (1, 2, or 3): "))
#                     if opponent_type == "Minimax":
#                         opponent = PlayerMM(opponent_depth, opponent_heuristic)
#                     elif opponent_type == "Alpha-Beta":
#                         opponent = PlayerAB(opponent_depth, opponent_heuristic)
#                 elif opponent_type == "Monte Carlo":
#                     opponent_tests = int(input("Opponent Monte Carlo test count per move: "))
#                     opponent = PlayerMC(opponent_tests)
#                 else:
#                     opponent = PlayerRandom()
#
#                 game_count = int(input("How many games would you like to play: "))
#                 g = Game(player, opponent)
#                 for game in range(0, game_count):
#                     g.playGame()
#                 g.printResults([g], game_count)

if __name__ == "__main__":
    showMainMenu()

    p1 = ManualPlayer()
    p2 = PlayerRandom()
    g = Game(p1, p2)

    # g.drawBoard()
    # g.playGame()
