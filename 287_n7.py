import matplotlib.pyplot as plt
import numpy as np

def create_diagram(N):
    """
    Create a diagram for D_N as described in the problem.
    For a positive integer N, create a 2^N × 2^N image where:
    - pixel (0,0) is bottom left
    - if (x - 2^(N-1))^2 + (y - 2^(N-1))^2 <= 2^(2N-2) then pixel is black
    """
    size = 2**N
    center = 2**(N-1)
    radius_squared = 2**(2*N-2)
    
    # Create the image array (1 for black, 0 for white)
    image = np.zeros((size, size))
    
    for x in range(size):
        for y in range(size):
            # Check if pixel should be black
            if (x - center)**2 + (y - center)**2 <= radius_squared:
                image[y, x] = 1  # Note: y first for correct orientation
    
    return image

def plot_n7_diagram():
    """Plot diagram specifically for N=7"""
    N = 2
    print(f"Generating diagram for N = {N}...")
    
    image = create_diagram(N)
    size = 2**N  # 128x128
    center = 2**(N-1)  # 64
    radius = 2**(N-1)  # 64
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    # Display the image (flip vertically so (0,0) is bottom-left)
    ax.imshow(image, cmap='gray_r', origin='lower', extent=[0, size, 0, size])
    
    # Add circle outline for visualization
    circle = plt.Circle((center, center), radius, fill=False, color='red', linewidth=3, alpha=0.8)
    ax.add_patch(circle)
    
    # Labels and title
    ax.set_title(f'D₇: {size}×{size} image\nCenter: ({center}, {center}), Radius: {radius}', fontsize=16)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_aspect('equal')
    
    # Add grid lines every 16 pixels for reference
    step = 16
    ax.set_xticks(range(0, size + 1, step))
    ax.set_yticks(range(0, size + 1, step))
    ax.grid(True, alpha=0.3)
    
    # Add minor ticks every 8 pixels
    ax.set_xticks(range(0, size + 1, 8), minor=True)
    ax.set_yticks(range(0, size + 1, 8), minor=True)
    ax.grid(True, which='minor', alpha=0.1)
    
    plt.tight_layout()
    plt.savefig('D7_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print statistics
    black_pixels = np.sum(image)
    total_pixels = size * size
    print(f"\nStatistics for N = {N}:")
    print(f"Image size: {size} × {size} = {total_pixels:,} pixels")
    print(f"Circle center: ({center}, {center})")
    print(f"Circle radius: {radius}")
    print(f"Black pixels: {int(black_pixels):,}")
    print(f"White pixels: {int(total_pixels - black_pixels):,}")
    print(f"Black pixel ratio: {black_pixels/total_pixels:.4f}")
    print(f"Theoretical circle area: π × {radius}² = {np.pi * radius**2:.1f}")
    print(f"Actual vs theoretical ratio: {black_pixels/(np.pi * radius**2):.4f}")

if __name__ == "__main__":
    plot_n7_diagram()
    print("Diagram saved as 'D7_diagram.png'") 