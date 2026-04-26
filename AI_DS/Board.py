class Board:
    def __init__(self, board):
        # store board
        self.board = board

    @staticmethod
    def is_valid_diagonal(x1, y1, x2, y2):
        """
        returns if the diagonal move is posssible given two points
        :param x1: point1 x -> int
        :param y1: point1 y -> int
        :param x2: point2 x -> int
        :param y2: point2 y -> int
        :return: boolean
        """

        # returns false if the points are in the same column or row
        if x1 == x2 or y1 == y2:
            return False

        # returns True if the distance bettween the points is 1
        # and checks if p1 coincides with a valid alternating point with diagonals
        return abs(x1 - x2) == abs(y1 - y2) == 1 and (x1 + y1) % 2 == 0

    def can_move(self, player_x, player_y, check_x, check_y):
        """
        this functions cheks if a piece can be moved to another place
        :param player_x: int
        :param player_y: int
        :param check_x: int
        :param check_y: int
        :return: boolean
        """
        # check limit
        if not (0 <= check_x < len(self.board) and 0 <= check_y < len(self.board)):
            return False

        if self.board[check_x][check_y] == 0:
            if check_x == player_x or check_y == player_y:
                return True

            elif self.is_valid_diagonal(player_x, player_y, check_x, check_y):
                return True

        return False

    def can_capture_move(self, player_x, player_y, check_x, check_y):
        """
        this function gets the capture move given a player pos and the closest piece
        :param player_x: int
        :param player_y: int
        :param check_x: int
        :param check_y: int
        :return:
        """
        direction_x = check_x - player_x
        direction_y = check_y - player_y

        move = False

        # check if direction is possible
        if (check_x == player_x or check_y == player_y) or self.is_valid_diagonal(player_x, player_y, check_x, check_y):

            # loop to capture multiple pieces -- checks limits
            while True:
                # FIXME: can capture in muliple directions

                # checks to see if there is an enemy piece
                if 0 != self.board[check_x][check_y] != self.board[player_x][player_y]:

                    # jump to the next piece
                    check_x += direction_x
                    check_y += direction_y

                    # check limit
                    if not (0 <= check_x < len(self.board) and 0 <= check_y < len(self.board)):
                        break

                    # checks if the piece is empty
                    if self.board[check_x][check_y] == 0:
                        # saves the move
                        move = (check_x, check_y, True)
                    else:
                        break

                    # jump to the next piece
                    check_x += direction_x
                    check_y += direction_y

                    # check limit
                    if not (0 <= check_x < len(self.board) and 0 <= check_y < len(self.board)):
                        break

                else:
                    break

        return move

    def has_capture_moves(self, selected_piece):
        """
        returns true if the player has capture moves
        :param selected_piece: {x, y} -> tuple[int | int]
        :return: boolean
        """
        # get current player
        player = self.board[selected_piece[0]][selected_piece[1]]

        # loop through all pieces in the board
        for player_x in range(len(self.board)):
            for player_y in range(len(self.board[0])):

                # if the piece belongs to the player
                if self.board[player_x][player_y] == player:

                    # check if the piece has capture moves
                    if len(self.get_capture_moves((player_x, player_y))) > 0:
                        return True

        return False

    def get_moves(self, selected_piece):
        """
        gets all possible moves given a selected_piece
        :param selected_piece: {x, y} -> tuple[int | int]
        :return: {x, y, is_capture_move} -> list[tuple[int, int, boolean]
        """
        moves = []

        # player position
        player_x, player_y = selected_piece

        # possible directions for each player

        # loop through all possible directions
        for direction_x in (-1, 0, 1):
            for direction_y in (-1, 0, 1):

                # ignore the selected piece itself
                if direction_y == direction_x == 0:
                    continue

                # point to be checked
                check_x = player_x + direction_x
                check_y = player_y + direction_y

                # check limits
                if 0 <= check_x < len(self.board) and 0 <= check_y < len(self.board):

                    # appends move if it's possible
                    if self.can_move(player_x, player_y, check_x, check_y):
                        moves.append((check_x, check_y, False))

        return moves

    def get_capture_moves(self, selected_piece):
        """
        returns a list of possible moves given a selected piece
        :param selected_piece:
        :return: {x, y, is_capture_move} -> list[tuple[int | int | boolean]]
        """
        moves = []

        # player position
        player_x, player_y = selected_piece

        # loop through all possible directions
        for direction_x in (-1, 0, 1):
            for direction_y in (-1, 0, 1):

                # ignore the selected piece itself
                if direction_y == direction_x == 0:
                    continue

                # point to be checked
                check_x = player_x + direction_x
                check_y = player_y + direction_y

                # check limits
                if 0 <= check_x < len(self.board) and 0 <= check_y < len(self.board[0]):

                    # appends capture move if there is a capture move that is possible
                    capture_move = self.can_capture_move(player_x, player_y, check_x, check_y)
                    if capture_move:
                        moves.append(capture_move)

        return moves

    def get_valid_moves(self, selected_piece):
        """
        gets the piece possible moves
        :param selected_piece: {x, y} -> tuple[int | int]
        :return:
        """
        if selected_piece:
            if self.has_capture_moves(selected_piece):
                moves = self.get_capture_moves(selected_piece)
            else:
                moves = self.get_moves(selected_piece)

            return moves

        return None

    def delete_pieces(self, player_x, player_y, jump_x, jump_y):
        direction_x = player_x - jump_x
        if direction_x > 0:
            direction_x = 1
        elif direction_x < 0:
            direction_x = -1

        direction_y = player_y - jump_y
        if direction_y > 0:
            direction_y = 1
        elif direction_y < 0:
            direction_y = -1

        delete_x = jump_x
        delete_y = jump_y

        while delete_x != player_x or delete_y != player_y:
            self.board[delete_x][delete_y] = 0

            delete_x += direction_x
            delete_y += direction_y

        self.board[player_x][player_y] = 0

    def capture_piece(self, jump, selected_piece):
        valid_moves = self.get_valid_moves(selected_piece)

        player_x, player_y = selected_piece
        player = self.board[player_x][player_y]
        jump_x, jump_y = jump

        if (jump_x, jump_y, False) in valid_moves:
            self.board[player_x][player_y] = 0
            self.board[jump_x][jump_y] = player

            return True

        elif (jump_x, jump_y, True) in valid_moves:

            self.delete_pieces(player_x, player_y, jump_x, jump_y)

            self.board[jump_x][jump_y] = player

            return True

        else:
            return False

    def possible_plays(self, turn):
        possible_plays_list = []
        for x in range(len(self.board)):
            for y in range(len(self.board)):

                if self.board[x][y] == turn:
                    valid_moves = self.get_valid_moves((x, y))

                    if valid_moves:
                        for move in valid_moves:
                            jump_x = move[0]
                            jump_y = move[1]
                            possible_plays_list.append((x, y, jump_x, jump_y))

        return possible_plays_list

    def isEndState(self):
        pieces = self.count_pieces()
        if pieces[1] == 0 or pieces[2] == 0:
            return True
        return False

    def count_pieces(self):
        npiece = [0, 0, 0]
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    npiece[0] += 1
                elif self.board[row][col] == 1:
                    npiece[1] += 1
                else:
                    npiece[2] += 1
        return npiece

    def __len__(self):
        return len(self.board)

    def __getitem__(self, item):
        return self.board[item]

    def __str__(self):
        return str(self.board)

    def copy(self):
        b = []
        for x in range(len(self.board)):
            b.append([])
            for y in range(len(self.board)):
                b[x].append(self.board[x][y])

        return Board(b)
