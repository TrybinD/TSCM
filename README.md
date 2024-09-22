# TSCM
Repo for research on Task scheduling in cloud manufacturing with RL and GNN


Results of the work

1) The `Problem` class is implemented, which contains a description of the problem and methods for downloading problems from the dataset

2) The `calculate_cost` function, which calculates the cost of production for a given problem and solution

3) A number of `Solver` that represent different strategies for solving the problem:

- `RandomSolver` - Creates a random solution. Used in the notebook '1_baselines.ipynb'
- `GreedySolver` - Creates a greedy solution. Used in the notebook '1_baselines.ipynb'
- `MIPPaperSolver` - Finds a solution using the formulation from the paper with integer programming. Used in the notebook '2_mip.ipynb'
- `MIPSolver` - Finds a solution using the simplified formulation with integer programming. Used in the notebook '2_mip.ipynb'
- `DPSolver` - Finds a solution using Dynamic Programming.  Used in the notebook '3_dp.ipynb'

4) In notebook "4_compare.ipynb" the results of various solutions are compared



