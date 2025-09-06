import heapq

# Define goal state as a global constant
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def manhattan_distance(board):
    distance = 0
    for i in range(9):
        if board[i] != 0:
            current_row, current_col = divmod(i, 3)
            goal_pos = GOAL_STATE.index(board[i])
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def count_inversions(board):
    inversions = 0 
    # Get positions of each number in both current and goal states (excluding 0)
    current_positions = {}
    goal_positions = {}
    
    for i in range(9):
        if board[i] != 0:
            current_positions[board[i]] = i
        if GOAL_STATE[i] != 0:
            goal_positions[GOAL_STATE[i]] = i
    
    numbers = [x for x in GOAL_STATE if x != 0]
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            num1, num2 = numbers[i], numbers[j]
            if current_positions[num1] > current_positions[num2]:
                inversions += 1
    
    return inversions

def is_solvable(board):
    board_inversions = count_inversions(board)
    goal_inversions = count_inversions(GOAL_STATE)
    return board_inversions % 2 == goal_inversions % 2

def get_neighbors(board):
    neighbors = []
    blank_pos = board.index(0)
    row, col = divmod(blank_pos, 3)
    
    # Define possible moves: (direction, row_change, col_change)
    moves = [('U', -1, 0), ('D', 1, 0), ('L', 0, -1), ('R', 0, 1)]
    
    for direction, dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_pos = new_row * 3 + new_col
            new_board = board[:]
            new_board[blank_pos], new_board[new_pos] = new_board[new_pos], new_board[blank_pos]
            neighbors.append((new_board, direction))
    
    return neighbors

def print_board(board):
    for i in range(0, 9, 3):
        print(' '.join('_' if x == 0 else str(x) for x in board[i:i+3]))
    print()

def a_star(start):
    open_list = [(manhattan_distance(start), 0, start, [])]
    closed = set()
    
    while open_list:
        f_cost, g_cost, current, path = heapq.heappop(open_list)
        
        if current == GOAL_STATE:
            return path
        
        if tuple(current) in closed:
            continue
        closed.add(tuple(current))
        
        for neighbor, move in get_neighbors(current):
            if tuple(neighbor) not in closed:
                new_g = g_cost + 1
                new_f = new_g + manhattan_distance(neighbor)
                heapq.heappush(open_list, (new_f, new_g, neighbor, path + [move]))
    
    return None

def get_user_input():
    print("Enter the initial puzzle state:")
    print("Use numbers 1-8 and 0 for the blank space")
    print("Enter 9 numbers separated by spaces (row by row):")
    
    while True:
        try:
            user_input = input("Enter puzzle state: ").strip().split() 
            if len(user_input) != 9:
                print("Error: Please enter exactly 9 numbers.")
                continue
            # Convert to integers
            puzzle = [int(x) for x in user_input]
            if sorted(puzzle) != list(range(9)):
                print("Error: Please use numbers 0-8 exactly once each.")
                continue          
            return puzzle
        except ValueError:
            print("Error: Please enter only numbers.")
            continue

def display_menu():
    print("== 8 Puzzle Solver ==")
    print("1. Input puzzle state")
    print("2. Quit")


def solve_puzzle(initial_state):
    if initial_state == GOAL_STATE:
        print("Puzzle is already solved!")
        print_board(initial_state)
        return
    
    if not is_solvable(initial_state):
        print("This puzzle configuration is not solvable!")
        return
    
    print("Puzzle is solvable. Finding solution...")
    solution = a_star(initial_state)

    if solution:
        print(f"Solution found in {len(solution)} moves:")
        current = initial_state
        print("Initial state:")
        print_board(current)
        
        for i, move in enumerate(solution, 1):
            neighbors = get_neighbors(current)
            for board, direction in neighbors:
                if direction == move:
                    current = board
                    break
            print(f"Step {i}: Move {move}")
            print_board(current)
    else:
        print("No solution exists.")

if __name__ == "__main__":
    while True:
        display_menu()      
        try:
            choice = input("Enter your choice (1-2): ").strip()         
            if choice == '1':
                initial_state = get_user_input()
                print("\nYou entered:")
                print_board(initial_state)
                
                confirm = input("Is this correct? (y/n): ").strip().lower()
                if confirm == 'y':
                    solve_puzzle(initial_state)
                else:
                    print("Please try again.")        
            elif choice == '2':
                print("Thank you for using 8-Puzzle Solver!")
                break            
            else:
                print("Invalid choice. Please enter 1 or 2.")              
        except KeyboardInterrupt:
            print("\n\nQuitting..")
            break