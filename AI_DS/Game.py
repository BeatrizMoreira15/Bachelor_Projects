import pygame as pg

from Board import Board
from ComputerPlayer import ComputerPlayer
from HumanPlayer import HumanPlayer
from settings import *


class Game:
    def __init__(self, screen):
        # screen
        self.screen = screen

        # get boards
        self.board_list = self.define_boards()

        # get user settings
        self.game_mode = self.get_game_mode()
        self.difficulty = self.get_difficulty()
        self.board = Board(self.choose_board())

        # define draw variables
        self.ROWS = None
        self.SQUARE_SIZE = None
        self.HALF_SQUARE_SIZE = None
        self.LINE_SIZE = None
        self.LINE_COLOR = None
        self.RADIUS = None
        self.CIRCLE_COLOR1_PLAYER1 = None
        self.CIRCLE_COLOR2_PLAYER1 = None
        self.CIRCLE_COLOR1_PLAYER2 = None
        self.CIRCLE_COLOR2_PLAYER2 = None
        self.CIRCLE_CAPTURE_MOVE_COLOR = None
        self.CIRCLE_POSSIBLE_MOVE_COLOR = None
        self.CIRCLE_SELECTED_PIECE_COLOR = None
        self.CIRCLE_OUTER_LINE = None
        self.CIRCLE_POSSIBLE_MOVE_RADIUS = None
        self.CENTER_X = None
        self.CENTER_Y = None
        self.font1 = None
        self.font2 = None
        self.font3 =None

        self.define_draw_variables()

        # get players
        self.players = []
        self.turn = 1
        self.define_players()

    @staticmethod
    def define_boards():
        board_3x3 = [[1, 1, 2],
                     [1, 0, 2],
                     [1, 2, 2]
                     ]

        board_5x5 = [[1, 1, 2, 2, 2],
                     [1, 1, 2, 2, 2],
                     [1, 1, 0, 2, 2],
                     [1, 1, 1, 2, 2],
                     [1, 1, 1, 2, 2]
                     ]

        board_7x7 = [[1, 1, 1, 2, 2, 2, 2],
                     [1, 1, 1, 2, 2, 2, 2],
                     [1, 1, 1, 2, 2, 2, 2],
                     [1, 1, 1, 0, 2, 2, 2],
                     [1, 1, 1, 1, 2, 2, 2],
                     [1, 1, 1, 1, 2, 2, 2],
                     [1, 1, 1, 1, 2, 2, 2]]

        return [board_3x3, board_5x5, board_7x7]

    @staticmethod
    def get_game_mode():
        """
        asks the user for the prefered game mode

        :return: game mode -> int
        """
        print("Escolher modo de jogo")
        print("1 - Humano/Humano  2 - Humano/Computador  3 - Computador/Computador ")

        user_input = int(input())

        while not (user_input in (1, 2, 3)):
            print("Escolher modo de jogo")
            print("1 - Humano/Humano  2 - Humano/Computador  3 - Computador/Computador ")

            user_input = int(input())

        return user_input

    def get_difficulty(self):
        """
        asks the user for the prefered difficulty
        :return: difficulty -> int | list[int]
        """
        if self.game_mode == 1:
            return None

        elif self.game_mode == 2:
            print("Escolha a dificuldade de jogo: \n1-Fácil 2-Médio 3-Difícil")
            return int(input())

        elif self.game_mode == 3:
            print("Escolha a dificuldade de jogador 1: \n1-Fácil 2-Médio 3-Difícil")
            difficulty1 = int(input())
            print("Escolha a dificuldade de jogador 2: \n1-Fácil 2-Médio 3-Difícil")
            difficulty2 = int(input())
            return difficulty1, difficulty2

    def choose_board(self):
        """
        asks the user for the prefered board_size and returns the board_index
        :return: board -> list[list[int]]
        """
        print("Escolher tabuleiro")
        print("1- 3x3    2-  5x5    3- 7x7")

        user_input = int(input()) - 1

        while not (user_input in (0, 1, 2)):
            print("Escolher tabuleiro")
            print("1- 3x3    2-  5x5    3- 7x7")

            user_input = int(input()) - 1

        return self.board_list[user_input]

    def define_draw_variables(self):
        self.ROWS = len(self.board)

        # calculate square size
        self.SQUARE_SIZE = WIDTH // self.ROWS
        self.HALF_SQUARE_SIZE = self.SQUARE_SIZE // 2

        # lines variables
        self.LINE_SIZE = 3
        self.LINE_COLOR = BLACK

        # circle variables
        self.RADIUS = self.SQUARE_SIZE // 3

        self.CIRCLE_COLOR1_PLAYER1 = BLACK
        self.CIRCLE_COLOR2_PLAYER1 = BLACK

        self.CIRCLE_COLOR1_PLAYER2 = CREME
        self.CIRCLE_COLOR2_PLAYER2 = BLACK

        self.CIRCLE_CAPTURE_MOVE_COLOR = SALMON
        self.CIRCLE_POSSIBLE_MOVE_COLOR = BLUE

        self.CIRCLE_SELECTED_PIECE_COLOR = BLUE

        self.CIRCLE_OUTER_LINE = 3
        self.CIRCLE_POSSIBLE_MOVE_RADIUS = self.RADIUS // 3

        self.CENTER_X = WIDTH // 2
        self.CENTER_Y = HEIGHT // 2

        # font variables
        pg.font.init()
        self.font1 = pg.font.SysFont("Arial", 22)
        self.font2 = pg.font.SysFont("Arial", 42)
        self.font3 = pg.font.SysFont("Arial", 70)

    def draw_label(self):

        text_creme = self.font1.render("No: " + str(self.board.count_pieces()[1]), True, CREME, BLACK)
        textRect_creme = text_creme.get_rect(topleft=(0, 0))

        text_black = self.font1.render("No : " + str(self.board.count_pieces()[2]), True, BLACK, CREME)
        textRect_black = text_black.get_rect(bottomright=(WIDTH,HEIGHT))

        self.screen.blit(text_creme, textRect_creme)
        self.screen.blit(text_black, textRect_black)

    def check_win(self):
        if self.board.count_pieces()[1] == 0:
            return True
        elif self.board.count_pieces()[2] == 0:
            return True
        return False

    def draw_victory(self):
        if self.check_win():
            winner = 1 if self.turn == 2 else 2

            text = self.font3.render("The winner is player " + str(winner), True, CREME, BLACK)

            text_rect = text.get_rect(center=(self.CENTER_X, self.CENTER_Y))

            self.screen.blit(text, text_rect)

    def define_players(self):
        # Human vs Human
        if self.game_mode == 1:
            self.players.append(HumanPlayer(1, self.board, self.SQUARE_SIZE))
            self.players.append(HumanPlayer(2, self.board, self.SQUARE_SIZE))

        # Human vs Computer
        elif self.game_mode == 2:
            self.players.append(HumanPlayer(1, self.board, self.SQUARE_SIZE))
            self.players.append(ComputerPlayer(2, self.board, self.difficulty))

        # Computer vs Computer
        else:
            print(self.difficulty)
            self.players.append(ComputerPlayer(1, self.board, self.difficulty[0]))
            self.players.append(ComputerPlayer(2, self.board, self.difficulty[1]))

    def draw_board(self):
        """
        draws the lines in the given Surface
        :return:
        """

        for i in range(self.ROWS):
            # horizontal lines
            p1 = (self.HALF_SQUARE_SIZE, i * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE)
            p2 = (WIDTH - self.HALF_SQUARE_SIZE, i * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE)

            pg.draw.line(self.screen, self.LINE_COLOR, p1, p2, self.LINE_SIZE)

            # vertical lines
            p1 = (i * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE, self.HALF_SQUARE_SIZE)
            p2 = (i * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE, HEIGHT - self.HALF_SQUARE_SIZE)

            pg.draw.line(self.screen, self.LINE_COLOR, p1, p2, self.LINE_SIZE)

            # diagonals lines
            for j in range(self.ROWS):
                # draws only in alternating squares
                if (i + j) % 2 == 0:
                    # diagonals going bottom right direction
                    if i < self.ROWS - 1 and j < self.ROWS - 1:
                        p1 = (
                            i * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE, j * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE)
                        p2 = ((i + 1) * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE,
                              (j + 1) * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE)

                        pg.draw.line(self.screen, self.LINE_COLOR, p1, p2, self.LINE_SIZE)

                    # diagonals going bottom left direction
                    if i > 0 and j < self.ROWS - 1:
                        p1 = (
                            i * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE, j * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE)
                        p2 = ((i - 1) * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE,
                              (j + 1) * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE)

                        pg.draw.line(self.screen, self.LINE_COLOR, p1, p2, self.LINE_SIZE)

    def draw_pieces(self, selected_piece):
        """
        draws the pieces of the current game state in the given Surface
        :return:
        """
        for i in range(self.ROWS):
            for j in range(self.ROWS):
                # calculate point
                x = i * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE
                y = j * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE

                # player one circles
                if self.board[i][j] == 1:
                    pg.draw.circle(self.screen, self.CIRCLE_COLOR1_PLAYER1, (x, y), self.RADIUS)
                    pg.draw.circle(self.screen, self.CIRCLE_COLOR2_PLAYER1, (x, y), self.RADIUS,
                                   width=self.CIRCLE_OUTER_LINE)

                # player two circles
                elif self.board[i][j] == 2:
                    pg.draw.circle(self.screen, self.CIRCLE_COLOR1_PLAYER2, (x, y), self.RADIUS)
                    pg.draw.circle(self.screen, self.CIRCLE_COLOR2_PLAYER2, (x, y), self.RADIUS,
                                   width=self.CIRCLE_OUTER_LINE)

        # draw circle in the selected piece
        if selected_piece is not None:
            x = selected_piece[0] * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE
            y = selected_piece[1] * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE

            pg.draw.circle(self.screen, self.CIRCLE_SELECTED_PIECE_COLOR, (x, y), self.RADIUS,
                           width=self.CIRCLE_OUTER_LINE)

    def draw_possible_moves(self, valid_moves):
        """
        draws the possibles moves on the given Surface
        :return:
        """
        if valid_moves:
            for x, y, capture_move in valid_moves:
                p = (x * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE, y * self.SQUARE_SIZE + self.HALF_SQUARE_SIZE)

                if capture_move:
                    pg.draw.circle(self.screen, self.CIRCLE_CAPTURE_MOVE_COLOR, p, self.CIRCLE_POSSIBLE_MOVE_RADIUS)
                else:
                    pg.draw.circle(self.screen, self.CIRCLE_POSSIBLE_MOVE_COLOR, p, self.CIRCLE_POSSIBLE_MOVE_RADIUS)

    def draw_game(self):
        self.draw_board()
        self.draw_pieces(self.players[self.turn - 1].selected_piece)
        self.draw_possible_moves(self.players[self.turn - 1].valid_moves)
        self.draw_label()
        self.draw_victory()

    def run(self):
        self.draw_game()

        # player input and change turns
        if self.players[self.turn - 1].input():
            self.turn = 2 if self.turn == 1 else 1
