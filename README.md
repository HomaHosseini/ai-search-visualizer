# Hostage Rescue — AI Search Algorithms

A grid-based hostage rescue game built with **Python and Pygame** that demonstrates three classical AI optimization algorithms: **Hill Climbing, Simulated Annealing, and Genetic Algorithm**.

The player navigates a grid containing obstacles to reach a hostage. Select an algorithm to observe how different search and optimization strategies approach the rescue task.

## Features

- **Interactive visualization:** Watch the player move through a grid-based environment.
- **Hill Climbing:** Iteratively chooses promising moves based on a heuristic.
- **Simulated Annealing:** Explores alternative solutions while allowing occasional less-promising moves to help escape local optima.
- **Genetic Algorithm:** Uses population-based search concepts to explore candidate solutions.
- **Randomized environment:** Obstacles create different navigation challenges.
- **Graphical interface:** Built with Pygame and custom image assets.

## Algorithms

| Algorithm | Approach | Main concept |
|---|---|---|
| Hill Climbing | Local search | Selects moves that appear to improve the current solution |
| Simulated Annealing | Probabilistic search | Balances exploration and exploitation using a temperature parameter |
| Genetic Algorithm | Population-based optimization | Explores candidate solutions using evolutionary operators |

## Project Structure

```text
hostage-rescue-ai-search/
├── main.py
├── assets/
│   ├── AI1.png
│   ├── AI2.png
│   ├── AI3.png
│   ├── AI4.png
│   └── AI5.png
└── README.md
```

## Requirements

- Python 3.10 or newer
- Pygame

## Learning Objectives

This project explores:

- Heuristic-based local search
- Exploration versus exploitation
- Probabilistic acceptance of candidate solutions
- Population-based optimization
- Applying AI search techniques to a grid-based navigation problem
- Visualizing algorithm behavior in an interactive environment

