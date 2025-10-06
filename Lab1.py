from collections import deque

# Missionaries and Cannibals Problem

def mc_is_valid(state):
    M, C, B = state
    # Check for invalid states: missionaries aren't outnumbered on either side
    if M < 0 or C < 0 or M > 3 or C > 3:
        return False
    if (M > 0 and M < C) or (3 - M > 0 and 3 - M < 3 - C):
        return False
    return True

def mc_get_successors(state):
    M, C, B = state
    moves = [(1,0),(2,0),(0,1),(0,2),(1,1)]  # 1 or 2 passengers: missionaries or cannibals or both
    successors = []
    for m, c in moves:
        if B == 1:  # boat on start side: move to end side
            new_state = (M - m, C - c, 0)
        else:       # boat on end side: move to start side
            new_state = (M + m, C + c, 1)
        if mc_is_valid(new_state):
            successors.append(new_state)
    return successors

def bfs_mc():
    start = (3, 3, 1)  # (Missionaries, Cannibals, Boat side 1=start,0=end)
    goal = (0, 0, 0)
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path
        for succ in mc_get_successors(state):
            if succ not in visited:
                visited.add(succ)
                queue.append((succ, path + [succ]))
    return None

def dfs_mc():
    start = (3, 3, 1)
    goal = (0, 0, 0)
    stack = [(start, [start])]
    visited = set()
    
    while stack:
        state, path = stack.pop()
        if state == goal:
            return path
        if state in visited:
            continue
        visited.add(state)
        for succ in mc_get_successors(state):
            if succ not in visited:
                stack.append((succ, path + [succ]))
    return None


# Rabbit Leap Problem

def print_rabbit_state(state):
    return "".join(state)

def rabbit_is_valid(state):
    # No additional invalid states beyond basic format in this problem
    return True

def rabbit_get_successors(state):
    # state is list of chars: 'E', 'W', '_'
    successors = []
    length = len(state)
    empty_index = state.index('_')
    
    for i, rabbit in enumerate(state):
        if rabbit == '_':
            continue
        # Rabbits move forward only
        if rabbit == 'E':
            # E moves right
            step1 = i + 1
            step2 = i + 2
            if step1 == empty_index:
                new_state = state[:]
                new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                successors.append(new_state)
            elif step2 == empty_index and i + 1 < length and state[i+1] != '_':
                # Jump over one rabbit
                new_state = state[:]
                new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                successors.append(new_state)

        else: # rabbit == 'W'
            # W moves left
            step1 = i - 1
            step2 = i - 2
            if step1 == empty_index:
                new_state = state[:]
                new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                successors.append(new_state)
            elif step2 == empty_index and i - 1 >= 0 and state[i-1] != '_':
                # Jump over one rabbit
                new_state = state[:]
                new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                successors.append(new_state)
    return successors

def bfs_rabbit():
    start = ['E', 'E', 'E', '_', 'W', 'W', 'W']
    goal = ['W', 'W', 'W', '_', 'E', 'E', 'E']
    start_t = tuple(start)
    goal_t = tuple(goal)
    queue = deque([(start_t, [start_t])])
    visited = set([start_t])
    
    while queue:
        state, path = queue.popleft()
        if state == goal_t:
            return path
        for succ in rabbit_get_successors(list(state)):
            succ_t = tuple(succ)
            if succ_t not in visited:
                visited.add(succ_t)
                queue.append((succ_t, path + [succ_t]))
    return None

def dfs_rabbit():
    start = ['E', 'E', 'E', '_', 'W', 'W', 'W']
    goal = ['W', 'W', 'W', '_', 'E', 'E', 'E']
    start_t = tuple(start)
    goal_t = tuple(goal)
    stack = [(start_t, [start_t])]
    visited = set()
    
    while stack:
        state, path = stack.pop()
        if state == goal_t:
            return path
        if state in visited:
            continue
        visited.add(state)
        for succ in rabbit_get_successors(list(state)):
            succ_t = tuple(succ)
            if succ_t not in visited:
                stack.append((succ_t, path + [succ_t]))
    return None


def print_path(path, problem_name):
    print(f"\n{problem_name} Solution Steps ({len(path)-1} moves):")
    for step in path:
        if isinstance(step, tuple):
            print(step)
        else:
            print("".join(step))


if _name_ == "_main_":
    # Missionaries and Cannibals
    bfs_mc_path = bfs_mc()
    print_path(bfs_mc_path, "Missionaries and Cannibals BFS")
    
    dfs_mc_path = dfs_mc()
    print_path(dfs_mc_path, "Missionaries and Cannibals DFS")
    
    # Rabbit Leap
    bfs_rabbit_path = bfs_rabbit()
    print_path(bfs_rabbit_path, "Rabbit Leap BFS")
    
    dfs_rabbit_path = dfs_rabbit()
    print_path(dfs_rabbit_path, "Rabbit Leap DFS")
