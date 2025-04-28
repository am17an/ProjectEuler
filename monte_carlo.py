import random
import numpy as np
import time
from collections import deque
from tqdm import tqdm

def in_memory(memory, number):
    """Check if a number is in memory"""
    return number in memory

def update_larry_memory(memory, number):
    """Update Larry's memory according to his rule"""
    memory_list = list(memory)
    if number in memory_list:
        # Move to front if already in memory
        memory_list.remove(number)
        memory_list.insert(0, number)
    else:
        # Add to front, remove last if not in memory
        memory_list.insert(0, number)
        memory_list.pop()
    return tuple(memory_list)

def update_robin_memory(memory, number):
    """Update Robin's memory according to her rule"""
    memory_list = list(memory)
    if number not in memory_list:
        # Only update if number is not in memory
        memory_list.insert(0, number)
        memory_list.pop()
    return tuple(memory_list)

def simulate_game(rounds=50):
    """Simulate one game of Larry and Robin's memory game"""
    # Initialize memories with zeros (or other starting values)
    larry_memory = tuple([0, 0, 0, 0, 0])  # Can be changed to any initial state
    robin_memory = tuple([0, 0, 0, 0, 0])
    
    score = 0  # Current score
    larry_winning = True  # Larry starts with serve

    larry_score = 0
    robin_score = 0
    
    for _ in range(rounds):
        # Pick a random number from 1 to 10
        number = random.randint(1, 10)
        
        # Check who remembers the number
        larry_remembers = in_memory(larry_memory, number)
        robin_remembers = in_memory(robin_memory, number)
        
        # Update score based on who remembers
        if larry_remembers and robin_remembers:
            # Both remember - no score change
            pass
        elif larry_remembers:
            # Only Larry remembers
            larry_score += 1
        elif robin_remembers:
            # Only Robin remembers
            robin_score += 1
        # Update memories according to their rules
        larry_memory = update_larry_memory(larry_memory, number)
        robin_memory = update_robin_memory(robin_memory, number)
    
    return abs(larry_score - robin_score)

def monte_carlo_simulation(num_simulations=1000000, rounds=50):
    """Run multiple simulations and calculate expected value"""
    start_time = time.time()
    
    scores = []
    for _ in tqdm(range(num_simulations)):
        scores.append(simulate_game(rounds))
    
    expected_value = np.mean(scores)
    std_dev = np.std(scores)
    
    end_time = time.time()
    
    print(f"Monte Carlo simulation with {num_simulations} runs:")
    print(f"- Expected value: {expected_value:.6f}")
    print(f"- Standard deviation: {std_dev:.6f}")
    print(f"- 95% confidence interval: {expected_value:.6f} ± {1.96 * std_dev / np.sqrt(num_simulations):.6f}")
    print(f"- Time taken: {end_time - start_time:.2f} seconds")
    
    return expected_value

if __name__ == "__main__":
    import sys
    
    # Default parameters
    num_simulations = 1000000
    rounds = 50
    
    # Parse command line arguments if provided
    if len(sys.argv) > 1:
        rounds = int(sys.argv[1])
    if len(sys.argv) > 2:
        num_simulations = int(sys.argv[2])
    
    # Run simulation
    monte_carlo_simulation(num_simulations, rounds) 
