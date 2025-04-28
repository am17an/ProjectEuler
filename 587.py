import math

def calculate_shaded_area_ratio(N):
    """
    Calculate the ratio of shaded area to (4-π)/4 for N circles
    arranged horizontally with a diagonal line from (-1,-1) to (2*N,1)
    
    Each circle has radius 1 and centers are spaced 2 units apart.
    """
    # Constants
    radius = 1.0
    
    # Calculate line equation: y = mx + b
    # Line from (-1, -1) to (2*N, 1)
    m = 2 / (2*(N-1) + 2)  # Slope
    b = -1 - m * (-1)  # y-intercept
    
    # Solve quadratic equation for intersection with first circle
    # Substituting line into circle: x^2 + (mx + b)^2 = 1
    a = 1 + m**2
    b_quad = 2 * m * b
    c = b**2 - 1
    
    # Solve quadratic equation
    discriminant = b_quad**2 - 4 * a * c
    x1 = (-b_quad + math.sqrt(discriminant)) / (2 * a)
    x2 = (-b_quad - math.sqrt(discriminant)) / (2 * a)
    
    # Find corresponding y values
    y1 = m * x1 + b
    y2 = m * x2 + b
    
    # Choose the bottom-left intersection point
    intersection = (x2, y2) if x2 < x1 else (x1, y1)
    
    # Points for the triangle
    origin_point = (-1, -1)
    bottom_point = (0, -1)
    
    # Calculate triangle area
    triangle_area = 0.5 * abs(
        origin_point[0] * (intersection[1] - bottom_point[1]) +
        intersection[0] * (bottom_point[1] - origin_point[1]) +
        bottom_point[0] * (origin_point[1] - intersection[1])
    )
    
    # Calculate circular segment area
    # First calculate chord length
    chord_length = math.sqrt(
        (bottom_point[0] - intersection[0])**2 + 
        (bottom_point[1] - intersection[1])**2
    )
    
    # Calculate central angle
    central_angle = 2 * math.asin(chord_length / (2 * radius))
    
    # Area of circular segment = (r²/2) * (θ - sin θ)
    segment_area = (radius**2 / 2) * (central_angle - math.sin(central_angle))
    
    # Area of the shaded region = triangle area - segment area
    shaded_area = triangle_area - segment_area
    
    # Calculate (4 - π)/4
    target_ratio = (4 - math.pi) / 4
    
    # Calculate the ratio of shaded area to target ratio
    ratio_to_target = shaded_area / target_ratio
    
    return ratio_to_target * 100  # Return as percentage

# Verify the result for N=1 and N=2
print(f"For N=1, ratio = {calculate_shaded_area_ratio(1):.4f}%")
print(f"For N=2, ratio = {calculate_shaded_area_ratio(2):.4f}%")

# Calculate for a range of N values
for n in range(1, 10000):
    ratio = calculate_shaded_area_ratio(n)
    if ratio < 0.1:
        print(ratio, n)
        break