from model import ExclusionProcess
from visualizer_static import plot_spacetime, plot_density_profile
from visualizer_dynamic import save_animation

# General Setting
L = 100  # Lattice size
N = 50  # Number of particles (density 0.5)
STEPS = 5000  # Total Gillespie steps
p=1.0
q=0.0

# Several Models

'''
# 1. SEP (Symmetric): p=0.5, q=0.5
# Particles diffuse randomly.
sim = ExclusionProcess(L=L, N=N, p=0.5, q=0.5)
mode = "SEP"
'''

'''
# 2. TASEP (Totally Asymmetric): p=1.0, q=0.0
# Particles flow only right.
sim = ExclusionProcess(L, N, p=1.0, q=0.0)
mode = "TASEP"
'''

#'''
# 3. ASEP (Asymmetric): p=0.8, q=0.2
# Drift to the right, but occasional backstepping.
sim = ExclusionProcess(L=L, N=N, p=0.8, q=0.2)
mode = "ASEP"
#'''

print(f"Running {mode} Simulation on L={L} with N={N}...")

# Run simulation
sim.run(steps=STEPS, save_every=10)

# Visualization
print("Simulation complete. Generating plots...")
plot_spacetime(sim.history, title=f"{mode} Space-Time Evolution")
plot_density_profile(sim.history)

gif_filename = f"{mode}_evolution.gif"
print(f"Creating GIF for {mode}...")
save_animation(sim.history, filename=gif_filename, fps=20, interval = 20)
