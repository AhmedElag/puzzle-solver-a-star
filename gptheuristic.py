"""
This file includes all three heuristics used in the project.
Authors: Group #8
Date: 2025-02-14
"""
 
import math
from functools import lru_cache

@lru_cache(maxsize=None)
def get_goal_map(goal_tuple):
    """
    Given the goal state as a tuple, returns a dictionary mapping each tile
    to its (row, col) coordinates.
    """
    goal = list(goal_tuple)
    grid_size = int(math.sqrt(len(goal)))
    return {tile: divmod(idx, grid_size) for idx, tile in enumerate(goal)}

def h1(current, goal, g):
    """
    Heuristic h1: Number of misplaced tiles (ignoring the blank) plus cost so far (g).

    Parameters:
      - current: current board state (list or tuple)
      - goal: goal board state (list or tuple)
      - g: cost so far

    Returns:
      - f = g + (# of misplaced tiles)
    """
    return sum(1 for idx, tile in enumerate(current) if tile != 0 and tile != goal[idx]) + g

def h2(current, goal, g):
    """
    Heuristic h2: Manhattan distance plus cost so far (g).

    Parameters:
      - current: current board state (list or tuple)
      - goal: goal board state (list or tuple)
      - g: cost so far

    Returns:
      - f = g + (sum of Manhattan distances for each tile)
    """
    grid_size = int(math.sqrt(len(current)))
    goal_map = get_goal_map(tuple(goal))
    total_distance = 0
    for idx, tile in enumerate(current):
        if tile == 0:
            continue
        current_row, current_col = divmod(idx, grid_size)
        goal_row, goal_col = goal_map[tile]
        total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return total_distance + g

def h3(current, goal, g):
    """
    Heuristic h3: Manhattan distance plus 2 * linear conflicts plus cost so far (g).
    A linear conflict occurs when two tiles in the same row or column are in their goal
    row or column but are reversed relative to their goal order.

    Parameters:
      - current: current board state (list or tuple)
      - goal: goal board state (list or tuple)
      - g: cost so far

    Returns:
      - f = g + (Manhattan distance + 2 * linear conflicts)
    """
    grid_size = int(math.sqrt(len(current)))
    # Manhattan distance: use h2 with g = 0.
    manhattan_distance = h2(current, goal, 0)
    linear_conflict = 0

    # Check rows for linear conflicts.
    for row in range(grid_size):
        row_start = row * grid_size
        row_tiles = current[row_start:row_start + grid_size]
        for i in range(len(row_tiles)):
            tile_a = row_tiles[i]
            if tile_a == 0:
                continue
            goal_index_a = goal.index(tile_a)
            goal_row_a, goal_col_a = divmod(goal_index_a, grid_size)
            if goal_row_a != row:
                continue
            for j in range(i + 1, len(row_tiles)):
                tile_b = row_tiles[j]
                if tile_b == 0:
                    continue
                goal_index_b = goal.index(tile_b)
                goal_row_b, goal_col_b = divmod(goal_index_b, grid_size)
                if goal_row_b != row:
                    continue
                if goal_col_a > goal_col_b:
                    linear_conflict += 1

    # Check columns for linear conflicts.
    for col in range(grid_size):
        col_tiles = [current[col + i * grid_size] for i in range(grid_size)]
        for i in range(len(col_tiles)):
            tile_a = col_tiles[i]
            if tile_a == 0:
                continue
            goal_index_a = goal.index(tile_a)
            goal_row_a, goal_col_a = divmod(goal_index_a, grid_size)
            if goal_col_a != col:
                continue
            for j in range(i + 1, len(col_tiles)):
                tile_b = col_tiles[j]
                if tile_b == 0:
                    continue
                goal_index_b = goal.index(tile_b)
                goal_row_b, goal_col_b = divmod(goal_index_b, grid_size)
                if goal_col_b != col:
                    continue
                if goal_row_a > goal_row_b:
                    linear_conflict += 1

    return (manhattan_distance + 2 * linear_conflict) + g
