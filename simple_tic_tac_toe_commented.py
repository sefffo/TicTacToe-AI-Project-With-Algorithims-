# Import the tkinter library for creating the GUI
import tkinter as tk
# Import messagebox for displaying popup dialogs
from tkinter import messagebox


class SimpleTicTacToe:
    """
    Main class for the Tic-Tac-Toe game with AI algorithms.
    This class handles the game logic, UI, and AI decision-making.
    """

    def __init__(self):
        """
        Constructor: Initializes the game when creating a new SimpleTicTacToe object.
        Sets up the window, game state, and creates the user interface.
        """
        # Create the main window using Tkinter
        self.window = tk.Tk()

        # Set the title that appears in the window's title bar
        self.window.title("Tic-Tac-Toe AI")

        # Set window size to 400 pixels wide and 500 pixels tall
        self.window.geometry("400x500")

        # Initialize the game board as a list of 9 empty strings
        # Index mapping: [0,1,2] = top row, [3,4,5] = middle row, [6,7,8] = bottom row
        # Example board layout:
        # 0 | 1 | 2
        # ---------
        # 3 | 4 | 5
        # ---------
        # 6 | 7 | 8
        self.board = ['' for _ in range(9)]

        # List to store references to all 9 button widgets on the board
        self.buttons = []

        # Default AI algorithm is BFS (Breadth-First Search)
        self.algorithm = "BFS"

        # Flag to track if the current game has ended (win/loss/draw)
        self.game_over = False

        # Call the method to create all UI elements
        self.create_ui()

    def create_ui(self):
        """
        Creates all the visual elements of the game interface.
        This includes: title, algorithm selector, game board, and control buttons.
        """
        # === TITLE SECTION ===
        # Create and display the game title at the top
        tk.Label(self.window, text="Tic-Tac-Toe", font=('Arial', 20, 'bold')).pack(pady=10)

        # === ALGORITHM SELECTION SECTION ===
        # Create a frame (container) to hold the algorithm selection buttons
        algo_frame = tk.Frame(self.window)
        # Add the frame to the window with 10 pixels of padding on top and bottom
        algo_frame.pack(pady=10)

        # Create a label asking the user to choose an AI algorithm
        tk.Label(algo_frame, text="Choose AI:", font=('Arial', 11)).grid(row=0, column=0, padx=5)

        # Create BFS button - when clicked, sets algorithm to BFS
        # lambda: creates an anonymous function that calls set_algorithm("BFS")
        tk.Button(algo_frame, text="BFS", width=8, bg='lightblue',
                 command=lambda: self.set_algorithm("BFS")).grid(row=0, column=1, padx=3)

        # Create DFS button - when clicked, sets algorithm to DFS
        tk.Button(algo_frame, text="DFS", width=8, bg='lightgreen',
                 command=lambda: self.set_algorithm("DFS")).grid(row=0, column=2, padx=3)

        # Create A* button - when clicked, sets algorithm to A*
        tk.Button(algo_frame, text="A*", width=8, bg='lightyellow',
                 command=lambda: self.set_algorithm("A*")).grid(row=0, column=3, padx=3)

        # Create a label to display which algorithm is currently selected
        self.algo_label = tk.Label(self.window, text="AI: BFS", font=('Arial', 12, 'bold'), fg='blue')
        self.algo_label.pack()

        # === GAME BOARD SECTION ===
        # Create a frame to hold the 3x3 grid of buttons
        board_frame = tk.Frame(self.window)
        board_frame.pack(pady=20)

        # Loop through positions 0-8 to create 9 buttons
        for i in range(9):
            # Create a button for each board position
            # lambda pos=i: captures the current value of i for this button
            btn = tk.Button(board_frame, text='', font=('Arial', 24, 'bold'),
                          width=5, height=2, bg='white',
                          command=lambda pos=i: self.player_click(pos))

            # Position the button in a 3x3 grid
            # i//3 gives the row (0, 1, or 2)
            # i%3 gives the column (0, 1, or 2)
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)

            # Add this button to our list so we can reference it later
            self.buttons.append(btn)

        # === CONTROL BUTTONS SECTION ===
        # Create a frame to hold the New Game and Rematch buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)

        # Create "New Game" button - resets the game completely
        tk.Button(btn_frame, text="New Game", font=('Arial', 12),
                 bg='orange', width=12, command=self.reset).pack(side=tk.LEFT, padx=5)

        # Create "Rematch" button - starts a new game with the same AI
        tk.Button(btn_frame, text="Rematch", font=('Arial', 12),
                 bg='lightgreen', width=12, command=self.rematch).pack(side=tk.LEFT, padx=5)

    def set_algorithm(self, algo):
        """
        Changes the AI algorithm when user clicks BFS, DFS, or A* button.

        Parameters:
            algo (str): The algorithm name ("BFS", "DFS", or "A*")
        """
        # Store the selected algorithm
        self.algorithm = algo

        # Update the label to show which algorithm is now active
        self.algo_label.config(text=f"AI: {algo}")

    def player_click(self, pos):
        """
        Handles when the player clicks on a board position.

        Parameters:
            pos (int): The position clicked (0-8)
        """
        # Check if the position is empty AND the game is still ongoing
        if self.board[pos] == '' and not self.game_over:
            # Place player's mark (X) on the board
            self.board[pos] = 'X'

            # Update the button to show X in blue color and disable it
            self.buttons[pos].config(text='X', fg='blue', state='disabled')

            # Check if the game ended (player won or draw)
            if not self.check_end():
                # If game continues, let AI make its move after 300ms delay
                # This delay makes the game feel more natural
                self.window.after(300, self.ai_turn)

    def ai_turn(self):
        """
        AI's turn to make a move. Calls the appropriate algorithm based on selection.
        """
        # Check which algorithm is selected and call the corresponding method
        if self.algorithm == "BFS":
            move = self.bfs()  # Get move using Breadth-First Search
        elif self.algorithm == "DFS":
            move = self.dfs()  # Get move using Depth-First Search
        else:  # A*
            move = self.astar()  # Get move using A* algorithm

        # If a valid move was found (not None)
        if move is not None:
            # Place AI's mark (O) on the board at the chosen position
            self.board[move] = 'O'

            # Update the button to show O in red color and disable it
            self.buttons[move].config(text='O', fg='red', state='disabled')

            # Check if the game ended after AI's move
            self.check_end()

    def bfs(self):
        """
        BFS (Breadth-First Search) Algorithm

        How it works:
        1. First level: Check all positions to see if AI can win immediately
        2. Second level: Check all positions to see if must block player
        3. Third level: Choose strategic positions (center > corners > edges)

        BFS explores all possibilities at each level before moving to the next level.

        Returns:
            int: The position (0-8) where AI should move, or None if no moves available
        """

        # === LEVEL 1: OFFENSIVE - Try to win immediately ===
        # Loop through all 9 positions
        for i in range(9):
            # Check if this position is empty
            if self.board[i] == '':
                # Temporarily place AI's mark (O) here
                self.board[i] = 'O'

                # Check if this move would make AI win
                if self.is_winner('O'):
                    # Remove the temporary mark
                    self.board[i] = ''
                    # Return this position - it's a winning move!
                    return i

                # This move doesn't win, so remove the temporary mark
                self.board[i] = ''

        # === LEVEL 2: DEFENSIVE - Block player from winning ===
        # Loop through all 9 positions again
        for i in range(9):
            # Check if this position is empty
            if self.board[i] == '':
                # Temporarily place player's mark (X) here
                self.board[i] = 'X'

                # Check if player would win with this move
                if self.is_winner('X'):
                    # Remove the temporary mark
                    self.board[i] = ''
                    # Return this position - we must block it!
                    return i

                # Player wouldn't win here, remove temporary mark
                self.board[i] = ''

        # === LEVEL 3: STRATEGIC - Choose best available position ===

        # Strategy 1: Take the center if available (position 4)
        # Center is the most valuable position in tic-tac-toe
        if self.board[4] == '':
            return 4

        # Strategy 2: Take a corner if available
        # Corners (positions 0, 2, 6, 8) are second most valuable
        for corner in [0, 2, 6, 8]:
            if self.board[corner] == '':
                return corner

        # Strategy 3: Take any remaining edge position
        # If center and corners are taken, choose any empty position
        for i in range(9):
            if self.board[i] == '':
                return i

    def dfs(self):
        """
        DFS (Depth-First Search) Algorithm

        How it works:
        DFS follows a predefined priority order and explores deeply:
        1. Check positions in priority order for immediate win
        2. Check positions in priority order to block player
        3. Return first available position in priority order

        Priority: center (4) > corners (0,2,6,8) > edges (1,3,5,7)

        DFS differs from BFS by following a specific path deeply before backtracking,
        rather than checking all positions at each level.

        Returns:
            int: The position (0-8) where AI should move, or None if no moves available
        """

        # Define the priority order for checking positions
        # Position 4 (center) is highest priority, then corners, then edges
        # This creates a "depth-first" exploration path
        priority = [4, 0, 2, 6, 8, 1, 3, 5, 7]

        # === DEPTH 1: OFFENSIVE - Try to win immediately ===
        # Loop through positions in priority order
        for i in priority:
            # Check if this prioritized position is empty
            if self.board[i] == '':
                # Temporarily place AI's mark (O)
                self.board[i] = 'O'

                # Check if this is a winning move
                if self.is_winner('O'):
                    # Remove temporary mark
                    self.board[i] = ''
                    # Return winning position
                    return i

                # Not a winning move, remove temporary mark
                self.board[i] = ''

        # === DEPTH 2: DEFENSIVE - Block player ===
        # Loop through positions in priority order again
        for i in priority:
            # Check if this prioritized position is empty
            if self.board[i] == '':
                # Temporarily place player's mark (X)
                self.board[i] = 'X'

                # Check if player would win with this move
                if self.is_winner('X'):
                    # Remove temporary mark
                    self.board[i] = ''
                    # Must block this position
                    return i

                # Player wouldn't win, remove temporary mark
                self.board[i] = ''

        # === DEPTH 3: STRATEGIC - Follow priority order ===
        # No immediate threats, so follow the priority list
        for i in priority:
            # Return the first empty position in priority order
            if self.board[i] == '':
                return i

    def astar(self):
        """
        A* (A-Star) Algorithm

        How it works:
        A* uses a heuristic function (scoring system) to evaluate each move:
        1. First check for immediate win (highest priority)
        2. Then check for blocking moves (second priority)
        3. Finally, score all empty positions and choose the highest score

        Scoring heuristic:
        - Center (position 4): 4 points
        - Corners (positions 0,2,6,8): 3 points
        - Edges (positions 1,3,5,7): 2 points

        A* is optimal because it always chooses the move with the best score,
        combining both cost (position value) and heuristic (strategic importance).

        Returns:
            int: The position (0-8) where AI should move, or None if no moves available
        """

        # === STEP 1: IMMEDIATE WIN CHECK ===
        # Loop through all positions to find a winning move
        for i in range(9):
            # Check if position is empty
            if self.board[i] == '':
                # Temporarily place AI's mark (O)
                self.board[i] = 'O'

                # Check if this move wins the game
                if self.is_winner('O'):
                    # Remove temporary mark
                    self.board[i] = ''
                    # Return winning move (highest priority)
                    return i

                # Not a winning move, remove temporary mark
                self.board[i] = ''

        # === STEP 2: BLOCKING CHECK ===
        # Loop through all positions to find blocking moves
        for i in range(9):
            # Check if position is empty
            if self.board[i] == '':
                # Temporarily place player's mark (X)
                self.board[i] = 'X'

                # Check if player would win with this move
                if self.is_winner('X'):
                    # Remove temporary mark
                    self.board[i] = ''
                    # Must block this move
                    return i

                # Player wouldn't win, remove temporary mark
                self.board[i] = ''

        # === STEP 3: HEURISTIC SCORING ===
        # No immediate threats, so score each empty position

        # Create empty list to store (score, position) tuples
        scores = []

        # Define the heuristic values for each position
        # Index corresponds to board position (0-8)
        # These values represent strategic importance:
        # - Center (4): Most valuable at 4 points
        # - Corners (0,2,6,8): Second most valuable at 3 points
        # - Edges (1,3,5,7): Least valuable at 2 points
        position_value = [3, 2, 3, 2, 4, 2, 3, 2, 3]

        # Calculate score for each empty position
        for i in range(9):
            # Only consider empty positions
            if self.board[i] == '':
                # Get the heuristic score for this position
                score = position_value[i]

                # Add (score, position) tuple to our list
                # We store as tuple so we can sort by score
                scores.append((score, i))

        # === STEP 4: SELECT BEST MOVE ===
        # If we have any possible moves
        if scores:
            # Sort scores in descending order (highest score first)
            # reverse=True means sort from high to low
            scores.sort(reverse=True)

            # Return the position with the highest score
            # scores[0] is the tuple with highest score
            # scores[0][1] extracts just the position (second element of tuple)
            return scores[0][1]

    def is_winner(self, player):
        """
        Checks if the specified player has won the game.

        Parameters:
            player (str): Either 'X' or 'O'

        Returns:
            bool: True if the player has won, False otherwise

        Win conditions:
            - Three in a row horizontally
            - Three in a row vertically
            - Three in a row diagonally
        """

        # Define all possible winning combinations
        # Each inner list represents a winning line of 3 positions
        wins = [
            # Horizontal wins (rows)
            [0, 1, 2],  # Top row: positions 0, 1, 2
            [3, 4, 5],  # Middle row: positions 3, 4, 5
            [6, 7, 8],  # Bottom row: positions 6, 7, 8

            # Vertical wins (columns)
            [0, 3, 6],  # Left column: positions 0, 3, 6
            [1, 4, 7],  # Middle column: positions 1, 4, 7
            [2, 5, 8],  # Right column: positions 2, 5, 8

            # Diagonal wins
            [0, 4, 8],  # Top-left to bottom-right diagonal
            [2, 4, 6]   # Top-right to bottom-left diagonal
        ]

        # Check each possible winning combination
        for combo in wins:
            # all() returns True only if ALL positions in combo contain the player's mark
            # Example: if combo is [0,1,2] and player is 'X'
            #          checks if board[0]=='X' AND board[1]=='X' AND board[2]=='X'
            if all(self.board[i] == player for i in combo):
                # This player has won!
                return True

        # No winning combination found
        return False

    def check_end(self):
        """
        Checks if the game has ended (win, loss, or draw) and shows appropriate message.

        Returns:
            bool: True if game is over, False if game continues
        """

        # === CHECK FOR PLAYER WIN ===
        if self.is_winner('X'):
            # Set flag to prevent further moves
            self.game_over = True

            # Show victory popup with Yes/No buttons
            # Returns True if user clicks "Yes", False if "No"
            result = messagebox.askyesno("You Win!", 
                                        "Congratulations! 🎉\n\nRematch with same AI?")

            # If user wants rematch
            if result:
                self.rematch()  # Start new game with same AI

            return True  # Game is over

        # === CHECK FOR AI WIN ===
        if self.is_winner('O'):
            # Set flag to prevent further moves
            self.game_over = True

            # Show loss popup with algorithm name
            result = messagebox.askyesno("AI Wins", 
                                        f"AI ({self.algorithm}) won!\n\nRematch?")

            # If user wants rematch
            if result:
                self.rematch()  # Start new game with same AI

            return True  # Game is over

        # === CHECK FOR DRAW ===
        # If there are no empty positions left ('' not in board)
        if '' not in self.board:
            # Set flag to prevent further moves
            self.game_over = True

            # Show draw popup
            result = messagebox.askyesno("Draw", 
                                        "It's a tie!\n\nRematch?")

            # If user wants rematch
            if result:
                self.rematch()  # Start new game with same AI

            return True  # Game is over

        # Game continues
        return False

    def rematch(self):
        """
        Starts a new game while keeping the same AI algorithm selected.
        This is like a "quick restart" button.
        """
        # Reset the board to all empty positions
        self.board = ['' for _ in range(9)]

        # Reset the game over flag so players can make moves again
        self.game_over = False

        # Reset all buttons to their initial state
        for btn in self.buttons:
            # Clear the text (X or O)
            # Enable the button (state='normal')
            # Reset background color to white
            btn.config(text='', state='normal', bg='white')

    def reset(self):
        """
        Starts a completely new game.
        Same as rematch(), but semantically allows changing the algorithm.
        """
        # Reset the board to all empty positions
        self.board = ['' for _ in range(9)]

        # Reset the game over flag
        self.game_over = False

        # Reset all buttons to their initial state
        for btn in self.buttons:
            # Clear the text, enable button, reset color
            btn.config(text='', state='normal', bg='white')

    def run(self):
        """
        Starts the game by running the Tkinter event loop.
        This keeps the window open and responsive to user interactions.
        """
        # mainloop() is a blocking call that waits for user events
        # (button clicks, window closing, etc.)
        self.window.mainloop()


# === PROGRAM ENTRY POINT ===
# This block only runs if this file is executed directly (not imported)
if __name__ == "__main__":
    # Create a new instance of the game
    game = SimpleTicTacToe()

    # Start the game (opens window and waits for user input)
    game.run()
