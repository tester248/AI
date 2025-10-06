class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(25)]  # 5x5 board
        self.current_player = 'X'
    
    def print_board(self):
        for i in range(0, 25, 5):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} | {self.board[i+3]} | {self.board[i+4]} ")
            if i < 20:
                print("——————————————————")
    
    def is_winner(self, player):
        # Horizontal wins
        for row in range(5):
            if all(self.board[row * 5 + col] == player for col in range(5)):
                return True
        
        # Vertical wins
        for col in range(5):
            if all(self.board[row * 5 + col] == player for row in range(5)):
                return True
        
        # Diagonal wins
        if all(self.board[i * 5 + i] == player for i in range(5)):  # Top-left to bottom-right
            return True
        if all(self.board[i * 5 + (4 - i)] == player for i in range(5)):  # Top-right to bottom-left
            return True
        
        return False
    
    def is_board_full(self):
        return ' ' not in self.board
    
    def get_available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == ' ']
    
    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False
    
    def undo_move(self, position):
        self.board[position] = ' '
    
    def evaluate(self):
        if self.is_winner('X'):
            return 1
        elif self.is_winner('O'):
            return -1
        else:
            return 0

def minimax_alpha_beta(game, depth, alpha, beta, maximizing_player):
    if game.is_winner('X'):
        return 1
    if game.is_winner('O'):
        return -1
    if game.is_board_full() or depth == 0:
        return 0
    if maximizing_player:
        max_eval = float('-inf')
        for move in game.get_available_moves():
            game.make_move(move, 'X')
            eval_score = minimax_alpha_beta(game, depth - 1, alpha, beta, False)
            game.undo_move(move)         
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.get_available_moves():
            game.make_move(move, 'O')
            eval_score = minimax_alpha_beta(game, depth - 1, alpha, beta, True)
            game.undo_move(move)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        
        return min_eval

def get_best_move(game, player):
    best_score = float('-inf') if player == 'X' else float('inf')
    best_move = None
    for move in game.get_available_moves():
        game.make_move(move, player)
        if player == 'X':
            score = minimax_alpha_beta(game, 6, float('-inf'), float('inf'), False)  # Reduced depth for 5x5
            if score > best_score:
                best_score = score
                best_move = move
        else:
            score = minimax_alpha_beta(game, 6, float('-inf'), float('inf'), True)  # Reduced depth for 5x5
            if score < best_score:
                best_score = score
                best_move = move
        
        game.undo_move(move)
    return best_move

def main():
    game = TicTacToe()
    
    while True:
        game.print_board()
        
        if game.is_winner('X'):
            print("X wins! (You Win!)")
            break
        elif game.is_winner('O'):
            print("O wins! (AI Won.)")
            break
        elif game.is_board_full():
            print("It's a tie!")
            break
        
        if game.current_player == 'X':
            try:
                move = int(input(f"Player {game.current_player}, enter position (0-24): "))  # Updated range
                if move < 0 or move > 24 or not game.make_move(move, game.current_player):  # Updated validation
                    print("Invalid move! Try again.")
                    continue
            except ValueError:
                print("Please enter a number between 0-24.")  # Updated message
                continue
        else:
            print("AI is thinking...")
            move = get_best_move(game, game.current_player)
            game.make_move(move, game.current_player)
            print(f"AI chose position {move}")
        game.current_player = 'O' if game.current_player == 'X' else 'X'

if __name__ == "__main__":
    main()