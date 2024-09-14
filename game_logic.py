import random


class TicTacToeLogic:
    def __init__(self):
        self.game_board = [[None for _ in range(3)] for _ in range(3)]
        self.game_ui = None
        self.difficulty = 'Easy'
        self.ai_score = 0
        self.player_score = 0
        self.first_move = False
        self.current_turn = 'O'
        self.board_patterns = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]

    def link_game_ui(self, game_ui):
        """Links the TicTacToeUI instance to the Logic."""
        self.game_ui = game_ui

    def set_difficulty(self, level):
        """Sets the difficulty level for the game as selected in the UI."""
        self.difficulty = level

    def player_move(self, row, col):
        """Handles player moves on board."""
        if self.current_turn == 'O' and self.game_board[row][col] is None:
            self.game_board[row][col] = 'O'
            self.game_ui.draw_o(row, col)
            if not self.check_winner('O'):
                self.current_turn = 'X'
                self.game_ui.window.after(150, self.computer_move)

        if not self.game_ui.menu_disabled:
            self.game_ui.disable_menu()

    def computer_move(self):
        """Handles computer moves on board."""
        if self.current_turn == 'X':
            move = None
            if self.difficulty == 'Easy':
                move = self.get_random_move()
            elif self.difficulty == 'Hard':
                move = self.get_best_move()
            elif self.difficulty == 'Pain':
                move = self.get_minimax_move()

            if move:
                row, col = move
                self.game_board[row][col] = 'X'
                self.game_ui.draw_x(row, col)
                if not self.check_winner('X'):
                    self.current_turn = 'O'

    def get_random_move(self):
        """Gets a random empty cell on board."""
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.game_board[row][col] is None]
        return random.choice(empty_cells) if empty_cells else None

    def get_best_move(self):
        """AI strategy for difficulty set to 'Hard'."""

        # Randomize first AI move
        if not self.first_move:
            possible_moves = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]  # Strong opening moves: corners and center
            while possible_moves:
                first_move = random.choice(possible_moves)
                row, col = first_move
                if self.game_board[row][col] is None:
                    self.first_move = True
                    return first_move
                else:
                    possible_moves.remove(first_move)

        best_score = float('-inf')
        best_move = []
        for row in range(3):
            for col in range(3):
                if self.game_board[row][col] is None:
                    self.game_board[row][col] = 'X'  # Temporarily make the move
                    score = self.evaluate_board()  # Evaluate the board state
                    self.game_board[row][col] = None  # Undo move

                    if score > best_score:
                        best_score = score
                        best_move = [(row, col)]

                    elif score == best_score:
                        best_score = score
                        best_move.append((row, col))

        return random.choice(best_move) if best_move else None

    def evaluate_board(self):
        """
        Evaluates the current board state and returns a score based on pattern analysis.
        Evaluation Logic:
            - Prioritizes blocking the opponent's potential winning move.
            - Balances between offensive and defensive moves based on the score system.
        """

        score = 0

        for pattern in self.board_patterns:
            x_count = 0
            o_count = 0
            for cell in pattern:
                row, col = cell
                if self.game_board[row][col] == 'X':
                    x_count += 1
                elif self.game_board[row][col] == 'O':
                    o_count += 1

            if x_count == 3:
                score += 100  # highest score if X wins  (X X X)
            elif o_count == 3:
                score -= 100  # lowest score if O wins  (O O O)
            elif x_count == 2 and o_count == 0:
                score += 10  # offensive move for X (X X -)
            elif x_count == 0 and o_count == 2:
                score -= 15  # higher penalty for not blocking O (O O -)
            elif x_count == 1 and o_count == 0:
                score += 1
            elif x_count == 0 and o_count == 1:
                score -= 1
            else:
                score += 0  # Scenarios with no beneficial moves (eg: X X O)

        return score

    def get_minimax_move(self):
        """Determines the optimal move for the AI using the Minimax algorithm for 'Pain' difficulty."""

        best_score = float('-inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.game_board[row][col] is None:
                    self.game_board[row][col] = 'X'
                    score = self.minimax(self.game_board, is_maximizing=False)
                    self.game_board[row][col] = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def minimax(self, board, is_maximizing):
        """
        Implements the Minimax algorithm to find the best possible move for the AI ('X') by simulating all possible
        moves and their outcomes.
        Maximizing Player ('X'): The AI, playing as 'X', aims to maximize its score. It looks for moves that lead to
                                 the highest possible score.
        Minimizing Player ('O'): The AI playing as opponent 'O', aims to minimize the AI's score. It looks for moves
                                 that lead to the lowest possible score for the AI.
        Returns:
        int: The score of the board state. 1 if 'X' wins, -1 if 'O' wins, 0 for a draw.
        """

        winner = self.get_winner(board)
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        elif not any(None in row for row in board):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] is None:
                        board[row][col] = 'X'
                        score = self.minimax(board, is_maximizing=False)
                        board[row][col] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] is None:
                        board[row][col] = 'O'
                        score = self.minimax(board, is_maximizing=True)
                        board[row][col] = None
                        best_score = min(score, best_score)
            return best_score

    def get_winner(self, board):
        """Checks board for a winner and returns the winner."""
        for pattern in self.board_patterns:
            if all(board[row][col] == 'X' for row, col in pattern):
                return 'X'
            if all(board[row][col] == 'O' for row, col in pattern):
                return 'O'

        return None

    def check_winner(self, sign):
        """Checks board for a winner and handles UI updates."""
        winner = self.get_winner(self.game_board)

        if winner == sign:
            for line in self.board_patterns:
                if all(self.game_board[row][col] == sign for row, col in line):
                    start_cell, end_cell = line[0], line[-1]
                    self.game_ui.display_results(sign, start_cell, end_cell)
                    self.update_score(sign)
                    return True

        if not self.get_random_move():
            self.game_ui.display_results(sign=None, start=None, end=None)

        return False

    def update_score(self, winner):
        """Updates the score based on the winner."""
        if winner == 'O':
            self.player_score += 1
        elif winner == 'X':
            self.ai_score += 1
        self.game_ui.update_scoreboard(self.ai_score, self.player_score)

    def restart_game(self):
        """Restarts the game."""
        self.game_board = [[None for _ in range(3)] for _ in range(3)]
        self.game_ui.clear_board()
        self.current_turn = 'O'
        self.first_move = False
        self.game_ui.difficulty_menu.config(state='normal')
        self.game_ui.menu_disabled = False
