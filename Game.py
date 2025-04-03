import tkinter as tk
from tkinter import messagebox, ttk
import random

# Node with records for each move in the game
class MoveNode:
    def _init_(self, who, move, before, after, score_change, target):
        self.who = who
        self.move = move
        self.before = before
        self.after = after
        self.score_change = score_change
        self.target = target
        self.next = None

# Linked list to track all game moves
class MoveLinkedList:
    def _init_(self):
        self.head = None
        self.tail = None
        self.length = 0

    def add_move(self, who, move, before, after, score_change, target):
        new_node = MoveNode(who, move, before, after, score_change, target)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def get_all_moves(self):
        current = self.head
        moves = []
        while current:
            moves.append({
                "who": current.who,
                "move": current.move,
                "before": current.before,
                "after": current.after,
                "score_change": current.score_change,
                "target": current.target
            })
            current = current.next
        return moves
#Our graphic User interface GUI for the game
class DivisionGameGUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Division Game - Computer vs Player")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")

        self.default_font = ("Segoe UI", 11)
        self.header_font = ("Segoe UI", 20, "bold")
        self.button_font = ("Segoe UI", 12, "bold")

        self.algorithm_choice = tk.StringVar(value="minimax")
        self.starting_number = tk.IntVar()

        self.setup_start_screen()

    def setup_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Division Game", font=("Segoe UI", 28, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=(0, 10))
        tk.Label(main_frame, text="Divide numbers and score points strategically!", font=self.default_font, bg="#f5f5f5", fg="#7f8c8d").pack(pady=(0, 20))

        algo_frame = tk.LabelFrame(main_frame, text="Computer Algorithm", font=("Segoe UI", 12, "bold"), bg="#f5f5f5", fg="#2c3e50", padx=15, pady=15)
        algo_frame.pack(fill=tk.X, pady=15)

        tk.Radiobutton(algo_frame, text="Minimax", variable=self.algorithm_choice, value="minimax", bg="#f5f5f5", font=self.default_font).pack(anchor=tk.W)
        tk.Radiobutton(algo_frame, text="Alpha-Beta Pruning", variable=self.algorithm_choice, value="alphabeta", bg="#f5f5f5", font=self.default_font).pack(anchor=tk.W)

        self.generated_numbers = self.generate_numbers()
        number_frame = tk.LabelFrame(main_frame, text="Choose a starting number", font=("Segoe UI", 12, "bold"), bg="#f5f5f5", fg="#2c3e50", padx=15, pady=15)
        number_frame.pack(fill=tk.X, pady=15)

        for i, num in enumerate(self.generated_numbers):
            tk.Radiobutton(number_frame, text=f"{num:,}", variable=self.starting_number, value=num, bg="#f5f5f5", font=self.default_font).grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=5)

        tk.Button(main_frame, text="Start Game", command=self.start_game, font=self.button_font, bg="#3498db", fg="white", padx=25, pady=12, relief=tk.FLAT, activebackground="#2980b9", activeforeground="white", cursor="hand2").pack(pady=25)

#Code to generate random numbers between 10000 and 20000
    def generate_numbers(self):
        numbers = []
        while len(numbers) < 6:
            num = random.randint(10000, 20000)
            if num % 6 == 0:
                numbers.append(num)
        return numbers

    def start_game(self):
        if self.starting_number.get() == 0:
            messagebox.showwarning("Warning", "Please select a starting number.")
            return

        self.current_number = self.starting_number.get()
        self.player_score = 0
        self.computer_score = 0
        self.bank = 0
        self.is_player_turn = True
        self.move_history = MoveLinkedList()
        self.setup_game_screen()

    def setup_game_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Division Game", font=self.header_font, bg="#f5f5f5", fg="#2c3e50").pack(pady=(10, 0))

        self.status_label = tk.Label(self.root, text="Your Turn", font=("Segoe UI", 14), bg="#f5f5f5", fg="#3498db")
        self.status_label.pack()

        self.number_label = tk.Label(self.root, text=f"Current Number: {self.current_number:,}", font=("Segoe UI", 24, "bold"), bg="#f5f5f5", fg="#2c3e50")
        self.number_label.pack(pady=(0, 10))

        score_frame = tk.Frame(self.root, bg="#f5f5f5")
        score_frame.pack(pady=5)

        self.player_score_label = tk.Label(score_frame, text=f"Player: {self.player_score}", font=self.default_font, bg="#f5f5f5", fg="#3498db")
        self.player_score_label.pack(side=tk.LEFT, padx=20)

        self.computer_score_label = tk.Label(score_frame, text=f"Computer: {self.computer_score}", font=self.default_font, bg="#f5f5f5", fg="#e74c3c")
        self.computer_score_label.pack(side=tk.LEFT, padx=20)

        self.bank_value = tk.Label(score_frame, text=f"Bank: {self.bank}", font=self.default_font, bg="#f5f5f5", fg="#f39c12")
        self.bank_value.pack(side=tk.LEFT, padx=20)

        btn_frame = tk.Frame(self.root, bg="#f5f5f5")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Divide by 2", command=lambda: self.play_move(2), font=self.button_font, bg="#3498db", fg="white", padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Divide by 3", command=lambda: self.play_move(3), font=self.button_font, bg="#e74c3c", fg="white", padx=20, pady=10).pack(side=tk.LEFT, padx=10)

        self.winner_label = tk.Label(self.root, text="", font=("Segoe UI", 16, "bold"), bg="#f5f5f5")
        self.winner_label.pack(pady=10)

        log_frame = tk.LabelFrame(self.root, text="Game Moves", font=("Segoe UI", 12, "bold"), bg="#f5f5f5", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        self.tree = ttk.Treeview(log_frame, columns=("player", "move", "before", "after", "points", "target"), show="headings", height=6)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=self.default_font, rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.update_game_screen()
#Game logic for the player and computer moves
    def play_move(self, move):
        if self.current_number % move != 0:
            return

        before = self.current_number
        self.current_number //= move
        after = self.current_number

        if move == 2:
            if self.is_player_turn:
                self.computer_score += 2
                self.log_action("Player", move, before, after, 2, "Computer")
            else:
                self.player_score += 2
                self.log_action("Computer", move, before, after, 2, "Player")
        else:
            if self.is_player_turn:
                self.player_score += 3
                self.log_action("Player", move, before, after, 3, "Player")
            else:
                self.computer_score += 3
                self.log_action("Computer", move, before, after, 3, "Computer")

        if str(self.current_number)[-1] in ['0', '5']:
            self.bank += 1

        self.is_player_turn = not self.is_player_turn
        self.update_game_screen()

        if not self.is_player_turn and self.current_number > 10 and self.get_valid_moves(self.current_number):
            self.root.after(1000, self.computer_move)
        elif self.current_number <= 10 or not self.get_valid_moves(self.current_number):
            self.end_game()
#This line of code checks if the number is divisible by 2 or 3 and returns a list of valid moves
    def get_valid_moves(self, number):
        return [x for x in (2, 3) if number % x == 0]

    def computer_move(self):
        state = {
            'number': self.current_number,
            'player_score': self.player_score,
            'computer_score': self.computer_score,
            'bank': self.bank,
            'is_computer_turn': True
        }
        _, move = self.minimax(state, 5, True) if self.algorithm_choice.get() == "minimax" else self.alpha_beta(state, 5, float('-inf'), float('inf'), True)
        if move:
            self.play_move(move)

#This is the minimax algorithm that evaluates the game state and returns the best move for the computer
    # The minimax algorithm recursively explores all possible moves and their outcomes
    def minimax(self, state, depth, maximizing):
        if state['number'] <= 10 or depth == 0:
            return self.evaluate_state(state), None

        moves = self.get_valid_moves(state['number'])
        best_move = None

        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_state = self.apply_state_move(state, move)
                eval, _ = self.minimax(new_state, depth-1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_state = self.apply_state_move(state, move)
                eval, _ = self.minimax(new_state, depth-1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move
        
#This is the alpha-beta pruning algorithm that optimizes the minimax algorithm by eliminating branches that won't affect the final decision
    # The alpha-beta pruning algorithm reduces the number of nodes evaluated in the minimax algorithm
    def alpha_beta(self, state, depth, alpha, beta, maximizing):
        if state['number'] <= 10 or depth == 0:
            return self.evaluate_state(state), None

        moves = self.get_valid_moves(state['number'])
        best_move = None

        if maximizing:
            value = float('-inf')
            for move in moves:
                new_state = self.apply_state_move(state, move)
                eval, _ = self.alpha_beta(new_state, depth-1, alpha, beta, False)
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
                eval, _ = self.alpha_beta(new_state, depth-1, alpha, beta, True)
                if eval < value:
                    value = eval
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move
        
#Heuristic evaluation function to determine the value of a game state
    # The heuristic function evaluates the game state based on the difference in scores
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
        else:
            if new_state['is_computer_turn']:
                new_state['computer_score'] += 3
            else:
                new_state['player_score'] += 3

        if str(new_state['number'])[-1] in ['0', '5']:
            new_state['bank'] += 1

        if new_state['number'] <= 10:
            if new_state['is_computer_turn']:
                new_state['computer_score'] += new_state['bank']
            else:
                new_state['player_score'] += new_state['bank']
            new_state['bank'] = 0

        new_state['is_computer_turn'] = not new_state['is_computer_turn']
        return new_state

    def log_action(self, who, move, before, after, score_change, target):
        self.tree.insert("", "end", values=(who, f"+{move}", f"{before:,}", f"{after:,}", f"+{score_change}", target))
        self.move_history.add_move(who, move, before, after, score_change, target)

    def update_game_screen(self):
        self.number_label.config(text=f"Current Number: {self.current_number:,}")
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        self.bank_value.config(text=f"Bank: {self.bank}")
        self.status_label.config(text="Your Turn" if self.is_player_turn else "Computer is thinking...")

    def end_game(self):
        if self.is_player_turn:
            self.player_score += self.bank
        else:
            self.computer_score += self.bank

        self.bank = 0
        self.update_game_screen()

        if self.player_score > self.computer_score:
            result = "🎉 YOU WIN!"
            color = "#27ae60"
        elif self.player_score < self.computer_score:
            result = "💻 COMPUTER WINS!"
            color = "#e74c3c"
        else:
            result = "🤝 DRAW!"
            color = "#f39c12"

        self.status_label.config(text="Game Over", fg="#7f8c8d")
        self.winner_label.config(text=result, fg=color)
        
#The main rntry point of the program
# The main function initializes the GUI and starts the game loop
if _name_ == "_main_":
    root = tk.Tk()
    app = DivisionGameGUI(root)
    root.mainloop()