import math
from random import randint

from Player import Player
from settings import *


class ComputerPlayer(Player):
    def __init__(self, turn, board, difficulty):
        super().__init__(turn, board)

        self.difficulty = difficulty

        self.opponet_turn = 2 if self.turn == 1 else 1

        self.counter = 0
        self.counter_limit = 1 * TICTAC

        self.depth = 2 if difficulty == 2 else 5

        self.move =[]
        self.evaluation = None


    def minimax(self, board, move, depth, maximazingPlayer, alpha, beta):
        if depth == 0 or board.isEndState():
            return move, self.evaluate(board) * 10 ** (depth + 1) # reward less moves

        # MAX
        if maximazingPlayer:

            best_value = -math.inf
            possible_plays = board.possible_plays(self.turn)
            best_move = [None, None, None, None]
            for move in possible_plays:
                board_test = board.copy()

                # executs the standart moviment in a test phase
                selected_piece = (move[0], move[1])
                jump = (move[2], move[3])
                board_test.capture_piece(jump, selected_piece)

                # value is the difference between the number of pieces of the Human Player and the Computer Player and the addition of the minimax recursion
                # the addition of the evaluate is done in order to prioritize the plays with a higher piece count
                value = self.evaluate(board_test) + self.minimax(board_test, move, depth - 1, False, alpha, beta)[1]

                #if the value is higher than the best value, the value is the new best value and the move is the new best move
                if value > best_value:
                    best_value = value
                    best_move = move

                # alpha = max between alpha and its higher value
                alpha = max(alpha, best_value)
                if beta <= alpha:  # if beta <= alpha, the cycles breaksS
                    break

            return best_move, best_value

        # MIN
        else:

            best_value = math.inf
            possible_plays = board.possible_plays(self.opponet_turn)
            best_move = [None, None, None, None]
            for move in possible_plays:
                board_test = board.copy()

                # executs the standart moviment in a test phase
                selected_piece = (move[0], move[1])
                jump = (move[2], move[3])
                board_test.capture_piece(jump, selected_piece)

                # value is the difference between the number of pieces of the Human Player and the Computer Player and the addition of the minimax recursion
                # the addition of the evaluate is done in order to prioritize the plays with a higher piece count
                value = self.evaluate(board_test) + self.minimax(board_test, move, depth - 1, True, alpha, beta)[1]
                
                #if the best value is lower than the value, the new best value is the value and the move is the new best move
                if value < best_value:
                    best_value = value
                    best_move = move

                #if beta = min between the alpha and the best value
                beta = min(alpha, best_value)
                if beta <= alpha:  #if beta <= alpha, the cycle breaks
                    break

            return best_move, best_value



    def random_piece(self):
        # get pieces pos
        pieces = []
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y] == self.turn:
                    pieces.append((x, y))

        if len(pieces) > 0:

            # choose a piece at random
            choosen_piece_index = randint(0, len(pieces) - 1)
            self.selected_piece = pieces[choosen_piece_index]
            self.get_valid_moves()

            # if the piece has no possible moves choose another one
            while len(self.valid_moves) == 0:
                choosen_piece_index = randint(0, len(pieces) - 1)
                self.selected_piece = pieces[choosen_piece_index]
                self.get_valid_moves()

    def random_move(self):
        choosen_move_index = randint(0, len(self.valid_moves) - 1)
        move = self.valid_moves[choosen_move_index]
        jump = (move[0], move[1])

        self.board.capture_piece(jump, self.selected_piece)

    def print_evaluation(self):
        if self.difficulty == 1:
            super().print_evaluation()
        else:
            print(f"Player {self.turn} | Evaluation: {self.evaluation}")

    def input(self):
        # easy difficulty
        if self.difficulty == 1:
            self.counter += 1

            if not self.selected_piece:
                self.random_piece()
            elif self.counter >= self.counter_limit:
                self.counter = 0
                self.random_move()
                self.selected_piece = None
                self.valid_moves = []

                self.print_evaluation()
                return True

        # medium and hard difficulties
        else:
            self.counter += 1

            if not self.selected_piece:
                board_copy = self.board.copy()
                alpha = -math.inf
                beta = math.inf
                self.move, self.evaluation = self.minimax(board_copy,[],  self.depth, True, alpha, beta)

                if self.move:
                    self.selected_piece = (self.move[0], self.move[1])
                    self.get_valid_moves()

            elif self.counter == self.counter_limit:
                self.counter = 0

                jump = (self.move[2], self.move[3])
                self.board.capture_piece(jump, self.selected_piece)

                self.selected_piece = None
                self.valid_moves = []

                self.print_evaluation()
                return True

        return False