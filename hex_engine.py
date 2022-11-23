class hexPosition(object):
    """
    The class hexPosition stores data on a hex board position. The slots of an object are: size (an integer between 2 and 26), board (an array, 0=noStone, 1=whiteStone, 2=blackStone), and winner (0=noWin, 1=whiteWin, 2=blackWin).
    """

    def __init__(self, size=5):
        self.size = max(2, min(size, 26))

        self.board = [[0 for x in range(max(2, min(size, 26)))] for y in range(max(2, min(size, 26)))]
        self.winner = 0

    def reset(self):
        """
        This method resets the hex board. All stones are removed from the board.
        """

        self.board = [[0 for x in range(self.size)] for y in range(self.size)]
        self.winner = 0

    def getAdjacent(self, position):
        """
        Helper function to obtain adjacent cells in the board array.
        """

        u = (position[0] - 1, position[1])
        d = (position[0] + 1, position[1])
        r = (position[0], position[1] - 1)
        l = (position[0], position[1] + 1)
        ur = (position[0] - 1, position[1] + 1)
        dl = (position[0] + 1, position[1] - 1)

        return [pair for pair in [u, d, r, l, ur, dl] if
                max(pair[0], pair[1]) <= self.size - 1 and min(pair[0], pair[1]) >= 0]

    def getActionSpace(self, recodeBlackAsWhite=False):
        """
        This method returns a list of array positions which are empty (on which stones may be put).
        """

        actions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    actions.append((i, j))
        if recodeBlackAsWhite:
            return [self.recodeCoordinates(action) for action in actions]
        else:
            return (actions)

    def playRandom(self, player):
        """
        This method returns a uniformly randomized valid moove for the chosen player (player=1, or player=2).
        """
        from random import choice

        chosen = choice(self.getActionSpace())
        self.board[chosen[0]][chosen[1]] = player

    def randomMatch(self, evaluate_when_full=False):
        """
        This method randomizes an entire playthrough. Mostly useful to test code functionality. If evaluate_when_full=True then the board will be completely filled before the position is evaluated. Otherwise evaluation happens after every moove.
        """

        player = 1

        if evaluate_when_full:
            for i in range(self.size ** 2):
                self.playRandom(player)
                if (player == 1):
                    player = 2
                else:
                    player = 1
            self.whiteWin()
            self.blackWin()

        else:
            while self.winner == 0:
                self.playRandom(player)
                if (player == 1):
                    self.whiteWin()
                    player = 2
                else:
                    self.blackWin()
                    player = 1

    def prolongPath(self, path):
        """
        A helper function used for board evaluation.
        """

        player = self.board[path[-1][0]][path[-1][1]]
        candidates = self.getAdjacent(path[-1])

        # preclude loops
        candidates = [cand for cand in candidates if cand not in path]
        candidates = [cand for cand in candidates if self.board[cand[0]][cand[1]] == player]

        return [path + [cand] for cand in candidates]

    def whiteWin(self, verbose=False):
        """
        Evaluate whether the board position is a win for 'white'. Uses breadth first search. If verbose=True a winning path will be printed to the standard output (if one exists). This method may be time-consuming, especially for larger board sizes.
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
                prolongations = self.prolongPath(path)
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

    def blackWin(self, verbose=False):
        """
        Evaluate whether the board position is a win for 'black'. Uses breadth first search. If verbose=True a winning path will be printed to the standard output (if one exists). This method may be time-consuming, especially for larger board sizes.
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
                prolongations = self.prolongPath(path)
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

# Initializing an object
myboard = hexPosition(size=7)
