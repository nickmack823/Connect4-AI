import os
import sqlite3
from sqlite3 import Error

DATABASE_NAME = 'game_data.db'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(ROOT_DIR, 'database/' + DATABASE_NAME)


class Database:

    def __init__(self):
        # Connection to database file
        self.conn = self.createDatabaseConnection()

    def createDatabaseConnection(self):
        """
        Creates a connection to an SQLite database
        :return: the connection to the database if the connection was successful, else None
        """
        conn = None
        try:
            print(DATABASE_PATH)
            conn = sqlite3.connect(DATABASE_PATH)
            print(sqlite3.version)
        except Error as e:
            print("Error (createDatabaseConnection): " + str(e))
        return conn

    def createDatabaseTable(self, create_table_sql):
        """Creates a table from the given SQL statement.
        :param create_table_sql: a CREATE TABLE SQL statement
        :return:
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print("Error (createDatabaseTable): " + str(e))

    def createGamesTable(self):
        """Creates a table 'games' in the database for storing data relating to completed games."""
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

    def createMatchupsTable(self):
        """Creates a table 'matchups' in the database for storing data relating to game matchups."""
        sql_create_matchups_table = """ CREATE TABLE IF NOT EXISTS matchups (
                                                            id integer PRIMARY KEY,
                                                            matchup text,
                                                            games integer,
                                                            p1_victories integer,
                                                            p2_victories integer,
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
            self.createDatabaseTable(sql_create_matchups_table)
        else:
            print("Error: Cannot connect to database.")

    def insertGame(self, game):
        """
        Records a game's results into the database.
        :param game: the game to record
        :return:
        """
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

    def selectGames(self, values, equalities):
        """
        Returns the games that have the given values that satisfy the given equalities.
        :param values: a tuple of values to match
        :param equalities: a tuple of equalities to compare values with
        :return: the games that mee the criteria, or an empty list of no such games are found
        """
        print("SELECTING ALL FROM games WHERE game has values: " + str(values))
        cursor = self.conn.cursor()
        e = equalities
        sql_selection = 'SELECT * FROM games WHERE player1 = ? AND ' \
                        'player2 = ? AND p1_depth' + e[0] + '? AND p1_heuristic = ? AND ' \
                        'p1_monte_carlo_test_games' + e[1] + '? AND p2_depth' + e[2] + '? AND p2_heuristic = ? AND ' \
                        'p2_monte_carlo_test_games' + e[3] + '?'
        cursor.execute(sql_selection, values)
        games = cursor.fetchall()
        return games

    def insertMatchup(self, games):
        """
        Inserts the matchup data from the given list of games in the database.
        :param games: The games to record data from
        :return:
        """
        # Sample game to get persistent values from (names, depths, heuristics, Monte Carlo test games)
        game = games[0]
        p1 = game.player1.label
        p2 = game.player2.label
        matchup = p1 + " vs. " + p2

        n = len(games)
        wins = {'P1: ' + p1: 0, 'P2: ' + p2: 0, 'Draw': 0}
        p1_total_time, p2_total_time, p1_total_moves_considered, p2_total_moves_considered = 0, 0, 0, 0
        p1_total_moves, p2_total_moves = 0, 0

        for g in games:
            for k in g.results.keys():
                if k in wins.keys():
                    wins[k] += g.results[k]

            p1_total_time += g.time_elapsed_p1
            p2_total_time += g.time_elapsed_p2
            p1_total_moves_considered += g.moves_considered_p1
            p2_total_moves_considered += g.moves_considered_p2
            p1_total_moves += g.moves_made_p1
            p2_total_moves += g.moves_made_p2

        p1depth = game.player1.getDepth()
        p2depth = game.player2.getDepth()
        p1H = game.player1.getHeuristicName()
        p2H = game.player2.getHeuristicName()
        p1MC = game.player1.getMCTestTotal()
        p2MC = game.player2.getMCTestTotal()

        core_values = (matchup, p1depth, p1H, p1MC, p2depth, p2H, p2MC)

        existing_matchup = self.selectMatchup(core_values, ('=', '=', '=', '=',))
        matchup_values = (
            n, wins['P1: ' + p1], wins['P2: ' + p2], p1_total_time, p1_total_moves_considered,
            p1_total_moves, p2_total_time, p2_total_moves_considered,
            p2_total_moves, matchup, p1depth, p1H, p1MC, p2depth, p2H, p2MC)
        # If matchup already in matchups table, update it
        if len(existing_matchup) != 0:
            self.updateMatchup(matchup_values, existing_matchup)
        else:
            sql_insertion_matchup = """ INSERT INTO matchups (games,
                                                                    p1_victories,
                                                                    p2_victories,
                                                                    p1_total_time_elapsed,
                                                                    p1_total_moves_considered,
                                                                    p1_total_moves_made,
                                                                    p2_total_time_elapsed,
                                                                    p2_total_moves_considered,
                                                                    p2_total_moves_made,
                                                                    matchup,
                                                                    p1_depth,
                                                                    p1_heuristic,
                                                                    p1_monte_carlo_test_games,
                                                                    p2_depth,
                                                                    p2_heuristic,
                                                                    p2_monte_carlo_test_games
                                                                )
                                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            cursor = self.conn.cursor()
            cursor.execute(sql_insertion_matchup, matchup_values)
            self.conn.commit()

    def selectAll(self, table):
        """
        Selects every item from the given table.
        :param table: the table to select from
        :return: the results of the selection
        """
        print("SELECTING ALL FROM " + table)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + table)
        results = cursor.fetchall()
        return results

    def selectMatchup(self, values, equalities):
        """
        Returns the matchup that has the given values that satisfy the given equalities.
        :param values: a tuple of values to match
        :param equalities: a tuple of equalities to compare values with
        :return: the matchup that meets the criteria, or an empty list if no such matchup is found
        """
        print("SELECTING ALL FROM matchups WHERE matchup has values: " + str(values))
        cursor = self.conn.cursor()
        e = equalities
        sql_selection = 'SELECT * FROM matchups WHERE matchup = ? AND ' \
                        'p1_depth' + e[0] + '? AND p1_heuristic = ? AND p1_monte_carlo_test_games' + e[1] + '? AND ' \
                        'p2_depth' + e[2] + '? AND p2_heuristic = ? AND p2_monte_carlo_test_games' + e[3] + '?'
        cursor.execute(sql_selection, values)
        row = cursor.fetchall()
        return row

    def updateMatchup(self, values, existing_matchup):
        """
        Updates the given matchup with the given values.
        :param values: a tuple of values with which to update the matchup
        :param existing_matchup: the matchup to update
        :return:
        """
        print("UPDATING matchups with " + str(values))
        cursor = self.conn.cursor()
        sql_update = """UPDATE matchups 
                        SET games = ? ,
                            p1_victories = ? ,
                            p2_victories = ? ,
                            p1_total_time_elapsed = ? ,
                            p1_total_moves_considered = ? ,
                            p1_total_moves_made = ? ,
                            p2_total_time_elapsed = ? ,
                            p2_total_moves_considered = ? ,
                            p2_total_moves_made = ? 
                        WHERE matchup = ? AND
                            p1_depth = ? AND
                            p1_heuristic = ? AND
                            p1_monte_carlo_test_games = ? AND
                            p2_depth = ? AND
                            p2_heuristic = ? AND
                            p2_monte_carlo_test_games = ?
                        """
        # Values that are static for the matchup (matchup, depths, heuristics, MC test games)
        core_values = values[9:len(values)]

        # Calculating new values
        new_total = existing_matchup[0][2] + values[0]
        new_wins_p1 = values[1] + existing_matchup[0][3]
        new_wins_p2 = values[2] + existing_matchup[0][4]
        new_time_p1 = values[3] + existing_matchup[0][5]
        new_moves_considered_p1 = values[4] + existing_matchup[0][6]
        new_moves_made_p1 = values[5] + existing_matchup[0][7]
        new_time_p2 = values[6] + existing_matchup[0][11]
        new_moves_considered_p2 = values[7] + existing_matchup[0][12]
        new_moves_made_p2 = values[8] + existing_matchup[0][13]

        new_values = (new_total, new_wins_p1, new_wins_p2, round(new_time_p1, 2), new_moves_considered_p1,
                      new_moves_made_p1, round(new_time_p2, 2), new_moves_considered_p2, new_moves_made_p2)
        new_values = new_values + core_values

        cursor.execute(sql_update, new_values)
        self.conn.commit()
