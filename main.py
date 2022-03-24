import pygame
import pygame_menu
import tkinter
import game

from database import Database
from tkinter import *
from tkinter.ttk import Treeview

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

TITLE_FONT = pygame.font.SysFont('calibri', 50)
BUTTON_FONT = pygame.font.SysFont('arial', 30)
MAIN_MENU_FONT_SIZE = 60

p1Selection = 1
p2Selection = 2
gameCount = 0

p1Depth, p2Depth, p1TestGamesMC, p2TestGamesMC = 0, 0, 0, 0
p1Heuristic, p2Heuristic = 1, 1

menu = None
database = None


def showMainMenu():
    menu = pygame_menu.Menu('Connect4 AI', screen.get_width(), screen.get_height(),
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Run Game(s)', showConfigureGameMenu, font_size=MAIN_MENU_FONT_SIZE)
    menu.add.button('Data', showDataWindow, font_size=MAIN_MENU_FONT_SIZE)
    menu.add.button('Quit', pygame_menu.events.EXIT, font_size=MAIN_MENU_FONT_SIZE)
    menu.mainloop(screen)


def showConfigureGameMenu():
    print("Showing Game Configuration Menu")

    menu = pygame_menu.Menu('Connect4 AI', width, height,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Back', showMainMenu, font_size=30, padding=20)

    def updateGameCount(input):
        global gameCount
        gameCount = int(input) if input.isnumeric() else 0
        print(gameCount)

    menu.add.text_input('Number of Games: ', textinput_id='gameCount', onchange=updateGameCount)

    def updateP1Depth(input):
        global p1Depth
        p1Depth = int(input) if input.isnumeric() else None

    def updateP1Heuristic(name, value):
        global p1Heuristic
        p1Heuristic = value

    def updateP2Heuristic(name, value):
        global p2Heuristic
        p2Heuristic = value

    def updateP1TestGames(input):
        global p1TestGamesMC
        p1TestGamesMC = int(input) if input.isnumeric() else None

    def updateP2Depth(input):
        global p2Depth
        p2Depth = int(input) if input.isnumeric() else None

    def updateP2TestGames(input):
        global p2TestGamesMC
        p2TestGamesMC = int(input) if input.isnumeric() else None

    menu.add.text_input('Maximum Depth (P1): ', textinput_id='depthP1', onchange=updateP1Depth).hide()
    menu.add.selector('Heuristic (P1): ', [('Adjacent Pieces', 1), ('Piece Locations', 2), ('Connected Pieces', 3)],
                      selector_id='heuristicP1', onchange=updateP1Heuristic).hide()
    menu.add.text_input('Monte Carlo Test Games Per Move (P1): ', textinput_id='testGamesP1',
                        onchange=updateP1TestGames).hide()
    menu.add.text_input('Maximum Depth (P2): ', textinput_id='depthP2', onchange=updateP2Depth).hide()
    menu.add.selector('Heuristic (P2): ', [('Adjacent Pieces', 1), ('Piece Locations', 2), ('Connected Pieces', 3)],
                      selector_id='heuristicP2', onchange=updateP2Heuristic).hide()
    menu.add.text_input('Monte Carlo Test Games Per Move (P2): ', textinput_id='testGamesP2',
                        onchange=updateP2TestGames).hide()

    def updateP1(name, value):
        global p1Selection
        p1Selection = value
        # Show Minimax/Alpha-Beta setting
        if value == 3 or value == 4:
            menu.get_widget('depthP1').show()
            menu.get_widget('heuristicP1').show()
            menu.get_widget('testGamesP1').hide()
        # Show Monte Carlo setting
        elif value == 5:
            menu.get_widget('testGamesP1').show()
            menu.get_widget('depthP1').hide()
            menu.get_widget('heuristicP1').hide()
        else:
            menu.get_widget('depthP1').hide()
            menu.get_widget('heuristicP1').hide()
            menu.get_widget('testGamesP1').hide()

    def updateP2(name, value):
        global p2Selection
        p2Selection = value
        if value == 3 or value == 4:
            menu.get_widget('depthP2').show()
            menu.get_widget('heuristicP2').show()
            menu.get_widget('testGamesP2').hide()
        elif value == 5:
            menu.get_widget('testGamesP2').show()
            menu.get_widget('depthP2').hide()
            menu.get_widget('heuristicP2').hide()
        else:
            menu.get_widget('depthP2').hide()
            menu.get_widget('heuristicP2').hide()
            menu.get_widget('testGamesP2').hide()

    menu.add.selector('Player 1 ', [('You', 1), ('Random', 2), ('MiniMax', 3), ('Alpha-Beta', 4), ('Monte Carlo', 5)],
                      selector_id='p1', onchange=updateP1)
    menu.add.selector('Player 2 ', [('Random', 2), ('MiniMax', 3), ('Alpha-Beta', 4), ('Monte Carlo', 5)],
                      selector_id='p2', onchange=updateP2)
    # menu.add.button('', selection_effect=None)
    menu.add.button('Play', runGames, font_size=50, padding=25, button_id='play')
    menu.mainloop(screen)


def showDataWindow():
    app = Tk()
    frame_search = Frame(app)
    frame_search.grid(row=0, column=0)

    # lbl_search = Label(frame_search, text='Search by hostname',
    #                    font=('bold', 12), pady=20)
    # lbl_search.grid(row=0, column=0, sticky=W)
    # hostname_search = StringVar()
    # hostname_search_entry = Entry(frame_search, textvariable=hostname_search)
    # hostname_search_entry.grid(row=0, column=1)
    #
    # lbl_search = Label(frame_search, text='Search by Query',
    #                    font=('bold', 12), pady=20)
    # lbl_search.grid(row=1, column=0, sticky=W)
    # query_search = StringVar()
    # query_search.set("Select * from routers where ram>1024")
    # query_search_entry = Entry(frame_search, textvariable=query_search, width=40)
    # query_search_entry.grid(row=1, column=1)
    #
    # frame_fields = Frame(app)
    # frame_fields.grid(row=1, column=0)
    # # hostname
    # hostname_text = StringVar()
    # hostname_label = Label(frame_fields, text='hostname', font=('bold', 12))
    # hostname_label.grid(row=0, column=0, sticky=E)
    # hostname_entry = Entry(frame_fields, textvariable=hostname_text)
    # hostname_entry.grid(row=0, column=1, sticky=W)
    # # BRAND
    # brand_text = StringVar()
    # brand_label = Label(frame_fields, text='Brand', font=('bold', 12))
    # brand_label.grid(row=0, column=2, sticky=E)
    # brand_entry = Entry(frame_fields, textvariable=brand_text)
    # brand_entry.grid(row=0, column=3, sticky=W)
    # # RAM
    # ram_text = StringVar()
    # ram_label = Label(frame_fields, text='RAM', font=('bold', 12))
    # ram_label.grid(row=1, column=0, sticky=E)
    # ram_entry = Entry(frame_fields, textvariable=ram_text)
    # ram_entry.grid(row=1, column=1, sticky=W)
    # # FLASH
    # flash_text = StringVar()
    # flash_label = Label(frame_fields, text='Flash', font=('bold', 12), pady=20)
    # flash_label.grid(row=1, column=2, sticky=E)
    # flash_entry = Entry(frame_fields, textvariable=flash_text)
    # flash_entry.grid(row=1, column=3, sticky=W)
    #
    # frame_router = Frame(app)
    # frame_router.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
    #
    # columns = ['id', 'Player1', 'Player2', 'Winner']
    # router_tree_view = Treeview(frame_router, columns=columns, show="headings")
    # router_tree_view.column("id", width=30)
    # for col in columns[1:]:
    #     router_tree_view.column(col, width=120)
    #     router_tree_view.heading(col, text=col)
    # router_tree_view.bind('<<TreeviewSelect>>', None)
    # router_tree_view.pack(side="left", fill="y")
    # scrollbar = Scrollbar(frame_router, orient='vertical')
    # scrollbar.configure(command=router_tree_view.yview)
    # scrollbar.pack(side="right", fill="y")
    # router_tree_view.config(yscrollcommand=scrollbar.set)
    #
    # frame_btns = Frame(app)
    # frame_btns.grid(row=3, column=0)
    #
    # add_btn = Button(frame_btns, text='Add Router', width=12, command=None)
    # add_btn.grid(row=0, column=0, pady=20)
    #
    # remove_btn = Button(frame_btns, text='Remove Router',
    #                     width=12, command=None)
    # remove_btn.grid(row=0, column=1)
    #
    # update_btn = Button(frame_btns, text='Update Router',
    #                     width=12, command=None)
    # update_btn.grid(row=0, column=2)
    #
    # clear_btn = Button(frame_btns, text='Clear Input',
    #                    width=12, command=None)
    # clear_btn.grid(row=0, column=3)
    #
    # search_btn = Button(frame_search, text='Search',
    #                     width=12, command=None)
    # search_btn.grid(row=0, column=2)
    #
    # search_query_btn = Button(frame_search, text='Search Query',
    #                           width=12, command=None)
    # search_query_btn.grid(row=1, column=2)
    #
    # app.title('Connect4 AI (Database)')
    # app.geometry('700x550')
    #
    # # Start program
    # app.mainloop()


def drawBoard():
    screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE,
                             (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE * 2, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                               int(r * SQUARE_SIZE + SQUARE_SIZE * 3 - SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def drawPiece(column, row, color):
    pygame.draw.circle(screen, color, (int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
                                       int(row * SQUARE_SIZE + SQUARE_SIZE * 3 - SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def drawHoveringPiece(x, color):
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE + SQUARE_SIZE))
    pygame.draw.circle(screen, color, (x, int(SQUARE_SIZE / 2 + SQUARE_SIZE)), RADIUS)
    pygame.display.update()


def runGames():
    print("Starting Game(s)")
    if gameCount >= 1:
        p1 = getPlayer1()
        p2 = getPlayer2()
        if p1 is None or p2 is None:
            return
        games = []
        for n in range(gameCount):
            g = game.Game(p1, p2)
            g.playGame()
            games.append(g)
        for g in games:
            database.insertGame(g)


def getPlayer1():
    p1 = None
    if p1Selection == 1 or p1Selection == 2:
        p1 = game.Game.getPlayer(p1Selection)
    if p1Selection == 3 or p1Selection == 4:
        if p1Depth >= 1:
            p1 = game.Game.getPlayer(p1Selection, p1Depth, p1Heuristic)
    elif p1Selection == 5:
        if p1TestGamesMC >= 1:
            p1 = game.Game.getPlayer(p1Selection, p1TestGamesMC)
    return p1


def getPlayer2():
    p2 = None
    if p2Selection == 1 or p2Selection == 2:
        p2 = game.Game.getPlayer(p2Selection)
    if p2Selection == 3 or p2Selection == 4:
        if p2Depth >= 1:
            p2 = game.Game.getPlayer(p2Selection, p2Depth, p2Heuristic)
    elif p2Selection == 5:
        if p2TestGamesMC >= 1:
            p2 = game.Game.getPlayer(p2Selection, p2TestGamesMC)
    return p2


def printResults(games, n):
    totalTimeP1, totalTimeP2, totalMovesConsideredP1, totalMovesConsideredP2 = 0, 0, 0, 0
    p1 = games[0].player1.label
    p2 = games[0].player2.label
    finalResults = {'P1: ' + p1: 0, 'P2: ' + p2: 0, 'Draw': 0}
    for game in games:
        if len(games) == 1:
            game_number = " "
        else:
            game_number = " " + str(games.index(game) + 1) + " "
        print("\nGAME" + game_number + "RESULTS (" + p1 + " vs. " + p2 + ")\n")
        if p1 == "Minimax" or p1 == "Alpha-Beta":
            print(p1 + " depth (P1): " + str(game.player1.max_depth))
        if p2 == "Minimax" or p2 == "Alpha-Beta":
            print(p2 + " depth (P2): " + str(game.player2.max_depth))
        if p1 == "Monte Carlo":
            print("Random games played per possible move (Monte Carlo, P1): " + str(game.player1.test_total))
        if p2 == "Monte Carlo":
            print("Random games played per possible move (Monte Carlo, P2): " + str(game.player2.test_total))
        print("Results: " + str(game.results))
        print("\nPlayer 1 (" + p1 + ")")
        print("Total moves considered: " + "{:,}".format(game.moves_considered_p1))
        print("Average moves considered per game: " + "{:,}".format(game.moves_considered_p1 / n))
        print("Time spent considering moves: " + str(round(game.time_elapsed_p1, 2)) + " seconds")
        print("Average time spent per game: " + str(round(game.time_elapsed_p1 / n, 2)) + " seconds")
        print("\nPlayer 2 (" + p2 + ")")
        print("Total moves considered: " + "{:,}".format(game.moves_considered_p2))
        print("Average moves considered per game: " + "{:,}".format(game.moves_considered_p2 / n))
        print("Time spent considering moves: " + str(round(game.time_elapsed_p2, 2)) + " seconds")
        print("Average time spent per game: " + str(round(game.time_elapsed_p2 / n, 2)) + " seconds")

        totalTimeP1 += game.time_elapsed_p1
        totalTimeP2 += game.time_elapsed_p2
        totalMovesConsideredP1 += game.moves_considered_p1
        totalMovesConsideredP2 += game.moves_considered_p2
        finalResults = {'P1: ' + p1: finalResults.get('P1: ' + p1) + game.results.get('P1: ' + p1),
                        'P2: ' + p2: finalResults.get('P2: ' + p2) + game.results.get('P2: ' + p2),
                        'Draw': finalResults.get('Draw') + game.results.get('Draw')}

    print(p1 + " vs. " + p2 + " (" + str(n) + " games)")
    print("OVERALL RESULTS: " + str(finalResults))
    print("Moves made P1: " + str(game.moves_made_p1))
    print("Moves made P2: " + str(game.moves_made_p2))


if __name__ == '__main__':
    database = Database()
    database.selectAllGames()
    showMainMenu()
