# A* Solver for the 8-Puzzle and 15-Puzzle

## Overview
This project implements an A* search solver for both the 8-puzzle and 15-puzzle using multiple heuristic functions. It evaluates heuristic performance by measuring solution length and node expansions across batches of solvable puzzle instances.

The project focuses on informed search, heuristic design, and performance optimization within state-space search problems.

---

## Features
- A* search implementation for both 8-puzzle and 15-puzzle
- Three heuristic functions:
  - h1: Misplaced tiles
  - h2: Manhattan distance
  - h3: Manhattan distance + linear conflict
- Solvability checking before search execution
- Batch testing on randomly generated solvable puzzles
- Performance tracking:
  - solution length
  - node expansions
- Fair comparison by running all heuristics on identical puzzle sets

---

## Heuristics

### h1 — Misplaced Tiles
Counts the number of tiles that are not in their goal position.

### h2 — Manhattan Distance
Computes the sum of row and column distances between each tile and its goal position.

### h3 — Manhattan Distance + Linear Conflict
Extends Manhattan distance by adding penalties when tiles are in the correct row or column but in reversed order, improving search efficiency.

---

## Results Summary

### 8-Puzzle
| Heuristic | Avg Steps | Avg Nodes Expanded |
|----------|----------|--------------------|
| h1       | 21.66    | 23206              |
| h2       | 21.66    | 1774               |
| h3       | 21.66    | 965                |

### 15-Puzzle
| Heuristic | Avg Steps | Avg Nodes Expanded |
|----------|----------|--------------------|
| h1       | 17.15    | 42830              |
| h2       | 17.15    | 638                |
| h3       | 17.15    | 312                |

All heuristics produced optimal solutions, while **h3 significantly reduced node expansions**, making it the most efficient.

---

## Optimizations
- Heap-based priority queue for efficient open-list operations
- Tuple-based state representation for faster comparisons
- Visited-state tracking using sets to avoid redundant exploration
- Pre-generated solvable puzzles to isolate solver performance from generation cost
- Reduced unnecessary I/O during execution

---
### Authors
Ahmed Elag  
Marc Niven Kumar  
Ayush Gogne  
Isabel Katai

*This project was originally completed as part of a university course and is shared for educational and portfolio purposes.*

## File Structure

```text
PDSHeap.py        → Core A* solver and puzzle logic
gptheuristic.py   → Heuristic implementations (h1, h2, h3)
eightTest.py      → Batch testing for 8-puzzle
fifteenTest.py    → Batch testing for 15-puzzle
Group8_Assignment_Report.pdf → Full report and analysis

