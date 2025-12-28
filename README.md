# Exclusion-Process-Simulation

Exclusion Processes: a class of stochastic models where particles jump on a lattice with the constraint that each site can contain at most one particle. 

Exclusion Principle: Particles move to adjacent sites only if the target site is empty. This creates interactions between particles even though there's no explicit force between them.

1. SEP (Symmetric Exclusion Process)

Behavior: Particles diffuse randomly left and right with equal probability

Physics analogy: Simple diffusion with volume exclusion

Real-world analogy: People in a crowded hallway moving randomly in both directions

2. TASEP (Totally Asymmetric Exclusion Process)

Behavior: Particles only move right (unidirectional flow)

Physics analogy: Driven diffusive system with a field

Real-world analogy: Cars on a one-lane road, ribosomes moving along mRNA

3. ASEP (Asymmetric Exclusion Process)

Behavior: Particles preferentially move right but can occasionally step left

Physics analogy: Biased diffusion with thermal fluctuations

Real-world analogy: Molecular motors that mostly step forward but occasionally slip backward.



How the Code Works:
model.py creates a 1D lattice of length L, randomly places N particles, and initializes tracking variables for time and history

It also implements the Gillespie Algorithm, which is a continuous-time Monte Carlo method and more efficient than fixed-time steps for systems with varying event rates.

  First step: Identify all possible moves: For each particle, check if the right/left neighbor is empty: Particle at site i can move to i+1 if empty (rate p), to i-1 if empty (rate q)
Calculate total rate: Sum of all possible transition rates

text
Total rate = sum(p for all possible right moves + q for all possible left moves)
Randomly choose time to next event:

text
Δt = -log(random()) / Total rate
Faster total rate → smaller Δt (more frequent events)

Select which event occurs: Weighted by rates

Events with higher rates (p or q) are more likely to be chosen

This ensures correct kinetics

Execute the chosen move: Move particle from current to target site

C. Boundary Conditions
The code uses periodic boundaries: Site L-1 connects to site 0

Particle at site 99 moving right goes to site 0

Creates a closed loop, mimicking an infinite system

D. Simulation Flow (main.py)
Create simulation with chosen parameters

Run for 5000 Gillespie steps

Save lattice state every 10 steps for visualization

Generate two plots:

Space-time diagram: Shows evolution over time

Density profile: Average occupancy at each site

Visual Output Interpretation
1. Space-Time Diagram (plot_spacetime)
X-axis: Lattice position (0 to 99)

Y-axis: Time (increasing downward)

Black dots: Particles at that position and time

White space: Empty sites

What to observe:

TASEP: Diagonal streaks showing rightward motion. At high density, you'll see traffic jams (clusters that move slowly).

SEP: More random, diffusive pattern without clear directionality.

ASEP: Mostly rightward with some back-and-forth motion.

2. Density Profile (plot_density_profile)
Shows average occupancy (0 to 1) at each lattice site

For periodic boundaries and homogeneous initial conditions: Should be flat at N/L = 0.5

Deviations indicate interesting dynamics or finite-size effects
