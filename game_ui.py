import tkinter as tk
from game_logic import TicTacToeLogic


class TicTacToeUI:
    def __init__(self):
        self.WINDOW_BG = "#003C43"
        self.CELL_SIZE = 120
        self.GRID_SIZE = 3
        self.BOARD_SIZE = self.CELL_SIZE * self.GRID_SIZE
        self.pad_x = 40
        self.pad_y = 20
        self.ai_score = 0
        self.player_score = 0
        self.game_logic = TicTacToeLogic()
        self.game_logic.link_game_ui(self)
        self.menu_disabled = False

        # Initialize window with widgets
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe')
        self.window.config(padx=self.pad_x, pady=self.pad_y, bg=self.WINDOW_BG)
        self.window.geometry(f"620x780")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=self.BOARD_SIZE, height=self.BOARD_SIZE, bg=self.WINDOW_BG,
                                highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=90)
        self.canvas.bind('<Button-1>', self.get_canvas_click)

        difficulty = tk.StringVar(self.window)
        difficulty.set('Easy')
        self.difficulty_menu = tk.OptionMenu(self.window, difficulty, 'Easy', 'Hard', 'Pain',
                                             command=self.set_difficulty)
        self.difficulty_menu.config(font=('Courier', 15), bg=self.WINDOW_BG, fg=self.WINDOW_BG, width=10)
        self.difficulty_menu.grid(row=0, column=0, sticky='nw')

        self.scoreboard = tk.Frame(self.window, bg=self.WINDOW_BG)
        self.scoreboard.grid(row=0, column=0, columnspan=2, pady=50)

        self.ai_score_canvas = tk.Canvas(self.scoreboard, width=200, height=130, bg=self.WINDOW_BG,
                                         highlightthickness=0)
        self.ai_score_canvas.grid(row=0, column=0, padx=20)
        self.ai_score_canvas.create_rectangle(10, 40, 190, 90, outline="#A8CD9F", width=4)
        self.ai_score_label = tk.Label(self.ai_score_canvas, text=f'AI: {self.ai_score}', font=('Courier', 15),
                                       fg='#F1F1F1', bg=self.WINDOW_BG)
        self.ai_score_label.place(relx=0.5, rely=0.5, anchor='center')

        self.player_score_canvas = tk.Canvas(self.scoreboard, width=200, height=130, bg=self.WINDOW_BG,
                                             highlightthickness=0)
        self.player_score_canvas.grid(row=0, column=1, padx=20)
        self.player_score_canvas.create_rectangle(10, 40, 190, 90, outline="#A8CD9F", width=4)
        self.player_score_label = tk.Label(self.player_score_canvas, text=f'Player: {self.player_score}',
                                           font=('Courier', 15), fg='#F1F1F1', bg=self.WINDOW_BG)
        self.player_score_label.place(relx=0.5, rely=0.5, anchor='center')

        self.result_label = tk.Label(self.window, text='', font=('Courier', 30), bd=7, fg=self.WINDOW_BG,
                                     relief=tk.RAISED)
        self.result_label.grid(row=1, column=0, columnspan=2)
        self.result_label.grid_remove()

        self.restart_button = tk.Button(self.window, text='Restart', font=('Courier', 15), width=10, height=2,
                                        fg=self.WINDOW_BG, command=self.restart_game)
        self.restart_button.grid(row=2, column=0, columnspan=2, pady=(80, 30))

        self.draw_game_board()

    def set_difficulty(self, selection):
        """Updates the game_logic difficulty level based on the current UI selection."""
        if self.game_logic:
            self.game_logic.set_difficulty(selection)

    def disable_menu(self):
        """Disables the game difficulty menu."""
        self.difficulty_menu.config(state='disabled')
        self.menu_disabled = True

    def draw_game_board(self):
        """Draws grid lines for the TicTacToe board."""
        for i in range(1, self.GRID_SIZE):
            x0 = i * self.CELL_SIZE
            y0 = 0
            x1 = x0
            y1 = self.BOARD_SIZE
            self.canvas.create_line(x0, y0, x1, y1, width=3, fill='#135D66')
            self.canvas.create_line(y0, x0, y1, x1, width=3, fill='#135D66')

    def get_canvas_click(self, event):
        """Handles canvas clicks and triggers player move."""
        row = event.y // self.CELL_SIZE
        col = event.x // self.CELL_SIZE
        if self.game_logic:
            self.game_logic.player_move(row, col)

    def draw_x(self, row, col):
        """Draws animated 'X' at specified cell."""

        # Calculate the center of the cell
        center_x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = row * self.CELL_SIZE + self.CELL_SIZE // 2

        # Calculate the start and end points of the lines
        offset = self.CELL_SIZE // 12  # offset from cell edges
        x0 = center_x - offset
        y0 = center_y - offset
        x1 = center_x + offset
        y1 = center_y + offset

        line_1 = self.canvas.create_line(x0, y0, x1, y1, fill='#A8CD9F', width=4)
        line_2 = self.canvas.create_line(x1, y0, x0, y1, fill='#A8CD9F', width=4)

        # Animation
        for i in range(10):
            self.canvas.after(15)
            self.canvas.scale(line_1, center_x, center_y, 1.1, 1.1)  # Scale the first line
            self.canvas.scale(line_2, center_x, center_y, 1.1, 1.1)  # Scale the second line
            self.canvas.update()

    def draw_o(self, row, col):
        """Draws animated 'O' at specified cell."""
        center_x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = row * self.CELL_SIZE + self.CELL_SIZE // 2

        offset = self.CELL_SIZE // 12
        x0 = center_x - offset
        y0 = center_y - offset
        x1 = center_x + offset
        y1 = center_y + offset

        oval = self.canvas.create_oval(x0, y0, x1, y1, outline='white', width=4)

        # Animation
        for i in range(10):
            self.canvas.after(15)
            self.canvas.scale(oval, center_x, center_y, 1.1, 1.1)
            self.canvas.update()

    def draw_winning_line(self, start_cor, end_cor):
        """
            Draws an animated winning line from start_cor to end_cor.
            Args:
                start_cor (tuple): Starting cell coordinates (row, col).
                end_cor (tuple): Ending cell coordinates (row, col).
            """
        y0, x0 = start_cor
        y1, x1 = end_cor

        # Convert cell coordinates to pixel coordinates
        x0 = x0 * self.CELL_SIZE + self.CELL_SIZE // 2
        y0 = y0 * self.CELL_SIZE + self.CELL_SIZE // 2
        x1 = x1 * self.CELL_SIZE + self.CELL_SIZE // 2
        y1 = y1 * self.CELL_SIZE + self.CELL_SIZE // 2

        # Calculate the direction vector
        dir_x = x1 - x0
        dir_y = y1 - y0

        # Normalize the direction vector to unit length (enables uniform extension of line)
        length = (dir_x ** 2 + dir_y ** 2) ** 0.5
        norm_x = dir_x / length
        norm_y = dir_y / length

        # Extend the line by a fixed amount
        extend_length = self.CELL_SIZE // 3
        start_x = x0 - norm_x * extend_length
        start_y = y0 - norm_y * extend_length
        end_x = x1 + norm_x * extend_length
        end_y = y1 + norm_y * extend_length

        # Animation parameters
        steps = 20
        delay = 15
        delta_x = (end_x - start_x) / steps
        delta_y = (end_y - start_y) / steps

        def animate_line(step=0):
            if step <= steps:
                curr_x = start_x + step * delta_x
                curr_y = start_y + step * delta_y
                self.canvas.create_line(start_x, start_y, curr_x, curr_y, fill='#9BB0C1', width=4)
                self.canvas.after(delay, animate_line, step + 1)

        animate_line()

    def display_results(self, sign, start, end):
        """Displays game results."""

        def animate_result(label, sign, length=0):
            if sign == 'O':
                text = 'You win!'
            elif sign == 'X':
                text = 'AI wins!'
            else:
                text = 'Draw!'

            label.grid()
            label.config(text=text[:length])
            if length < len(text):
                self.window.after(25, animate_result, label, sign, length + 1)

        delay = 100
        if sign is not None:
            delay = 400
            self.draw_winning_line(start, end)

        self.canvas.after(delay, animate_result, self.result_label, sign)
        self.canvas.unbind('<Button-1>')
        self.difficulty_menu.config(state='normal')

    def update_scoreboard(self, ai_score, player_score):
        self.ai_score_label.config(text=f'AI: {ai_score}')
        self.player_score_label.config(text=f'Player: {player_score}')

    def clear_board(self):
        """Resets game board and UI at restart."""
        self.result_label.config(text='')
        self.result_label.grid_remove()
        self.canvas.delete('all')
        self.draw_game_board()
        self.canvas.bind('<Button-1>', self.get_canvas_click)

    def restart_game(self):
        if self.game_logic:
            self.game_logic.restart_game()
