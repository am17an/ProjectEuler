import numpy as np
from scipy.integrate import dblquad

def integrand(y, x):
    # Define vectors
    a_x, a_y = -x, 30 - y
    b_x, b_y = 40 - x, -y

    # Dot product and norms
    dot = a_x * b_x + a_y * b_y
    norm_a = np.sqrt(a_x**2 + a_y**2)
    norm_b = np.sqrt(b_x**2 + b_y**2)

    # Avoid division by zero
    if norm_a == 0 or norm_b == 0:
        return 0

    cos_theta = np.clip(dot / (norm_a * norm_b), -1.0, 1.0)
    angle = np.arccos(cos_theta)
    
    return angle / (2 * np.pi)

# y-limits depend on x
def y_max(x):
    return -0.75 * x + 30

result, error = dblquad(integrand, 0, 40, lambda x: 0, y_max)

print(f"Integral result: {result/600}")