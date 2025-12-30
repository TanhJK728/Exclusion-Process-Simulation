# Exclusion Process Simulation

**A stochastic simulation of particle interactions on a 1D lattice using the Gillespie Algorithm.**

This project simulates **Exclusion Processes**: a class of stochastic models where particles jump on a lattice with the constraint that each site can contain at most one particle. This simple rule creates complex collective behavior and is often used to model biological transport, traffic flow, and non-equilibrium statistical mechanics.

## Core Concepts

**The Exclusion Principle:** Particles move to adjacent sites only if the target site is empty. This creates effective interactions between particles ("jamming") even though there is no explicit force between them.

This repository implements three variations of the model:

### 1. SEP (Symmetric Exclusion Process)
* **Behavior:** Particles diffuse randomly left and right with equal probability ($p=q$).
* **Physics Analogy:** Simple diffusion with volume exclusion.
* **Real-world Analogy:** People in a crowded hallway moving randomly in both directions.

### 2. TASEP (Totally Asymmetric Exclusion Process)
* **Behavior:** Particles only move right ($p=1, q=0$). This creates a unidirectional flow.
* **Physics Analogy:** A driven diffusive system under an external field.
* **Real-world Analogy:** Cars on a one-lane road, or ribosomes moving along mRNA during translation.

### 3. ASEP (Asymmetric Exclusion Process)
* **Behavior:** Particles preferentially move right but can occasionally step left ($p > q$).
* **Physics Analogy:** Biased diffusion with thermal fluctuations.
* **Real-world Analogy:** Molecular motors that mostly step forward but occasionally slip backward.

---

## Project Structure

* `model.py`: Contains the `ExclusionProcess` class. It manages the lattice state, enforces boundary conditions, and executes the Gillespie algorithm logic.
* `main.py`: The entry point. Configures the simulation parameters (Lattice size `L`, Particle count `N`, Rates `p/q`), runs the model, and triggers visualization.
* `visualizer.py`: Helper functions using `matplotlib` to generate Space-Time diagrams and Density Profiles.

---

## The Gillespie Algorithm

This simulation uses the **Gillespie Algorithm** (Continuous-Time Monte Carlo). Unlike fixed time-step methods, this approach is exact and efficient for systems with varying event rates.

### 1. Identify Valid Moves
The system scans the lattice. A particle at site $i$ can move if:
* **Right ($i+1$):** The neighbor is empty (rate $p$).
* **Left ($i-1$):** The neighbor is empty (rate $q$).

### 2. Calculate Total Propensity
We sum the rates of all currently possible moves:
$$R_{total} = \sum (\text{valid right moves} \times p) + \sum (\text{valid left moves} \times q)$$

### 3. Determine Time to Next Event
Time advances continuously based on an exponential distribution determined by the total rate. The higher the activity, the smaller the time step:
$$\Delta t = \frac{-\ln(\text{random}(0,1))}{R_{total}}$$

### 4. Select Event
An event is chosen using a weighted probability:
$$
P(\text{event}_i) = \frac{r_i}{R_{total}}
$$
*Events with higher rates are more likely to occur.*

### 5. Boundary Conditions
The simulation uses **Periodic Boundary Conditions**.
* Site $L-1$ connects to Site $0$.
* A particle moving right from the last site reappears at the first site.
* This mimics an infinite system (a closed loop).

---

## Visual Interpretation

### 1. Space-Time Diagram (`plot_spacetime`)
* **X-axis:** Lattice position ($0$ to $L$).
* **Y-axis:** Time (increasing downward).
* **Black dots:** Particles.
* **White space:** Empty sites.

**What to look for:**
* **TASEP:** Diagonal streaks indicating flow. High density leads to "traffic jams" (clusters moving slowly).
* **SEP:** No clear direction; a noisy, diffusive pattern.
* **ASEP:** General drift to the right with stochastic back-steps.

### 2. Density Profile (`plot_density_profile`)
Shows the average occupancy ($0.0$ to $1.0$) at each lattice site over the simulation history. For periodic boundaries and homogeneous initial conditions, this should generally be flat at $\rho = N/L$. Deviations may indicate finite-size effects or non-steady-state behavior.

---

## Usage

1.  **Install Dependencies:**
    ```bash
    pip install numpy matplotlib
    ```
2.  **Configure the Model:**
    Open `main.py` and comment/uncomment the desired mode block:
    ```python
    # Example: Running TASEP
    # sim = ExclusionProcess(L=L, N=N, p=0.5, q=0.5) # Comment out SEP
    sim = ExclusionProcess(L, N, p=1.0, q=0.0)       # Uncomment TASEP
    ```
3.  **Run the Simulation:**
    ```bash
    python main.py
    ```




## Visualization Guide

This project generates two primary visualizations to help you analyze the system's behavior. Here is how to interpret them.

### 1. Space-Time Evolution Diagram
This heatmap visualizes the history of the entire lattice.
* **X-Axis:** Lattice sites (spatial position $0$ to $L$).
* **Y-Axis:** Time (simulation steps, increasing downward).
* **Pixels:** Black indicates a **Particle**; White indicates an **Empty Site**.

| Pattern | Interpretation |
| :--- | :--- |
| **"Static" / Noise** | **Equilibrium Diffusion (SEP).** Particles jitter randomly left and right. No net transport is occurring. |
| **Diagonal Stripes** | **Ballistic Transport (TASEP/ASEP).** Particles are flowing in a specific direction (usually right). The slope of the line indicates the velocity. |
| **Thick Dark Bands** | **Traffic Jams.** These are clusters of particles blocking each other due to the Exclusion Principle. Notice how these "jams" often move backward (upstream) relative to the particle flow. |

### 2. Average Density Profile
This line plot shows the time-averaged occupancy of each site (0.0 to 1.0).

* **Flat Line ($\approx 0.5$):** Indicates the system has reached a **Steady State**. The noise/roughness is due to finite simulation time (stochastic fluctuations).
* **Sloped Line:** (Only in Open Boundary systems) Would indicate a density gradient, where particles pile up at one end.
* **Persistent Waves:** In periodic systems, this often indicates "Kinematic Waves" or moving clusters that haven't yet dispersed.
