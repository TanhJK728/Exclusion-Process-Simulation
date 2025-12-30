import numpy as np
import random

class ExclusionProcess:
    def __init__(self, L, N, p, q):
        """
        Initialize the system.
        L: Length of lattice
        N: Number of particles
        p: Rate of jumping right
        q: Rate of jumping left
        """
        self.L = L
        self.N = N
        self.p = p # Right jump rate
        self.q = q # Left jump rate
        
        # Initialize lattice: 1 = particle, 0 = empty
        self.lattice = np.zeros(L, dtype=int)
        
        # Randomly place N particles
        indices = np.random.choice(L, N, replace=False)
        self.lattice[indices] = 1
        
        self.time = 0.0
        self.history = []
        self.time_history = []

    def get_valid_moves(self):
        """
        Identify all possible moves. 
        Returns a list of tuples: (current_index, target_index, rate)
        """
        moves = []
        
        # Find indices where particles exist
        particle_indices = np.where(self.lattice == 1)[0]
        
        for i in particle_indices:
            # Check Right Move (from i to i+1)
            right_neighbor = (i + 1) % self.L
            if self.lattice[right_neighbor] == 0 and self.p > 0:
                moves.append((i, right_neighbor, self.p))
                
            # Check Left Move (from i to i-1)
            left_neighbor = (i - 1) % self.L
            if self.lattice[left_neighbor] == 0 and self.q > 0:
                moves.append((i, left_neighbor, self.q))
                
        return moves

    def step(self):
        """
        Executes one Gillespie step.
        """
        moves = self.get_valid_moves()
        
        # If simulation gets stuck (jammed state), return False
        if not moves:
            return False

        # Calculate Total Rate (Propensity)
        total_rate = sum(m[2] for m in moves)
        
        # Determine time to next event (exponentially distributed): dt = -ln(rand) / total_rate
        dt = np.random.exponential(1.0 / total_rate)
        self.time += dt
        
        # Choose which event happens
        # We weight the choice by the rates (p or q)
        rates = [m[2] for m in moves]
        probabilities = [r / total_rate for r in rates]
        
        # Pick an index from the moves list based on probabilities
        move_index = np.random.choice(len(moves), p=probabilities)
        chosen_move = moves[move_index]
        
        # Update System
        curr, target, _ = chosen_move
        self.lattice[curr] = 0
        self.lattice[target] = 1
        
        return True

    def run(self, steps, save_every=10):
        """
        Run the simulation for a number of steps.
        """
        for s in range(steps):
            if s % save_every == 0:
                self.history.append(self.lattice.copy())
                self.time_history.append(self.time)
                
            running = self.step()
            if not running:
                print(f"System jammed at step {s}")
                break