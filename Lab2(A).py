from collections import deque

# Puzzle-8 functions

def get_possible_moves(state):
    moves = []
    blank = state.index(0)
    row, col = divmod(blank, 3)
    if row > 0: moves.append(blank - 3)
    if row < 2: moves.append(blank + 3)
    if col > 0: moves.append(blank - 1)
    if col < 2: moves.append(blank + 1)
    return moves

def apply_move(state, move):
    new_state = list(state)
    blank = new_state.index(0)
    new_state[blank], new_state[move] = new_state[move], new_state[blank]
    return tuple(new_state)

def is_goal(state, goal_state):
    return state == goal_state

# Node class for search tree
class Node:
    def _init_(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

def iterative_deepening_search(start_state, goal_state, max_depth=50):
    def dls(node, goal_state, limit):
        if is_goal(node.state, goal_state):
            return node
        elif limit == 0:
            return None
        else:
            for move in get_possible_moves(node.state):
                child_state = apply_move(node.state, move)
                child = Node(child_state, parent=node, depth=node.depth + 1)
                result = dls(child, goal_state, limit - 1)
                if result is not None:
                    return result
            return None

    for depth_limit in range(max_depth):
        result = dls(Node(start_state), goal_state, depth_limit)
        if result is not None:
            return result
    return None

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

# Example Usage:
if _name_ == "_main_":
    start = (1, 2, 3,
             4, 0, 5,
             6, 7, 8)  # Example start with blank at center

    goal = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)   # Standard goal state

    result_node = iterative_deepening_search(start, goal, max_depth=20)
    if result_node:
        solution_path = reconstruct_path(result_node)
        print(f"Solution found in {len(solution_path)-1} moves:")
        for state in solution_path:
            print(state[0:3])
            print(state[3:6])
            print(state[6:9])
            print("---")
    else:
        print("No solution found within depth limit.")
