import matplotlib.pyplot as plt
import numpy as np

def plot_spacetime(history, title="Space-Time Diagram"):
    """
    Plots the evolution of the system.
    History: List of lattice arrays
    """
    # Convert list of arrays to 2D matrix
    data = np.array(history)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(data, aspect='auto', cmap='Greys', interpolation='nearest')
    plt.title(title)
    plt.xlabel("Lattice Site (x)")
    plt.ylabel("Time Steps (downward)")
    plt.colorbar(label="Occupancy")
    plt.show()

def plot_density_profile(history):
    """
    Plots average density per site to check for uniformity.
    """
    data = np.array(history)
    avg_density = np.mean(data, axis=0)
    
    plt.figure(figsize=(10, 4))
    plt.plot(avg_density)
    plt.ylim(0, 1)
    plt.title("Average Density Profile")
    plt.xlabel("Lattice Site")
    plt.ylabel("Density")
    plt.show()