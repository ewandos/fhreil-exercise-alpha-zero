class HexPosition(object):
    """
    The class hexPosition stores data on a hex board position. The slots of an object are: size (an integer between 2
    and 26), board (an array, 0=noStone, 1=whiteStone, 2=blackStone), and winner (0=noWin, 1=whiteWin, 2=blackWin).
    """

    def __init__(self, size=5):
        self.size = max(2, min(size, 26))
        self.board = [[0 for _ in range(max(2, min(size, 26)))] for _ in range(max(2, min(size, 26)))]
        self.winner = 0

    # ----------------------------------
    # A I     A P I
    # ----------------------------------

    def make_move(self, chosen, player):
        self.board[chosen[0]][chosen[1]] = player

    def does_winner_exist(self):
        self.white_win()
        self.black_win()
        return self.winner

    def get_action_space(self, recode_black_as_white=False):
        """
        This method returns a list of array positions which are empty (on which stones may be put).
        """

        actions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    actions.append((i, j))
        if recode_black_as_white:
            return [self.recode_coordinates(action) for action in actions]
        else:
            return actions

    def reset(self):
        """
        This method resets the hex board. All stones are removed from the board.
        """

        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.winner = 0

    # ----------------------------------
    # E N G I N E   F U N C T I O N S
    # ----------------------------------

    def get_adjacent(self, position):
        """
        Helper function to obtain adjacent cells in the board array.
        """

        up = (position[0] - 1, position[1])
        down = (position[0] + 1, position[1])
        right = (position[0], position[1] - 1)
        left = (position[0], position[1] + 1)
        up_right = (position[0] - 1, position[1] + 1)
        down_left = (position[0] + 1, position[1] - 1)

        return [pair for pair in [up, down, right, left, up_right, down_left] if
                max(pair[0], pair[1]) <= self.size - 1 and min(pair[0], pair[1]) >= 0]

    def recode_coordinates(self, coordinates):
        """
        Transforms a coordinate tuple (with respect to the board) analogously to the method recodeBlackAsWhite.
        """
        return self.size - 1 - coordinates[1], self.size - 1 - coordinates[0]

    def prolong_path(self, path):
        """
        A helper function used for board evaluation.
        """

        player = self.board[path[-1][0]][path[-1][1]]
        candidates = self.get_adjacent(path[-1])

        # preclude loops
        candidates = [cand for cand in candidates if cand not in path]
        candidates = [cand for cand in candidates if self.board[cand[0]][cand[1]] == player]

        return [path + [cand] for cand in candidates]

    def white_win(self, verbose=False):
        """
        Evaluate whether the board position is a win for 'white'. Uses breadth first search. If verbose=True a winning
        path will be printed to the standard output (if one exists). This method may be time-consuming,
        especially for larger board sizes.
        """

        paths = []
        visited = []
        for i in range(self.size):
            if self.board[i][0] == 1:
                paths.append([(i, 0)])
                visited.append([(i, 0)])

        while True:

            if len(paths) == 0:
                return False

            for path in paths:
                prolongations = self.prolong_path(path)
                paths.remove(path)

                for new in prolongations:
                    if new[-1][1] == self.size - 1:
                        if verbose:
                            print("A winning path for White:\n", new)
                        self.winner = 1
                        return True

                    if new[-1] not in visited:
                        paths.append(new)
                        visited.append(new[-1])

    def black_win(self, verbose=False):
        """
        Evaluate whether the board position is a win for 'black'. Uses breadth first search. If verbose=True a winning
        path will be printed to the standard output (if one exists).
        This method may be time-consuming, especially for larger board sizes.
        """

        paths = []
        visited = []
        for i in range(self.size):
            if self.board[0][i] == 2:
                paths.append([(0, i)])
                visited.append([(0, i)])

        while True:

            if len(paths) == 0:
                return False

            for path in paths:
                prolongations = self.prolong_path(path)
                paths.remove(path)

                for new in prolongations:
                    if new[-1][0] == self.size - 1:
                        if verbose:
                            print("A winning path for Black:\n", new)
                        self.winner = 2
                        return True

                    if new[-1] not in visited:
                        paths.append(new)
                        visited.append(new[-1])
