import pygame as pg

from Player import Player


class HumanPlayer(Player):

    def __init__(self, turn, board, square_size):
        super().__init__(turn, board)
        self.SQUARE_SIZE = square_size
        self.pressing = False

    def just_pressed(self):
        """
        returns true if the player just pressed
        :return: boolean
        """
        # if the player WAS already pressing ...
        if self.pressing:
            # ... and STOPPED pressing reset var and returns false
            if not pg.mouse.get_pressed(3)[0]:
                self.pressing = False
                return False

        # if the player WASN'T pressing ...
        else:
            # ... and PRESSED toggle var and return true
            if pg.mouse.get_pressed(3)[0]:
                self.pressing = True
                return True

    def select_piece(self, mouse_pos):
        """
        selects the piece if it belongs to the player
        :param mouse_pos: tuple[int | it]
        :return: tuple[int | int]
        """
        grid_x, grid_y = self.get_selected_grid(mouse_pos)

        if self.board[grid_x][grid_y] == self.turn:
            self.selected_piece = grid_x, grid_y

    def get_selected_grid(self, mouse_pos):
        """
        get the index of the clicked pos given a mouse pos
        :param mouse_pos: tuple[int | int]
        :return: tuple[int | int]
        """
        x, y = mouse_pos

        grid_x = x // self.SQUARE_SIZE
        grid_y = y // self.SQUARE_SIZE

        return grid_x, grid_y

    def input(self):
        """
        Handels player input
        :return: to cicle or not to cicle turns -> boolean
        """
        # if player just clicked
        if self.just_pressed():
            mouse_pos = pg.mouse.get_pos()

            # select piece if it's not selected
            if not self.selected_piece:
                self.select_piece(mouse_pos)
                self.get_valid_moves()

            # if it's already selected...
            else:
                # ... check if the player selected a possible move
                jump = self.get_selected_grid(mouse_pos)
                capture_board = self.board.capture_piece(jump, self.selected_piece)
                if capture_board:
                    # capture and reset selected piece
                    self.selected_piece = None
                    self.valid_moves = []

                    self.print_evaluation()

                    # return True to cicle turns
                    return True

                # ... if the player clicked on another place other than a possible move
                else:
                    self.select_piece(mouse_pos)
                    self.get_valid_moves()

        # return false to not cicle moves
        return False

