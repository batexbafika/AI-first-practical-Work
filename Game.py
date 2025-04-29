import tkinter as tk
from tkinter import messagebox, ttk
import random

class DivisionGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Division Game - Computer vs Player")
        self.root.geometry("650x700")
        self.root.configure(bg="#f5f5f5")
        
        # Apply consistent theme and font
        self.default_font = ("Segoe UI", 11)
        self.header_font = ("Segoe UI", 18, "bold")
        self.button_font = ("Segoe UI", 12, "bold")
        
        self.algorithm_choice = tk.StringVar()
        self.starting_number = tk.IntVar()

        # Set default values
        self.algorithm_choice.set("minimax")

        self.setup_start_screen()

    def setup_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(main_frame, text="Division Game", font=("Segoe UI", 28, "bold"), 
                      bg="#f5f5f5", fg="#2c3e50")
        title.pack(pady=20)

        # Game description
        description = tk.Label(main_frame, text="Divide numbers and score points strategically!", 
                           font=self.default_font, bg="#f5f5f5", fg="#7f8c8d")
        description.pack(pady=5)

        # Algorithm selection section with styled frame
        algo_frame = tk.LabelFrame(main_frame, text="Computer Algorithm", 
                               font=("Segoe UI", 12, "bold"), bg="#f5f5f5", 
                               fg="#2c3e50", padx=15, pady=15)
        algo_frame.pack(fill=tk.X, pady=15)

        tk.Radiobutton(algo_frame, text="Minimax", variable=self.algorithm_choice, 
                    value="minimax", bg="#f5f5f5", font=self.default_font).pack(anchor=tk.W)
        tk.Radiobutton(algo_frame, text="Alpha-Beta Pruning", variable=self.algorithm_choice, 
                    value="alphabeta", bg="#f5f5f5", font=self.default_font).pack(anchor=tk.W)

        # Number selection section with styled frame and better visualization
        self.generated_numbers = self.generate_numbers()
        number_frame = tk.LabelFrame(main_frame, text="Choose a starting number", 
                                 font=("Segoe UI", 12, "bold"), bg="#f5f5f5", 
                                 fg="#2c3e50", padx=15, pady=15)
        number_frame.pack(fill=tk.X, pady=15)

        # Display numbers in a grid for better visualization
        for i, num in enumerate(self.generated_numbers):
            tk.Radiobutton(number_frame, text=f"{num:,}", variable=self.starting_number, 
                        value=num, bg="#f5f5f5", font=self.default_font).grid(
                row=i//2, column=i%2, sticky=tk.W, padx=10, pady=5)

        # Start button with modern styling
        start_button = tk.Button(main_frame, text="Start Game", command=self.start_game, 
                             font=self.button_font, bg="#3498db", fg="white", 
                             padx=25, pady=12, relief=tk.FLAT,
                             activebackground="#2980b9", activeforeground="white",
                             cursor="hand2")
        start_button.pack(pady=25)

    def generate_numbers(self):
        numbers = []
        while len(numbers) < 6:  # Increased to 6 numbers for better options
            num = random.randint(10000, 20000)
            if num % 6 == 0:  # Ensure it's divisible by both 2 and 3
                numbers.append(num)
        return numbers

    def start_game(self):
        if self.algorithm_choice.get() == "":
            messagebox.showwarning("Warning", "Please select an algorithm.")
            return
        if self.starting_number.get() == 0:
            messagebox.showwarning("Warning", "Please select a starting number.")
            return
        self.setup_game_screen()

    def setup_game_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.current_number = self.starting_number.get()
        self.player_score = 0
        self.computer_score = 0
        self.bank = 0
        self.is_player_turn = True
        self.move_history = []  # Track move history for better logging

        # Create a main container with padding
        main_container = tk.Frame(self.root, bg="#f5f5f5", padx=25, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Top section: Header and Status
        top_frame = tk.Frame(main_container, bg="#f5f5f5")
        top_frame.pack(fill=tk.X, pady=5)

        # Game title and algorithm info
        header = tk.Label(top_frame, text="Division Game", font=self.header_font, 
                      bg="#f5f5f5", fg="#2c3e50")
        header.pack(side=tk.LEFT)
        
        algorithm_info = tk.Label(top_frame, 
                              text=f"Algorithm: {self.algorithm_choice.get().title()}", 
                              font=self.default_font, bg="#f5f5f5", fg="#7f8c8d")
        algorithm_info.pack(side=tk.RIGHT)

        # Current number display with modern card design
        number_card = tk.Frame(main_container, bg="white", padx=20, pady=20, 
                           relief=tk.RAISED, bd=1)
        number_card.pack(fill=tk.X, pady=15)

        self.status_label = tk.Label(number_card, text="Your Turn", 
                                 font=("Segoe UI", 14, "bold"), bg="white", 
                                 fg="#3498db")
        self.status_label.pack()

        self.number_label = tk.Label(number_card, 
                                 text=f"Current Number: {self.current_number:,}", 
                                 font=("Segoe UI", 24, "bold"), bg="white", 
                                 fg="#2c3e50", pady=10)
        self.number_label.pack()

        # Scores section with modern card design
        score_card = tk.Frame(main_container, bg="white", padx=15, pady=15, 
                          relief=tk.RAISED, bd=1)
        score_card.pack(fill=tk.X, pady=15)

        # Create a grid for scores with better visualization
        score_grid = tk.Frame(score_card, bg="white")
        score_grid.pack(fill=tk.X)

        # Player score
        player_label = tk.Label(score_grid, text="Player", font=("Segoe UI", 12, "bold"), 
                            bg="white", fg="#3498db")
        player_label.grid(row=0, column=0, padx=20, pady=5)
        
        self.player_score_label = tk.Label(score_grid, text="0", 
                                       font=("Segoe UI", 20, "bold"), 
                                       bg="white", fg="#3498db")
        self.player_score_label.grid(row=1, column=0, padx=20, pady=0)

        # VS separator
        vs_label = tk.Label(score_grid, text="VS", font=("Segoe UI", 12), 
                        bg="white", fg="#7f8c8d")
        vs_label.grid(row=0, column=1, rowspan=2, padx=30)

        # Computer score
        computer_label = tk.Label(score_grid, text="Computer", 
                              font=("Segoe UI", 12, "bold"), 
                              bg="white", fg="#e74c3c")
        computer_label.grid(row=0, column=2, padx=20, pady=5)
        
        self.computer_score_label = tk.Label(score_grid, text="0", 
                                         font=("Segoe UI", 20, "bold"), 
                                         bg="white", fg="#e74c3c")
        self.computer_score_label.grid(row=1, column=2, padx=20, pady=0)

        # Bank display
        bank_frame = tk.Frame(score_card, bg="white", pady=10)
        bank_frame.pack(fill=tk.X)
        
        bank_label = tk.Label(bank_frame, text="Bank:", 
                          font=("Segoe UI", 12), bg="white", fg="#7f8c8d")
        bank_label.pack(side=tk.LEFT, padx=20)
        
        self.bank_value = tk.Label(bank_frame, text="0", 
                               font=("Segoe UI", 14, "bold"), 
                               bg="white", fg="#f39c12")
        self.bank_value.pack(side=tk.LEFT)

        # Move buttons with modern styling
        button_frame = tk.Frame(main_container, bg="#f5f5f5", pady=10)
        button_frame.pack()

        self.btn_div2 = tk.Button(button_frame, text="Divide by 2", width=15, height=2,
                             command=lambda: self.play_move(2), bg="#3498db", fg="white",
                             font=self.button_font, relief=tk.FLAT,
                             activebackground="#2980b9", activeforeground="white")
        
        self.btn_div3 = tk.Button(button_frame, text="Divide by 3", width=15, height=2,
                             command=lambda: self.play_move(3), bg="#e74c3c", fg="white",
                             font=self.button_font, relief=tk.FLAT,
                             activebackground="#c0392b", activeforeground="white")

        self.btn_div2.grid(row=0, column=0, padx=10)
        self.btn_div3.grid(row=0, column=1, padx=10)

        # Winner announcement section
        self.winner_label = tk.Label(main_container, text="", 
                                 font=("Segoe UI", 16, "bold"), 
                                 bg="#f5f5f5", fg="#27ae60")
        self.winner_label.pack(pady=10)

        # Enhanced move log with a styled treeview instead of text box
        log_frame = tk.LabelFrame(main_container, text="Game Moves", 
                              font=("Segoe UI", 12, "bold"), bg="#f5f5f5", 
                              fg="#2c3e50", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create treeview with columns for each piece of information
        self.tree = ttk.Treeview(log_frame, columns=("player", "move", "before", "after", "points", "target"),
                             show="headings", height=7)
        
        # Configure column headings
        self.tree.heading("player", text="Player")
        self.tree.heading("move", text="Move")
        self.tree.heading("before", text="Before")
        self.tree.heading("after", text="After")
        self.tree.heading("points", text="Points")
        self.tree.heading("target", text="To")
        
        # Configure column widths
        self.tree.column("player", width=80, anchor=tk.CENTER)
        self.tree.column("move", width=80, anchor=tk.CENTER)
        self.tree.column("before", width=100, anchor=tk.CENTER)
        self.tree.column("after", width=100, anchor=tk.CENTER)
        self.tree.column("points", width=60, anchor=tk.CENTER)
        self.tree.column("target", width=80, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bank action log separately
        self.bank_log = tk.Label(main_container, text="", font=self.default_font, 
                             bg="#f5f5f5", fg="#f39c12")
        self.bank_log.pack(pady=5)

        # Buttons container for both reset and new game buttons
        buttons_container = tk.Frame(main_container, bg="#f5f5f5")
        buttons_container.pack(pady=10)
        
        # End game (reset) button
        self.reset_button = tk.Button(buttons_container, text="End Game", 
                                  command=self.setup_start_screen,
                                  font=self.default_font, bg="#9b59b6", fg="white", 
                                  relief=tk.FLAT, width=10, padx=5,
                                  activebackground="#8e44ad", activeforeground="white")
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # New game button (always active)
        self.new_game_button = tk.Button(buttons_container, text="New Game", 
                                     command=self.start_new_game,
                                     font=self.default_font, bg="#2ecc71", fg="white", 
                                     relief=tk.FLAT, width=10, padx=5,
                                     activebackground="#27ae60", activeforeground="white")
        self.new_game_button.pack(side=tk.LEFT, padx=5)

        # Apply custom styles to the treeview
        style = ttk.Style()
        style.configure("Treeview", 
                     background="white", 
                     foreground="#2c3e50", 
                     rowheight=25, 
                     fieldbackground="white",
                     font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                     font=("Segoe UI", 10, "bold"), 
                     background="#f0f0f0",
                     foreground="#2c3e50")
        style.map("Treeview", 
               background=[("selected", "#3498db")],
               foreground=[("selected", "white")])

        self.update_game_screen()
    
    def start_new_game(self):
        # Confirm if a game is in progress
        if hasattr(self, 'current_number') and self.current_number > 10 and len(self.get_valid_moves(self.current_number)) > 0:
            if messagebox.askyesno("New Game", "Are you sure you want to start a new game? Current game progress will be lost."):
                # Generate new numbers and show the start screen
                self.algorithm_choice.set(self.algorithm_choice.get())  # Keep current algorithm selection
                self.generated_numbers = self.generate_numbers()  # Generate new numbers
                self.setup_start_screen()
        else:
            # Just go back to start screen if no game in progress or game is over
            self.setup_start_screen()

    def log_action(self, who, move, before, after, score_change, target):
        # Insert into treeview with formatted values
        self.tree.insert("", "end", values=(
            who, 
            f"÷ {move}", 
            f"{before:,}", 
            f"{after:,}", 
            f"+{score_change}", 
            target
        ))
        
        # Keep focus on the last item
        self.tree.yview_moveto(1)
        
        # Store in move history
        self.move_history.append({
            "who": who,
            "move": move,
            "before": before,
            "after": after,
            "score_change": score_change,
            "target": target
        })

    def log_bank_action(self, amount):
        """Log bank point addition to the tree view"""
        self.tree.insert("", "end", values=(
            "Bank", 
            "0/5", 
            "", 
            "", 
            f"+{amount}", 
            "Bank"
        ))
        self.tree.yview_moveto(1)

    def update_game_screen(self):
        # Update number display with thousands separator
        self.number_label.config(text=f"Current Number: {self.current_number:,}")
        
        # Update score labels
        self.player_score_label.config(text=str(self.player_score))
        self.computer_score_label.config(text=str(self.computer_score))
        self.bank_value.config(text=str(self.bank))
        
        # Update turn status
        if self.is_player_turn:
            self.status_label.config(text="Your Turn", fg="#3498db")
        else:
            self.status_label.config(text="Computer is thinking...", fg="#e74c3c")

        # Check for game end
        if self.current_number <= 10 or not self.get_valid_moves(self.current_number):
            # Game is ending
            if self.is_player_turn:
                # Player's turn ended the game, add bank to player's score
                if self.bank > 0:
                    self.tree.insert("", "end", values=(
                        "Player", 
                        "Bank", 
                        "", 
                        "", 
                        f"+{self.bank}", 
                        "Player"
                    ))
                self.player_score += self.bank
                self.player_score_label.config(text=str(self.player_score))
            else:
                # Computer's turn ended the game, add bank to computer's score
                if self.bank > 0:
                    self.tree.insert("", "end", values=(
                        "Computer", 
                        "Bank", 
                        "", 
                        "", 
                        f"+{self.bank}", 
                        "Computer"
                    ))
                self.computer_score += self.bank
                self.computer_score_label.config(text=str(self.computer_score))

            # Reset bank
            self.bank = 0
            self.bank_value.config(text="0")

            # Determine winner
            if self.player_score > self.computer_score:
                winner_text = "🎉 YOU WIN!"
                winner_color = "#27ae60"
            elif self.computer_score > self.player_score:
                winner_text = "💻 COMPUTER WINS!"
                winner_color = "#e74c3c"
            else:
                winner_text = "🤝 It's a DRAW!"
                winner_color = "#f39c12"

            self.status_label.config(text="Game Over", fg="#7f8c8d")
            self.winner_label.config(text=winner_text, fg=winner_color)
            self.btn_div2.config(state="disabled")
            self.btn_div3.config(state="disabled")

    def get_valid_moves(self, number):
        return [x for x in (2, 3) if number % x == 0]

    def play_move(self, move):
        if move not in self.get_valid_moves(self.current_number):
            return

        before = self.current_number
        self.current_number //= move
        after = self.current_number

        # Scoring logic
        if move == 2:
            if self.is_player_turn:
                self.computer_score += 2
                self.log_action("Player", move, before, after, 2, "Computer")
            else:
                self.player_score += 2
                self.log_action("Computer", move, before, after, 2, "Player")
        elif move == 3:
            if self.is_player_turn:
                self.player_score += 3
                self.log_action("Player", move, before, after, 3, "Player")
            else:
                self.computer_score += 3
                self.log_action("Computer", move, before, after, 3, "Computer")

        # Check for bank increase (number ends with 0 or 5)
        if str(self.current_number)[-1] in ['0', '5']:
            self.bank += 1
            self.bank_log.config(text=f"Number ends with 0 or 5: Bank +1! (Total: {self.bank})")
            self.log_bank_action(1)
            self.bank_value.config(text=str(self.bank))
        else:
            self.bank_log.config(text="")

        self.is_player_turn = not self.is_player_turn
        self.update_game_screen()

        # Computer's turn
        if not self.is_player_turn and self.current_number > 10 and self.get_valid_moves(self.current_number):
            self.root.after(1000, self.computer_move)

    def computer_move(self):
        move = self.select_computer_move()
        self.play_move(move)

    def select_computer_move(self):
        state = {
            'number': self.current_number,
            'player_score': self.player_score,
            'computer_score': self.computer_score,
            'bank': self.bank,
            'is_computer_turn': True
        }

        depth = 5
        if self.algorithm_choice.get() == "minimax":
            _, move = self.minimax(state, depth, True)
        else:
            _, move = self.alpha_beta(state, depth, float('-inf'), float('inf'), True)
        return move

    def evaluate_state(self, state):
        return state['computer_score'] - state['player_score']

    def apply_state_move(self, state, move):
        new_state = state.copy()
        new_state['number'] //= move

        if move == 2:
            if new_state['is_computer_turn']:
                new_state['player_score'] += 2
            else:
                new_state['computer_score'] += 2
        elif move == 3:
            if new_state['is_computer_turn']:
                new_state['computer_score'] += 3
            else:
                new_state['player_score'] += 3

        # Check if result ends with 0 or 5 and update bank
        if str(new_state['number'])[-1] in ['0', '5']:
            new_state['bank'] += 1

        # Check if game ends with this move
        if new_state['number'] <= 10:
            if new_state['is_computer_turn']:
                new_state['computer_score'] += new_state['bank']
            else:
                new_state['player_score'] += new_state['bank']
            new_state['bank'] = 0  # Reset bank after transferring
            new_state['game_over'] = True
        else:
            new_state['game_over'] = False

        new_state['is_computer_turn'] = not new_state['is_computer_turn']
        return new_state

    def minimax(self, state, depth, maximizing):
        if state['number'] <= 10 or depth == 0:
            return self.evaluate_state(state), None

        moves = self.get_valid_moves(state['number'])
        if not moves:
            return self.evaluate_state(state), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_state = self.apply_state_move(state, move)
                eval, _ = self.minimax(new_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_state = self.apply_state_move(state, move)
                eval, _ = self.minimax(new_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def alpha_beta(self, state, depth, alpha, beta, maximizing):
        if state['number'] <= 10 or depth == 0:
            return self.evaluate_state(state), None

        moves = self.get_valid_moves(state['number'])
        if not moves:
            return self.evaluate_state(state), None

        best_move = None
        if maximizing:
            value = float('-inf')
            for move in moves:
                new_state = self.apply_state_move(state, move)
                eval, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, False)
                if eval > value:
                    value = eval
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = float('inf')
            for move in moves:
                new_state = self.apply_state_move(state, move)
                eval, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, True)
                if eval < value:
                    value = eval
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move

       
if __name__ == "__main__":
    root = tk.Tk()
    app = DivisionGameGUI(root)
    root.mainloop()