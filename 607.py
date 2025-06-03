import math

def calculate_ac_plus_cd(theta_degrees):
    # Convert angle from degrees to radians
    radians = math.radians(theta_degrees)

    rest = (100-50*math.sqrt(2))/10

    othersides = (50*math.sqrt(2))/(2*math.cos(radians))

    r = 0.4*othersides/(9) + 0.4*othersides/8 + 0.2*othersides/7
    r += 0.2*othersides/(7) + 0.4*othersides/6 + 0.2*othersides/5

    return r + rest


def golden_section_search(f, a, b, tol=1e-10):
    """
    Find minimum of unimodal function f within [a, b] using golden section search.
    Returns x value corresponding to the minimum with tolerance tol.
    """
    golden_ratio = (math.sqrt(5) + 1) / 2
    c = b - (b - a) / golden_ratio
    d = a + (b - a) / golden_ratio
    
    while abs(b - a) > tol:
        if f(c) < f(d):
            b = d
        else:
            a = c
        
        c = b - (b - a) / golden_ratio
        d = a + (b - a) / golden_ratio
    
    return (a + b) / 2

# Thoroughly search for the minimum in a wider range
print("Searching for optimum θ with high precision...")

# First, do a coarse search to find approximate minimum
coarse_thetas = [theta for theta in range(-10, 20)]
coarse_values = [calculate_ac_plus_cd(theta) for theta in coarse_thetas]
min_index = coarse_values.index(min(coarse_values))
min_theta_coarse = coarse_thetas[min_index]

print(f"Coarse search suggests minimum near θ = {min_theta_coarse}°")

# Refine the search with golden section in a narrower range around the coarse minimum
lower_bound = max(1, min_theta_coarse - 2)
upper_bound = min_theta_coarse + 2

optimum_theta = golden_section_search(calculate_ac_plus_cd, lower_bound, upper_bound)
optimum_result = calculate_ac_plus_cd(optimum_theta)

print(f"Optimum θ = {optimum_theta:.10f}°")
print(f"Minimum AC + CD = {optimum_result:.10f}")

print(calculate_ac_plus_cd(180))