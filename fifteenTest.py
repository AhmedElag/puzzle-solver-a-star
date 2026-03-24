
from PDSHeap import puzzlenode, checkSolvable, solve
from gptheuristic import h1, h2, h3
import random
# ---------------------------
# 15-Puzzle Generation Functions
# ---------------------------
GOAL15 = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)

def get_neighbors_15(state):
    dimension = 4
    blank_index = state.index(0)
    neighbors = []
    row, col = blank_index // dimension, blank_index % dimension
    moves = []
    if row > 0:
        moves.append(blank_index - dimension)
    if row < dimension - 1:
        moves.append(blank_index + dimension)
    if col > 0:
        moves.append(blank_index - 1)
    if col < dimension - 1:
        moves.append(blank_index + 1)
    for move in moves:
        new_state = list(state)
        new_state[blank_index], new_state[move] = new_state[move], new_state[blank_index]
        neighbors.append(tuple(new_state))
    return neighbors

def create15Puzzle(scramble_moves):
    goal_state = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
    current = goal_state[:]
    for _ in range(scramble_moves):
        nbrs = get_neighbors_15(tuple(current))
        current = list(random.choice(nbrs))
    return puzzlenode(current, 0, 0, current.index(0))

def generate_unique_puzzles_15(numpuzzles, scramble_moves):
    unique = set()
    puzzles = []
    while len(unique) < numpuzzles:
        puzzle = create15Puzzle(scramble_moves)
        if not checkSolvable(puzzle):
            continue
        state_tuple = tuple(puzzle.data)
        if state_tuple in unique:
            continue
        unique.add(state_tuple)
        puzzles.append(puzzle)
    return puzzles

def testFifteenBatch(numpuzzles=100, scramble_moves=50):
    goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
    heuristics = [("h1", h1), ("h2", h2), ("h3", h3)]
    results = {name: [] for name, _ in heuristics}
    
    puzzles = generate_unique_puzzles_15(numpuzzles, scramble_moves)
    for puzzle in puzzles:
        for name, heuristic in heuristics:
            res = solve(puzzle.data, goal, heuristic)
            if isinstance(res, tuple):
                sol, exp = res
                results[name].append((sol, exp))
    #print("\nRunning batch tests for 15-puzzle...\n")
    print("=== 15 Puzzle Summary ===")
    print("Heuristic   Avg Steps   Avg Node Expansions")
    for name, _ in heuristics:
        count = len(results[name])
        if count > 0:
            total_sol = sum(sol for sol, exp in results[name])
            total_exp = sum(exp for sol, exp in results[name])
            print("{:<10}  {:<10.2f}  {:<10.2f}".format(name, total_sol / count, total_exp / count))
        else:
            print("{:<10}  No results".format(name))