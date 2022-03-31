import pygame
import pygame_menu
import game

from database import Database
from tkinter import *
from tkinter.ttk import Treeview

# Initialize pygame
pygame.init()

# Static variables for pygame

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

# Game configuration variables

p1Selection = 1
p2Selection = 2
gameCount = 0
p1Depth, p2Depth, p1TestGamesMC, p2TestGamesMC = 0, 0, 0, 0
p1Heuristic, p2Heuristic = 1, 1

# Root Tkinter view
root = None

# Pygame menu
menu = None

# Reference to Database class instance
database = None

# Search parameters

p1Search, p2Search, p1DepthSearch, p2DepthSearch = None, None, None, None
p1HeuristicSearch, p2HeuristicSearch, p1TestGamesMCSearch, p2TestGamesMCSearch = None, None, None, None
p1DepthEquality, p2DepthEquality, p1MCEquality, p2MCEquality = None, None, None, None

# Data selection value
dataSelection = None

# TreeViews
game_view, matchup_view = None, None

# Items to show in TreeView
items = []

# Scrolling
scrolling = False

# Searching
searching = False


def showMainMenu():
    """Displays the main menu for the application."""
    menu = pygame_menu.Menu('Connect4 AI', screen.get_width(), screen.get_height(),
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Run Game(s)', showConfigureGameMenu, font_size=MAIN_MENU_FONT_SIZE)
    menu.add.button('Data', showDataWindow, font_size=MAIN_MENU_FONT_SIZE)
    menu.add.button('Quit', pygame_menu.events.EXIT, font_size=MAIN_MENU_FONT_SIZE)
    menu.mainloop(screen)


def showConfigureGameMenu():
    """Displays the menu for the user to configure the game(s) they want to run."""
    menu = pygame_menu.Menu('Connect4 AI', width, height,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Back', showMainMenu, font_size=30, padding=20)

    def updateGameCount(input):
        global gameCount
        gameCount = int(input) if input.isnumeric() else 0

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
    """Displays Tkinter window with a UI for viewing and searching the game_data database."""
    global root
    root = Tk()
    createSearchWidgets()
    createButtons()

    getAllItems()
    createTreeView()

    root.title('Connect4 AI (Database)')
    root.geometry('1300x550')

    # Start program
    root.mainloop()


def createSearchWidgets():
    """Creates UI widgets (entry boxes, option menus) related to searching."""
    labels = ['Player 1', 'Player 2', 'Depth (P1)', 'Depth (P2)', 'Heuristic (P1)', 'Heuristic (P2)',
              'Monte Carlo Test Games (P1)', 'Monte Carlo Test Games (P2)']
    equalities = ['=', '>', '>=', '<', '<=']
    row, column = 0, 0

    # Initializing global search variables
    global p1Search, p2Search, p1DepthSearch, p2DepthSearch, p1DepthEquality, p2DepthEquality, p1MCEquality, \
        p2MCEquality, p1HeuristicSearch, p2HeuristicSearch, p1TestGamesMCSearch, p2TestGamesMCSearch
    p1Search, p2Search, p1HeuristicSearch, p2HeuristicSearch = StringVar(), StringVar(), StringVar(), StringVar()
    p1DepthSearch, p2DepthSearch, p1TestGamesMCSearch, p2TestGamesMCSearch = StringVar(), StringVar(), StringVar(), StringVar()
    p1DepthEquality, p2DepthEquality, p1MCEquality, p2MCEquality = StringVar(), StringVar(), StringVar(), StringVar()

    p1HeuristicSearch.set('N/A')
    p2HeuristicSearch.set('N/A')
    p1DepthEquality.set('=')
    p2DepthEquality.set('=')
    p1MCEquality.set('=')
    p2MCEquality.set('=')

    for label in labels:
        i = labels.index(label)
        if (i + 1) % 2 != 0:
            column = 0
        else:
            column = 1
        f = Frame(root)
        f.grid(row=row, column=column)

        l = Label(f, text=label, font=('bold', 10), pady=20, padx=10)
        l.grid(row=row, column=column, sticky=W)

        if 'Player' in label:
            choices = ['Manual', 'Random', 'Minimax', 'Alpha-Beta', 'Monte Carlo']
            if '1' in label:
                menu = OptionMenu(f, p1Search, *choices)
            else:
                menu = OptionMenu(f, p2Search, *choices)
            menu.grid(row=row, column=column, padx=(75, 0))
        elif 'Depth' in label:
            if 'P1' in label:
                search_entry = Entry(f, textvariable=p1DepthSearch)
                menu = OptionMenu(f, p1DepthEquality, *equalities)
            else:
                search_entry = Entry(f, textvariable=p2DepthSearch)
                menu = OptionMenu(f, p2DepthEquality, *equalities)
            menu.grid(row=row, column=column, padx=(90, 10))
            search_entry.grid(row=row, column=column + 1)
        elif 'Heuristic' in label:
            choices = ['N/A', 'Adjacent Pieces', 'Piece Locations', 'Connected Pieces']
            if 'P1' in label:
                menu = OptionMenu(f, p1HeuristicSearch, *choices)
            else:
                menu = OptionMenu(f, p2HeuristicSearch, *choices)
            menu.grid(row=row, column=column, padx=(100, 0))
        elif 'Monte Carlo' in label:
            if 'P1' in label:
                menu = OptionMenu(f, p1MCEquality, *equalities)
                search_entry = Entry(f, textvariable=p1TestGamesMCSearch)
            else:
                menu = OptionMenu(f, p2MCEquality, *equalities)
                search_entry = Entry(f, textvariable=p2TestGamesMCSearch)
            menu.grid(row=row, column=column, padx=(190, 10))
            search_entry.grid(row=row, column=column + 1)
        if column == 1:
            row += 1


def createButtons():
    """Creates UI buttons for searching, clearing searches, and selecting the table of the database to view."""
    frame_buttons = Frame(root)
    frame_buttons.grid(row=3, column=2)

    def search():
        global searching
        searching = True
        displayItems()

    search_button = Button(frame_buttons, text='Search',
                           width=12, command=search)
    search_button.grid(row=0, column=0)

    def clearSearch():
        global searching
        searching = False
        displayItems()

    clear_search_button = Button(frame_buttons, text='Clear Search', width=12, command=clearSearch)
    clear_search_button.grid(row=1, column=0)

    global dataSelection
    dataSelection = IntVar()

    def changeData():
        if not searching:
            getAllItems()
            createTreeView()

    radio_button_1 = Radiobutton(frame_buttons, text='Show All Games', variable=dataSelection, value=1,
                                 command=changeData)
    radio_button_2 = Radiobutton(frame_buttons, text='Show Matchups', variable=dataSelection, value=2,
                                 command=changeData)

    radio_button_1.grid(row=0, column=1)
    radio_button_2.grid(row=1, column=1)
    radio_button_1.select()


def createTreeView():
    """Establishes a TreeView for the display of database items."""
    # Gets column headers
    columns = getTreeViewColumns()

    frame_data = Frame(root)
    frame_data.grid(row=4, column=0, columnspan=len(columns), rowspan=1, pady=20, padx=20)

    tree_view = Treeview(frame_data, columns=columns, show="headings")
    tree_view.column("id", width=30)

    for col in columns[1:]:
        tree_view.column(col, width=80, minwidth=125, stretch=True)
        tree_view.heading(col, text=col)

    tree_view.bind('<<TreeviewSelect>>', None)
    tree_view.pack(side="left", fill="y")
    createScrollbars(tree_view, frame_data)

    index = 0
    for item in items:
        values_list = []
        id = item[0]
        # If item already displayed, skip insertion
        if tree_view.exists(id):
            continue
        game_count = item[2]
        for value in item:
            # If this value is a total, calculate average
            if 'Avg.' in columns[index]:
                avg_value = round(value / game_count, 2)
                values_list.append(avg_value)
            else:
                values_list.append(value)
            index += 1

        values = tuple(values_list)
        tree_view.insert(parent='', iid=id, index='end', values=values)
        index = 0

    selection = dataSelection.get() if dataSelection is not None else 1
    global game_view, matchup_view
    # Destroy matchup view when switching to games
    if selection == 1:
        game_view = tree_view
        if matchup_view is not None:
            try:
                matchup_view.destroy()
            except:
                print("Matchup View already destroyed")
    # Destroy games view when switching to matchups
    else:
        matchup_view = tree_view
        try:
            game_view.destroy()
        except:
            print("Game View already destroyed")


def getTreeViewColumns():
    """
    Returns a list of column headers to use in the TreeView.
    :return: a list of column headers
    """
    global items, dataSelection
    selection = dataSelection.get() if dataSelection is not None else 1
    # 1 = Show All Games
    if selection == 1:
        columns = ['id', 'Player 1', 'Player 2', 'Winner', 'Time Elapsed (P1)', 'Moves Considered (P1)',
                   'Moves Made (P1)', 'Depth (P1)', 'Heuristic (P1)', 'MC Test Games (P1)', 'Time Elapsed (P2)',
                   'Moves Considered (P2)', 'Moves Made (P2)', 'Depth (P2)', 'Heuristic (P2)', 'MC Test Games (P2)']
        return columns
    # 2 = Show All Matchups
    elif selection == 2:
        columns = ['id', 'Matchup', 'Games', 'Wins (P1)', 'Wins (P2)', 'Avg. Time Elapsed (P1)',
                   'Avg. Moves Considered (P1)', 'Avg. Moves Made (P1)', 'Depth (P1)', 'Heuristic (P1)',
                   'MC Test Games (P1)', 'Avg. Time Elapsed (P2)', 'Avg. Moves Considered (P2)', 'Avg. Moves Made (P2)',
                   'Depth (P2)', 'Heuristic (P2)', 'MC Test Games (P2)']
        return columns


def displayItems():
    """Retrieves items to display and creates a TreeView filled with said items."""
    getAllItems()
    createTreeView()


def getAllItems():
    """Sets the items to display in the TreeView based on the user's selected table and whether or not the user is
    currently using the 'search' functionality."""
    global items
    selection = dataSelection.get() if dataSelection is not None else 1
    if searching:
        items = getItemsBySearch()
    else:
        items = database.selectAll('games') if selection == 1 else database.selectAll('matchups')


def getItemsBySearch():
    """
    Retrieves a collection of items based on the user's search parameters.
    :return: a list of items that satisfy the user's search parameters
    """
    selection = dataSelection.get()
    equalities = (p1DepthEquality.get(), p1MCEquality.get(), p2DepthEquality.get(), p2MCEquality.get())
    items = []

    if p1Search.get() != 'Monte Carlo':
        p1TestGamesMCSearch.set('N/A')
    if p2Search.get() != 'Monte Carlo':
        p2TestGamesMCSearch.set('N/A')
    if p1Search.get() != 'Minimax' and p1Search.get() != 'Alpha-Beta':
        p1DepthSearch.set('N/A')
        p1HeuristicSearch.set('N/A')
    if p2Search.get() != 'Minimax' and p2Search.get() != 'Alpha-Beta':
        p2DepthSearch.set('N/A')
        p2HeuristicSearch.set('N/A')

    # Searching all games
    if selection == 1:
        values = (
        p1Search.get(), p2Search.get(), p1DepthSearch.get(), p1HeuristicSearch.get(), p1TestGamesMCSearch.get(),
        p2DepthSearch.get(), p2HeuristicSearch.get(), p2TestGamesMCSearch.get())
        items = database.selectGames(values, equalities)
    # Searching matchups
    elif selection == 2:
        matchup = p1Search.get() + ' vs. ' + p2Search.get()
        values = (matchup, p1DepthSearch.get(), p1HeuristicSearch.get(), p1TestGamesMCSearch.get(),
                  p2DepthSearch.get(), p2HeuristicSearch.get(), p2TestGamesMCSearch.get())
        items = database.selectMatchup(values, equalities)
    return items


def createScrollbars(connected_widget, frame):
    """
    Creates vertical and horizontal scrollbars that are located in the given frame and attached to the given widget.
    :param connected_widget: The widget to pair with the scrollbars
    :param frame: The frame to house the scrollbars
    :return:
    """
    v_scroll = Scrollbar(frame, orient='vertical')
    v_scroll.configure(command=connected_widget.yview)
    v_scroll.pack(side="right", fill="y")
    h_scroll = Scrollbar(root, orient='horizontal', repeatdelay=0)
    h_scroll.configure(command=connected_widget.xview)
    h_scroll.grid(row=5, column=1)
    connected_widget.config(xscrollcommand=h_scroll.set)
    connected_widget.config(yscrollcommand=v_scroll.set)

    def scroll(arrow, *args):
        if arrow == "arrow1":
            connected_widget.tk.call(connected_widget._w, 'xview', 'scroll', -20, 'units')
        if arrow == "arrow2":
            connected_widget.tk.call(connected_widget._w, 'xview', 'scroll', 20, 'units')

    def start_scrolling(event):
        scroll(h_scroll.identify(event.x, event.y))

    h_scroll.bind("<Button-1>", start_scrolling)
    h_scroll.bind('<ButtonRelease-1>', start_scrolling)


def drawBoard():
    """Draws an empty Connect4 board on the screen."""
    screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE,
                             (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE * 2, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                               int(r * SQUARE_SIZE + SQUARE_SIZE * 3 - SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def drawPiece(column, row, color):
    """
    Draws a piece of the given color into the given column-row location of the board.
    :param column: The piece's column
    :param row: The piece's row
    :param color: The piece's color
    :return:
    """
    pygame.draw.circle(screen, color, (int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
                                       int(row * SQUARE_SIZE + SQUARE_SIZE * 3 - SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def drawHoveringPiece(x, color):
    """
    Draws a hovering Connect4 piece of the given color at the given 'x' of the x-axis.
    :param x: The x-coordinate of the piece to draw
    :param color: The color of the piece to draw
    :return:
    """
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE + SQUARE_SIZE))
    pygame.draw.circle(screen, color, (x, int(SQUARE_SIZE / 2 + SQUARE_SIZE)), RADIUS)
    pygame.display.update()


def runGames():
    """Runs a number of games based on user's input using user's selected configuration."""
    print("Running " + str(gameCount) + " games.")
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
        database.insertMatchup(games)


def getPlayer1():
    """Retrieves Player 1 using user's selection."""
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
    """Retrieves Player 2 using user's selection."""
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


if __name__ == '__main__':
    database = Database()
    database.createGamesTable()
    database.createMatchupsTable()
    showMainMenu()
