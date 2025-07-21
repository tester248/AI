import heapq
import numpy as np
from collections import deque

class PuzzleNode:
    """Node class for 8-puzzle problem."""
    
    def __init__(self, state, parent=None, move=None, depth=0, cost=0, heuristic=0):
        self.state = state  # 3x3 numpy array representing the puzzle
        self.parent = parent  # parent node
        self.move = move  # move that led to this state
        self.depth = depth  # depth in the search tree
        self.cost = cost  # path cost to this node
        self.heuristic = heuristic  # heuristic value
        self.f = cost + heuristic  # f(n) = g(n) + h(n)
    
    def __lt__(self, other):
        """Comparison method for priority queue."""
        return self.f < other.f
    
    def __eq__(self, other):
        """Check if two states are equal."""
        if other is None:
            return False
        return np.array_equal(self.state, other.state)
    
    def __hash__(self):
        """Hash function for the state."""
        return hash(str(self.state))

class Puzzle8:
    """Class for solving 8-puzzle problem using A* algorithm."""
    
    def __init__(self, initial_state=None):
        """Initialize the puzzle with an initial state."""
        if initial_state is None:
            # Default initial state
            self.initial_state = np.array([
                [1, 2, 3],
                [4, 0, 6],
                [7, 5, 8]
            ])
        else:
            self.initial_state = initial_state
            
        # Define the goal state
        self.goal_state = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
    
    def find_blank(self, state):
        """Find the position of the blank (0) in the state."""
        blank_pos = np.where(state == 0)
        return (blank_pos[0][0], blank_pos[1][0])
    
    def get_neighbors(self, node):
        """Get all possible neighbor states by moving the blank tile."""
        neighbors = []
        blank_row, blank_col = self.find_blank(node.state)
        
        # Possible moves: up, down, left, right
        moves = [
            ('up', (-1, 0)),
            ('down', (1, 0)),
            ('left', (0, -1)),
            ('right', (0, 1))
        ]
        
        for move_name, (dr, dc) in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            
            # Check if the move is valid
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Create a new state by swapping tiles
                new_state = node.state.copy()
                new_state[blank_row, blank_col] = new_state[new_row, new_col]
                new_state[new_row, new_col] = 0
                
                # Create a new node
                new_node = PuzzleNode(
                    state=new_state,
                    parent=node,
                    move=move_name,
                    depth=node.depth + 1,
                    cost=node.depth + 1,
                    heuristic=self.calculate_heuristic(new_state)
                )
                
                neighbors.append(new_node)
        
        return neighbors
    
    def calculate_heuristic(self, state):
        """
        Calculate the heuristic value for the given state.
        Using Manhattan distance heuristic.
        """
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i, j] != 0:
                    # Find the goal position of the current tile
                    goal_pos = np.where(self.goal_state == state[i, j])
                    goal_row, goal_col = goal_pos[0][0], goal_pos[1][0]
                    
                    # Calculate Manhattan distance
                    distance += abs(i - goal_row) + abs(j - goal_col)
        
        return distance
    
    def solve(self):
        """Solve the 8-puzzle using A* algorithm."""
        initial_node = PuzzleNode(
            state=self.initial_state,
            heuristic=self.calculate_heuristic(self.initial_state)
        )
        
        # Priority queue for open list
        open_list = []
        heapq.heappush(open_list, initial_node)
        
        # Set for closed list to check if a state is already explored
        closed_set = set()
        
        nodes_expanded = 0
        max_queue_size = 1
        
        while open_list:
            # Update max queue size
            max_queue_size = max(max_queue_size, len(open_list))
            
            # Get the node with the lowest f value
            current_node = heapq.heappop(open_list)
            nodes_expanded += 1
            
            # Check if goal is reached
            if np.array_equal(current_node.state, self.goal_state):
                return self.extract_solution(current_node), nodes_expanded, max_queue_size
            
            # Add the current state to closed set
            closed_set.add(str(current_node.state))
            
            # Generate neighbors
            for neighbor in self.get_neighbors(current_node):
                # Skip if this state is already explored
                if str(neighbor.state) in closed_set:
                    continue
                
                # Add to open list
                heapq.heappush(open_list, neighbor)
        
        return None, nodes_expanded, max_queue_size  # No solution found
    
    def extract_solution(self, goal_node):
        """Extract the solution path from initial state to goal state."""
        path = []
        current = goal_node
        
        while current:
            path.append((current.state, current.move))
            current = current.parent
        
        return path[::-1]  # Reverse to get path from initial to goal
    
    def print_solution(self, solution_path):
        """Print the solution path in a readable format."""
        if not solution_path:
            print("No solution found.")
            return
        
        print(f"Solution found in {len(solution_path) - 1} steps:")
        
        for i, (state, move) in enumerate(solution_path):
            if i == 0:
                print("Initial state:")
            else:
                print(f"\nStep {i}: {move}")
            
            for row in state:
                print(" ".join(str(cell) if cell != 0 else "_" for cell in row))

def get_user_input():
    """Get the initial state from the user."""
    print("Enter the initial state of the 8-puzzle (use 0 for the blank):")
    print("Enter each row with spaces between numbers (e.g., '1 2 3'):")
    
    initial_state = []
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1}: ").strip().split()))
                if len(row) != 3 or not all(0 <= n <= 8 for n in row):
                    print("Each row must have exactly 3 numbers between 0 and 8.")
                    continue
                initial_state.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
    
    return np.array(initial_state)

def is_solvable(state):
    """Check if the puzzle is solvable."""
    # Flatten the state but ignore the blank (0)
    flat_state = [num for num in state.flatten() if num != 0]
    
    # Count inversions
    inversions = 0
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1
    
    # For 8-puzzle, if the number of inversions is even, the puzzle is solvable
    return inversions % 2 == 0

def main():
    """Main function to solve the 8-puzzle."""
    print("8-Puzzle Solver using A* algorithm")
    print("----------------------------------")
    
    # Get user input or use default
    use_default = input("Use default puzzle state? (y/n): ").lower() == 'y'
    
    if use_default:
        initial_state = np.array([
            [1, 3, 2,
            4, 6, 5, 
             7, 0, 8]
        ])
    else:
        initial_state = get_user_input()
    
    # Check if the puzzle is solvable
    if not is_solvable(initial_state):
        print("The given puzzle is not solvable!")
        return
    
    # Create puzzle and solve
    puzzle = Puzzle8(initial_state)
    print("\nSolving puzzle...")
    solution, nodes_expanded, max_queue_size = puzzle.solve()
    
    # Print results
    puzzle.print_solution(solution)
    print(f"\nNodes expanded: {nodes_expanded}")
    print(f"Maximum queue size: {max_queue_size}")

if __name__ == "__main__":
    main()