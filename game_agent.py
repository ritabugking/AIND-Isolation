
class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    #  score = weighted improved score
    return float(own_moves - 2*opp_moves)

    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_loc = game.get_player_location(player)
    own_moves = len(game.get_legal_moves(player))
    # score = distance between player location and center location + the numbers of player's move
    return float((((own_loc[0]-3)**2+(own_loc[1]-3)**2)**0.5)) + own_moves
    

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_loc = game.get_player_location(player)
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    # score = distance between player location and center location + weighted improved score
    return float(((own_loc[0]-3)**2+(own_loc[1]-3)**2)**0.5) + own_moves - 2*opp_moves


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.
    ********************  DO NOT MODIFY THIS CLASS  ********************
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************
        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        
        self.time_left = time_left
      
        if not game.get_legal_moves():
            return (-1,-1)
        best_move=game.get_legal_moves()[0]

        try:
            
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # if time out

        # return the best move calculated by depth-limited minimax search algorithm
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        def maxValue(game, depth):
            # if time out
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # when no more legal move or time out, terminate.
            if len(game.get_legal_moves()) == 0 or depth == 0:
                return self.score(game, self)
            v = float('-inf')
            for m in game.get_legal_moves():
                # return the max value for each comparement
                v = max(v, minValue(game.forecast_move(m), depth - 1))
            return v

        def minValue(game, depth):
            # if time out
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # when no more legal move or time out, terminate.
            if len(game.get_legal_moves()) == 0 or depth == 0:
                return self.score(game, self)
            v = float('inf')
            for m in game.get_legal_moves():
                # return the min value for each comparement
                v = min(v, maxValue(game.forecast_move(m), depth - 1))
            return v

        # the start of class of MinimaxPlayer 
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if len(game.get_legal_moves()) == 0:
            return (-1, -1)

        

        best = float('-inf')
        move = game.get_legal_moves()[0]
#        move = game.get_legal_moves()[0]
#        for m in game.get_legal_moves():
#            move = max([(minValue(game.forecast_move(m), depth - 1), m)])
#        return move
        # return the move which can get the maximal value
        for m in game.get_legal_moves():
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            val = minValue(game.forecast_move(m), depth - 1)
            if val > best:
                best = val
                move = m
        return move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        if not game.get_legal_moves():
            return (-1,-1)
        best_move = game.get_legal_moves()[0]

        i=0
        while True:
            try:
                # reach the deepest level before time out
                best_move=self.alphabeta(game,i)
                i += 1

            except SearchTimeout:
                break  # if time out

        # return the best move calculated by depth-limited minimax search algorithm with alpha-beta pruning
        return best_move

        


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        def maxValue(game, depth, alpha, beta):
            # if time out
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # when no more legal move or time out, terminate.
            if len(game.get_legal_moves()) == 0 or depth == 0:
                return self.score(game, self)
            v = float('-inf')
            for m in game.get_legal_moves():
                # return the max value for each comparement
                v = max(v, minValue(game.forecast_move(m), depth - 1, alpha, beta))
                # if value >= beta, don't need to care of the other value
                if v >= beta:
                    return v
                alpha = max(v, alpha) # set alpha = max value
            return v


        def minValue(game, depth, alpha, beta):
            # if time out
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # when no more legal move or time out, terminate.
            if len(game.get_legal_moves()) == 0 or depth <= 0:
                return self.score(game, self)
            v = float('inf')
            for m in game.get_legal_moves():
                # return the max value for each comparement
                v = min(v, maxValue(game.forecast_move(m), depth - 1, alpha, beta))
                # if value <= alpha, don't need to care of the other value
                if v <= alpha:
                    return v
                beta = min(v, beta) # set beta = min value
            return v

        # the start of class of AlphaBetaPlayer 
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if len(game.get_legal_moves()) == 0:
            return (-1, -1)

        best = float('-inf')
        move = game.get_legal_moves()[0]

        # return the move which can get the maximal value
        for m in game.get_legal_moves():
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            val = minValue(game.forecast_move(m), depth - 1, alpha, beta)
            if val > best:
                best = val
                move = m
            alpha = max(alpha, val)
        return move