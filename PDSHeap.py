"""
Authors: Group #8
Date: 2025-02-14

This file defines the puzzle node data structure and uses A* search to solve the puzzle.
f(n) = g(n) + h(n).
"""
import math 
import heapq
import time
import eightTest
import fifteenTest

class puzzlenode:
    def __init__(self, data, level, f, parent=None):   
        self.data = tuple(data)  #puzzle state as a tuple
        self.level = level       #g(n)
        self.f = f               #f(n) = g(n) + h(n)
        self.parent = parent     #parent puzzle node

    def __lt__(self, other):
        return self.f < other.f

#generate new puzzle states from the current state.
def createChildren(node):
    
    dimension = int(math.sqrt(len(node.data)))
    zero_index = node.data.index(0) #index of blank tile
    children = []
    moves = [] #all possible move positions
    
    if zero_index % dimension != 0: #not in the first column
        moves.append(zero_index - 1) #move left

    if zero_index % dimension != dimension - 1: #not in last column
        moves.append(zero_index + 1)  #move right

    if zero_index >= dimension: #not in firsrt row
        moves.append(zero_index - dimension)  #move up

    if zero_index < dimension * (dimension - 1):  #not in last row
        moves.append(zero_index + dimension)    #move down
    
    #create a new puzzle state for each move
    for new_index in moves:
        new_puzzle = list(node.data)
        new_puzzle[zero_index], new_puzzle[new_index] = new_puzzle[new_index], new_puzzle[zero_index] # swap blank tile with tile at the new index
        new_level = node.level + 1 #g(n) increases by 1
        child = puzzlenode(tuple(new_puzzle), new_level, 0, parent=node)
        children.append(child)

    return children

def checkSolvable(puzzle): #https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    """
    Check if a given puzzle configuration is solvable.
    Works for both 8-puzzle (3x3) and 15-puzzle (4x4).

    For odd grid sizes, the puzzle is solvable if the inversion count is even.
    For even grid sizes, the puzzle is solvable if (inversions + blank_row_from_bottom) is odd.
    """
    inversions = 0
    dimension = int(math.sqrt(len(puzzle.data)))
    
    for i in range(len(puzzle.data)):
        if puzzle.data[i] == 0:
            continue
        for j in range(i + 1, len(puzzle.data)):
            if puzzle.data[j] == 0:
                continue
            if puzzle.data[i] > puzzle.data[j]: #inversion
                inversions += 1

    if dimension % 2 == 1:  #odd grid width, solvable if inversion count is even
        return inversions % 2 == 0 
    
    else: 
        blank_index = puzzle.data.index(0)
        blank_row_from_bottom = dimension - (blank_index // dimension)
        return (inversions + blank_row_from_bottom) % 2 == 1 #solvable if (inversions + blank_row_from_bottom) is odd.

#calculates the number of moves
def path(node):
    moves = 0
    while node.parent:
        moves += 1
        node = node.parent
    return moves

#solves the puzzle
def solve(start, goal, function):
    node_expansions = 0  # count everytime we expand a node
    goal = tuple(goal)
    root = puzzlenode(start, 0, function(start, goal, 0))

    #check if the puzzle is solvable
    if not checkSolvable(root):
        print("Puzzle unsolvable")
        return float("inf"), float("inf")
    
    visited = set()
    open_list = [] #heap to store puzzlenodes
    heapq.heappush(open_list, (root.f, root))
    
    while open_list:
        _, current = heapq.heappop(open_list) #lowest f(n)
        node_expansions += 1 
        if current.data in visited:
            continue
        visited.add(current.data)
        
        if current.data == goal:
            move_count = path(current) 
            return move_count, node_expansions
            
        #create children of current node
        for child in createChildren(current):
            child.f = function(child.data, goal, child.level)
            heapq.heappush(open_list, (child.f, child))

    print("No solution found")
    return float("inf"), float("inf")  



# ---------------------------
# Main Execution for statistics
# ---------------------------

if __name__ == "__main__":
    start_time = time.time()
    print("Testing 8\n")
    eightTest.testEight(100)
    print("Testing 15\n")
    fifteenTest.testFifteenBatch(100, scramble_moves=50)
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")