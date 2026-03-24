from PDSHeap import  checkSolvable, solve, puzzlenode
from gptheuristic import h1, h2, h3
import random

def create8Puzzle():
    state = [0,1,2,3,4,5,6,7,8]
    random.shuffle(state)
    f = 0
    level = 0
    puzzle = puzzlenode(state, level, f)
    return puzzle

def generateSolvable8(): #create a solvable puzzle
    while True:
        puzzle = create8Puzzle()
        if checkSolvable(puzzle):
            return puzzle
        
def testEight(numpuzzles):
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    heuristics = [("h1", h1), ("h2", h2), ("h3", h3)]
    results = {name: [] for name, _ in heuristics}
    
    for i in range(numpuzzles):
        puzzle = generateSolvable8()
        for name, heuristic in heuristics:
            sol, exp = solve(puzzle.data, goal, heuristic)
            results[name].append((sol, exp))
        
    # Print summary of average results.
    print("\n=== 8 Puzzle Summary ===")
    print("Heuristic   Avg Steps   Avg Node Expansions")
    for name, _ in heuristics:
        total_sol = sum(sol for sol, exp in results[name])
        total_exp = sum(exp for sol, exp in results[name])
        print("{:<10}  {:<10.2f}  {:<10.2f}".format(name, total_sol/numpuzzles, total_exp/numpuzzles))
        

