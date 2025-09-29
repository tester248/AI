class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
    
    def print_board(self):
        for i in range(0, 9, 3):
            print(f" {self.board[i]} || {self.board[i+1]} || {self.board[i+2]} ")
            if i < 6:
                print("=============")
    
    def is_winner(self, player):
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  #rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  #columns
            [0, 4, 8], [2, 4, 6]              #diagonals
        ]
        return any(all(self.board[i] == player for i in pattern) for pattern in win_patterns)
    
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
            score = minimax_alpha_beta(game, 9, float('-inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move
        else:
            score = minimax_alpha_beta(game, 9, float('-inf'), float('inf'), True)
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
            print("X wins!")
            break
        elif game.is_winner('O'):
            print("O wins!")
            break
        elif game.is_board_full():
            print("It's a tie!")
            break
        
        if game.current_player == 'X':
            try:
                move = int(input(f"Player {game.current_player}, enter position (0-8): "))
                if move < 0 or move > 8 or not game.make_move(move, game.current_player):
                    print("Invalid move! Try again.")
                    continue
            except ValueError:
                print("Please enter a number between 0-8.")
                continue
        else:
            print("AI is thinking...")
            move = get_best_move(game, game.current_player)
            game.make_move(move, game.current_player)
            print(f"AI chose position {move}")
        game.current_player = 'O' if game.current_player == 'X' else 'X'

if __name__ == "__main__":
    main()