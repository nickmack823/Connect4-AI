import main
import time
from player import *


class Game:

    def __init__(self, player1, player2):
        self.move_history = []
        self.player1 = player1
        self.player2 = player2
        self.moves_considered_p1, self.moves_considered_p2 = 0, 0
        self.moves_made_p1, self.moves_made_p2 = 0, 0
        self.time_elapsed_p1, self.time_elapsed_p2 = 0, 0
        self.total_time = 0
        self.results = {'P1: ' + player1.label: 0, 'P2: ' + player2.label: 0, 'Draw': 0}
        self.board = Board()

    def playGame(self):
        """
        Plays one game of Connect4 using the current two players.
        """
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
                            move = self.player1.findMove(board.move_history, col)
                            # Move valid, continue onwards
                            if move is not None:
                                break
                # AI as Player 1
                else:
                    move = self.player1.findMove(board.move_history)
                if move is not None:
                    time_end_p1 = time.time()
                    self.time_elapsed_p1 += time_end_p1 - time_start_p1
                    self.moves_considered_p1 += self.player1.moves_considered
                    self.moves_made_p1 += 1
                    main.drawPiece(move, board.getMoveRow(move), main.RED)
                    time_start_p1 = None
                    # print("Player 1 move: " + str(move))
            if board.turn == 2:
                # print("Player 2 turn")
                time_start_p2 = time.time()
                move = self.player2.findMove(board.move_history)
                time_end_p2 = time.time()
                self.time_elapsed_p2 += time_end_p2 - time_start_p2
                self.moves_considered_p2 += self.player2.moves_considered
                self.moves_made_p2 += 1
                # print("Player 2 move: " + str(move))
                main.drawPiece(move, board.getMoveRow(move), main.YELLOW)
            if move is not None:
                # print(move)
                board.makeMove(move)
                # board.printBoard()

                if board.winner == 1:
                    print("Player 1 wins.")
                elif board.winner == 2:
                    print("Player 2 wins.")
                elif board.winner == 0:
                    print("Draw.")
                if board.winner is not None:
                    self.recordResult(board.winner)

    def recordResult(self, result):
        """
        Records the result of a game after it is completed.
        :param result: an integer indiciating whether Player 1 or Player 2 won the game
        :return:
        """
        if result == 1:
            self.results['P1: ' + self.player1.label] += 1
        elif result == 2:
            self.results['P2: ' + self.player2.label] += 1
        else:
            self.results["Draw"] += 1
        self.moves_considered_p1 += self.player1.moves_considered
        self.moves_considered_p2 += self.player2.moves_considered

    @classmethod
    def getPlayer(cls, selection, depth=None, heuristic=None):
        """
        Returns a Player object based on input arguments.
        :param selection: the type of player
        :param depth: the depth of the player (if applicable)
        :param heuristic: the herustic of the player (if applicable)
        :return:
        """
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
