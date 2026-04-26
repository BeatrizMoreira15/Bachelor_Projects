
class Player:
    def __init__(self, turn, board):
        self.turn = turn
        self.board = board
        self.number_pieces = 0
        self.count_pieces()
        self.selected_piece = None
        self.valid_moves = []

    def get_valid_moves(self):
        """
        gets the piece possible moves
        :return:
        """
        self.valid_moves = self.board.get_valid_moves(self.selected_piece)

    def count_pieces(self):
        npiece = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == self.turn:
                    npiece += 1

        self.number_pieces = npiece

    @staticmethod
    def evaluate(board):
        count_pieces = board.count_pieces()
        if board == 1:
            return count_pieces[1] - count_pieces[2]
        else:
            return count_pieces[2] - count_pieces[1]

    def print_evaluation(self):
        print(f"Player {self.turn} | Evaluation: {self.evaluate(self.board)}")

    def input(self):
        pass
