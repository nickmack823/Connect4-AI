import os
import sqlite3
from sqlite3 import Error

DATABASE_NAME = 'game_history.db'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(ROOT_DIR, 'database/' + DATABASE_NAME)


class Database:

    def __init__(self):
        # Connection to database file
        self.conn = self.createDatabaseConnection()

    def createDatabaseConnection(self):
        """Creates a connection to an SQLite database"""
        conn = None
        try:
            print(DATABASE_PATH)
            conn = sqlite3.connect(DATABASE_PATH)
            print(sqlite3.version)
        except Error as e:
            print("Error (createDatabaseConnection): " + str(e))
        return conn

    def createDatabaseTable(self, create_table_sql):
        """Creates a table from the createTableSQL statement
        :param conn: Connection object
        :param create_table_sql: A CREATE TABLE SQL statement
        :return:
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print("Error (createDatabaseTable): " + str(e))

    def createGamesTable(self):
        """Creates a table 'games' in the database for storing data relating to past completed games"""
        sql_create_games_table = """ CREATE TABLE IF NOT EXISTS games (
                                                    id integer PRIMARY KEY,
                                                    player1 text,
                                                    player2 text,
                                                    winner text,
                                                    p1_total_time_elapsed real,
                                                    p1_total_moves_considered integer,
                                                    p1_total_moves_made integer,
                                                    p1_depth integer,
                                                    p1_heuristic text,
                                                    p1_monte_carlo_test_games integer,
                                                    p2_total_time_elapsed real,
                                                    p2_total_moves_considered integer,
                                                    p2_total_moves_made integer,
                                                    p2_depth integer,
                                                    p2_heuristic text,
                                                    p2_monte_carlo_test_games integer
                                                ); """
        if self.conn is not None:
            self.createDatabaseTable(sql_create_games_table)
        else:
            print("Error: Cannot connect to database.")

    def insertGame(self, game):
        """Inserts a 'game' item into the 'games' table of the database"""
        print("INSERT GAME")
        sql_insertion_games = """ INSERT INTO games ( player1,
                                                player2,
                                                winner,
                                                p1_total_time_elapsed,
                                                p1_total_moves_considered,
                                                p1_total_moves_made,
                                                p1_depth,
                                                p1_heuristic,
                                                p1_monte_carlo_test_games,
                                                p2_total_time_elapsed,
                                                p2_total_moves_considered,
                                                p2_total_moves_made,
                                                p2_depth,
                                                p2_heuristic,
                                                p2_monte_carlo_test_games)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        gameWinner = [key for key, value in game.results.items() if value == 1][0]
        p1depth = game.player1.getDepth()
        p2depth = game.player2.getDepth()
        p1H = game.player1.getHeuristicName()
        p2H = game.player2.getHeuristicName()
        p1MC = game.player1.getMCTestTotal()
        p2MC = game.player2.getMCTestTotal()

        gameValues = (
            game.player1.label, game.player2.label, gameWinner, round(game.time_elapsed_p1, 2),
            game.moves_considered_p1,
            game.moves_made_p1, p1depth, p1H, p1MC, round(game.time_elapsed_p2, 2), game.moves_considered_p2,
            game.moves_made_p2, p2depth, p2H, p2MC)
        cursor = self.conn.cursor()
        cursor.execute(sql_insertion_games, gameValues)
        # Commit required to actually save the changes
        self.conn.commit()
        self.selectAllGames()

    def selectAllGames(self):
        print("SELECT")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM games")
        games = cursor.fetchall()
        print(games)
        for game in games:
            print(game)
