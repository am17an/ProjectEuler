#!/usr/bin/env python3

import random
import numpy as np

def simulate_one_trial():
    """
    Simulate drawing cards from a shuffled deck until finding
    a consecutive pair of the same rank or reaching the end.
    Returns the number of cards drawn.
    """
    # Create a standard deck (values represent ranks 0-12)
    deck = [rank % 13 for rank in range(52)]
    
    # Shuffle the deck
    random.shuffle(deck)
    
    # Draw cards until finding consecutive pair or end of deck
    draws = 1  # First card is always drawn
    prev_rank = deck[0]
    
    for i in range(1, 52):
        draws += 1
        curr_rank = deck[i]
        
        # Check if we found a consecutive pair
        if curr_rank == prev_rank:
            return draws
        
        prev_rank = curr_rank
    
    # If we reach here, we drew all 52 cards without finding a pair
    # For exhausted deck case, return the full 52 (same as exact DP algorithm)
    return 52

def monte_carlo_simulation(num_trials=1000000):
    """
    Run Monte Carlo simulation with specified number of trials.
    Returns the estimated expected number of draws.
    """
    total_draws = 0
    
    for _ in range(num_trials):
        draws = simulate_one_trial()
        # When no consecutive pair is found (draws == 52), we count it as 52
        # This matches the DP implementation that returns 52 when deck is exhausted
        total_draws += draws
    
    expected_draws = total_draws / num_trials
    return expected_draws

if __name__ == "__main__":
    # Set seed for reproducibility
    random.seed(42)
    
    # When no consecutive pair is found, both the DP solution and Monte Carlo
    # return 52, meaning we've gone through all 52 cards
    
    # Number of trials (higher = more accurate but slower)
    trials = 1000000
    
    print(f"Running Monte Carlo simulation with {trials:,} trials...")
    expected = monte_carlo_simulation(trials)
    print(f"Expected number of draws: {expected:.8f}")
    
    # Calculate a modified expectation where we add 52 when no pair is found
    # This seems to be what the user is suggesting
    modified_total = 0
    no_pair_count = 0
    for _ in range(trials):
        draws = simulate_one_trial()
        if draws == 52:  # No consecutive pair found
            modified_total += 52 + 52  # Add 52 (as requested by user)
            no_pair_count += 1
        else:
            modified_total += draws
    
    modified_expected = modified_total / trials
    no_pair_probability = no_pair_count / trials
    
    print(f"Probability of no consecutive pair: {no_pair_probability:.8f}")
    print(f"Modified expectation (adding 52 when no pair): {modified_expected:.8f}")
    print(f"Expected with 52 added for no-pair case would be: {expected + 52 * no_pair_probability:.8f}")
    
    # Calculate 95% confidence interval by running multiple batches
    batch_size = 10000
    num_batches = 100
    batch_results = []
    
    for i in range(num_batches):
        if i % 10 == 0:
            print(f"Computing batch {i+1}/{num_batches}...")
        batch_expected = monte_carlo_simulation(batch_size)
        batch_results.append(batch_expected)
    
    mean = np.mean(batch_results)
    std_error = np.std(batch_results, ddof=1) / np.sqrt(num_batches)
    ci_lower = mean - 1.96 * std_error
    ci_upper = mean + 1.96 * std_error
    
    print("\nStatistical results:")
    print(f"Mean estimate: {mean:.8f}")
    print(f"95% confidence interval: [{ci_lower:.8f}, {ci_upper:.8f}]")
    print(f"Standard error: {std_error:.8f}")
    
    # Compare with the exact result from DP
    dp_result = 19.46138169
    print(f"\nDP result from C++: {dp_result}")
    print(f"Difference: {abs(mean - dp_result):.8f}")
    
    # Count frequency of different draw counts
    freq_counts = {}
    no_pair_count = 0
    for _ in range(100000):  # Use smaller sample for frequency counting
        draws = simulate_one_trial()
        if draws == 52:
            no_pair_count += 1
        freq_counts[draws] = freq_counts.get(draws, 0) + 1
    
    print("\nFrequency of draw counts (top 10):")
    sorted_counts = sorted(freq_counts.items(), key=lambda x: x[1], reverse=True)
    for draws, count in sorted_counts[:10]:
        print(f"{draws} draws: {count/100000:.6f} probability")
    
    print(f"\nProbability of no consecutive pair in the deck: {no_pair_count/100000:.6f}") 