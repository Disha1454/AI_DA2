import copy

# Define the goal state
GOAL_STATE = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]  # 0 represents the blank tile

# Heuristic: Manhattan Distance
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # Ignore the blank tile
                goal_x, goal_y = divmod(state[i][j] - 1, 3)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

# Get possible moves
def get_neighbors(state):
    neighbors = []
    x, y = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)

    moves = {'up': (x - 1, y), 'down': (x + 1, y), 'left': (x, y - 1), 'right': (x, y + 1)}
    for move, (nx, ny) in moves.items():
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append((new_state, move))
    return neighbors

# Hill Climbing Algorithm
def hill_climbing(start_state):
    current_state = start_state
    current_cost = manhattan_distance(current_state)
    steps = []

    while True:
        neighbors = get_neighbors(current_state)
        neighbors = [(state, manhattan_distance(state)) for state, move in neighbors]
        neighbors.sort(key=lambda x: x[1])  # Sort by heuristic value

        if not neighbors or neighbors[0][1] >= current_cost:
            # No better neighbors (local maxima/plateau)
            break

        # Move to the best neighbor
        current_state, current_cost = neighbors[0]
        steps.append(current_state)

        if current_state == GOAL_STATE:
            break

    return steps, current_state == GOAL_STATE

# Test the algorithm
if __name__ == "__main__":
    initial_state = [[2, 8, 3],
                     [1, 6, 4],
                     [7, 0, 5]]

    steps, success = hill_climbing(initial_state)
    print(f"Success: {success}")
    print(f"Steps taken ({len(steps)}):")
    for step in steps:
        for row in step:
            print(row)
        print()
