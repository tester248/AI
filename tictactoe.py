class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board as 1D array
        self.current_player = 'X'
    
    def print_board(self):
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("-----------")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("-----------")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print()
    
    def make_move(self, position, player):
        """Make a move and return new board state"""
        if self.board[position] == ' ':
            new_board = self.board.copy()
            new_board[position] = player
            return new_board
        return None
    
    def is_winner(self, board, player):
        """Check if player has won"""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        return any(all(board[i] == player for i in pattern) for pattern in win_patterns)
    
    def is_board_full(self, board):
        """Check if board is full"""
        return ' ' not in board
    
    def is_terminal(self, board):
        """Check if game is over"""
        return self.is_winner(board, 'X') or self.is_winner(board, 'O') or self.is_board_full(board)
    
    def evaluate(self, board):
        """Evaluate board position"""
        if self.is_winner(board, 'X'):
            return 1  # X wins (maximizing player)
        elif self.is_winner(board, 'O'):
            return -1  # O wins (minimizing player)
        else:
            return 0  # Draw
    
    def get_available_moves(self, board):
        """Get list of available positions"""
        return [i for i in range(9) if board[i] == ' ']
    
    def alpha_beta_pruning(self, board, depth, alpha, beta, maximizing_player):
        """Alpha-beta pruning algorithm for tic-tac-toe"""
        if self.is_terminal(board):
            return self.evaluate(board)
        
        if maximizing_player:  # X's turn
            max_eval = float('-inf')
            for move in self.get_available_moves(board):
                new_board = board.copy()
                new_board[move] = 'X'
                eval_score = self.alpha_beta_pruning(new_board, depth + 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
                    
            return max_eval
        else:  # O's turn
            min_eval = float('inf')
            for move in self.get_available_moves(board):
                new_board = board.copy()
                new_board[move] = 'O'
                eval_score = self.alpha_beta_pruning(new_board, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
                    
            return min_eval
    
    def get_best_move(self, board, player):
        """Get the best move using alpha-beta pruning"""
        best_move = -1
        if player == 'X':  # Maximizing player
            best_value = float('-inf')
            for move in self.get_available_moves(board):
                new_board = board.copy()
                new_board[move] = 'X'
                move_value = self.alpha_beta_pruning(new_board, 0, float('-inf'), float('inf'), False)
                if move_value > best_value:
                    best_value = move_value
                    best_move = move
        else:  # Minimizing player
            best_value = float('inf')
            for move in self.get_available_moves(board):
                new_board = board.copy()
                new_board[move] = 'O'
                move_value = self.alpha_beta_pruning(new_board, 0, float('-inf'), float('inf'), True)
                if move_value < best_value:
                    best_value = move_value
                    best_move = move
        
        return best_move
    
    def play_game(self):
        """Main game loop"""
        print("Tic-Tac-Toe with AI!")
        print("Positions are numbered 0-8:")
        print(" 0 | 1 | 2 ")
        print("-----------")
        print(" 3 | 4 | 5 ")
        print("-----------")
        print(" 6 | 7 | 8 ")
        print()
        
        while not self.is_terminal(self.board):
            self.print_board()
            
            if self.current_player == 'X':
                # Human player
                try:
                    move = int(input(f"Player {self.current_player}, enter position (0-8): "))
                    if 0 <= move <= 8 and self.board[move] == ' ':
                        self.board[move] = self.current_player
                    else:
                        print("Invalid move! Try again.")
                        continue
                except ValueError:
                    print("Please enter a number!")
                    continue
            else:
                # AI player
                print("AI is thinking...")
                move = self.get_best_move(self.board, self.current_player)
                self.board[move] = self.current_player
                print(f"AI chose position {move}")
            
            # Switch players
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        # Game over
        self.print_board()
        if self.is_winner(self.board, 'X'):
            print("X wins!")
        elif self.is_winner(self.board, 'O'):
            print("O wins!")
        else:
            print("It's a draw!")

# Run the game
if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()