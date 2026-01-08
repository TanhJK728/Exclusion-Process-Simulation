import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def save_animation(history, filename, fps, interval):
    """
    Saves the simulation history as a GIF animation.
    
    Args:
        history: List of lattice arrays (0s and 1s).
        filename: Output filename.
        fps: Frames per second.
        interval: Delay between frames in milliseconds.
    """
    if not history:
        print("Error: History is empty.")
        return

    L = len(history[0])
    
    # Setup figure, height is small because it is a 1D track
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(0, L)
    ax.set_ylim(-0.5, 0.5)
    
    # Hide Y axis ticks since there is only one row
    ax.set_yticks([])
    
    # Set labels
    ax.set_xlabel("Lattice Site (x)")
    ax.set_title("Exclusion Process Animation")
    
    # Draw a gray track line
    ax.plot([0, L], [0, 0], color='lightgray', linewidth=2, zorder=0)

    # Initialize scatter plot (particles)
    # c='black' sets particles to black, s=50 sets size, marker='s' sets shape to square
    particles = ax.scatter([], [], c='black', s=50, marker='s', label='Particle', zorder=1)
    
    # Text to display current time step
    time_text = ax.text(0.02, 0.9, '', transform=ax.transAxes)

    def init():
        """Initialization function, called before the first frame"""
        particles.set_offsets(np.empty((0, 2)))
        time_text.set_text('')
        return particles, time_text

    def update(frame):
        """Update function for each frame"""
        current_lattice = history[frame]
        
        # Find indices where value is 1 (particle)
        x_positions = np.where(current_lattice == 1)[0]
        # Y coordinates are all set to 0
        y_positions = np.zeros_like(x_positions)
        
        # Combine x and y coordinates
        if len(x_positions) > 0:
            data = np.stack([x_positions, y_positions]).T
            particles.set_offsets(data)
        else:
            particles.set_offsets(np.empty((0, 2)))
            
        time_text.set_text(f"Time Step: {frame}")
        return particles, time_text

    # Create animation
    print(f"Generating animation ({len(history)} frames)... This may take a while.")
    anim = animation.FuncAnimation(
        fig, 
        update, 
        init_func=init, 
        frames=len(history), 
        interval=interval, 
        blit=True
    )
    
    # Save as GIF
    try:
        anim.save(filename, writer='pillow', fps=fps)
        print(f"Animation successfully saved as: {filename}")
    except Exception as e:
        print(f"Failed to save animation: {e}")
    
    plt.close()