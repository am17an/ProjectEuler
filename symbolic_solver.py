#!/usr/bin/env python3
import numpy as np
from dataclasses import dataclass
from collections import defaultdict
import time
from typing import Dict, Set, Tuple, List, Optional

@dataclass(frozen=True)
class SymbolicState:
    """Represents a symbolic state of the memory game."""
    # Tuples to represent ordered memory (newest element first)
    larry_memory: tuple
    robin_memory: tuple
    # Score (positive means Larry is ahead, negative means Robin is ahead)
    score: int
    # Who has the serve (True for Larry, False for Robin)
    larry_serving: bool
    
    def __repr__(self):
        larry_mem = ','.join(str(x) for x in self.larry_memory) or "∅"
        robin_mem = ','.join(str(x) for x in self.robin_memory) or "∅"
        serving = "L" if self.larry_serving else "R"
        return f"({larry_mem}|{robin_mem}|{self.score}|{serving})"


class SymbolicSolver:
    def __init__(self, memory_size=5, total_symbols=10):
        self.memory_size = memory_size
        self.total_symbols = total_symbols
        
        # We'll use single letters for memory
        self.symbols = tuple(chr(ord('a') + i) for i in range(total_symbols))
        
        # Threshold for pruning low-probability states
        self.probability_threshold = 1e-40
        
    def update_larry_memory(self, memory: tuple, symbol: str) -> tuple:
        """Update Larry's memory according to his rule."""
        memory_list = list(memory)
        
        # If symbol is in memory, move it to the front
        if symbol in memory_list:
            memory_list.remove(symbol)
            memory_list.insert(0, symbol)
        else:
            # Add to front, remove last if needed
            memory_list.insert(0, symbol)
            if len(memory_list) > self.memory_size:
                memory_list.pop()
        
        return tuple(memory_list)
    
    def update_robin_memory(self, memory: tuple, symbol: str) -> tuple:
        """Update Robin's memory according to her rule."""
        memory_list = list(memory)
        
        # If symbol is in memory, do nothing
        if symbol in memory_list:
            return memory
        else:
            # Add to front, remove last if needed
            memory_list.insert(0, symbol)
            if len(memory_list) > self.memory_size:
                memory_list.pop()
            
            return tuple(memory_list)

    def get_next_state(self, state: SymbolicState, symbol: str) -> SymbolicState:
        """Compute the next state after a symbol is called."""
        larry_remembers = symbol in state.larry_memory
        robin_remembers = symbol in state.robin_memory
        
        # Calculate new score and serving status
        new_score = state.score
        new_larry_serving = state.larry_serving
        
        if larry_remembers and robin_remembers:
            # Both remember - no score change
            pass
        elif larry_remembers:
            # Only Larry remembers
            if state.larry_serving:
                new_score += 1
            else:
                new_score -= 1
                if new_score == 0:
                    new_larry_serving = True
        elif robin_remembers:
            # Only Robin remembers
            if not state.larry_serving:
                new_score += 1
            else:
                new_score -= 1
                if new_score <= 0:
                    new_larry_serving = False
                    new_score = abs(new_score)  # Convert to positive
        
        # Update memories
        new_larry_memory = self.update_larry_memory(state.larry_memory, symbol)
        new_robin_memory = self.update_robin_memory(state.robin_memory, symbol)
        
        return SymbolicState(
            larry_memory=new_larry_memory,
            robin_memory=new_robin_memory,
            score=new_score,
            larry_serving=new_larry_serving
        )
    
    def solve_dp(self, n_rounds: int) -> Tuple[float, Dict[SymbolicState, float]]:
        """Solve using dynamic programming approach - propagating probabilities forward.
        Returns expected score and final state distribution."""
        print(f"Solving with dynamic programming for {n_rounds} rounds...")
        start_time = time.time()
        
        # Start with empty memories
        initial_state = SymbolicState(
            larry_memory=(),  # Empty tuple
            robin_memory=(),  # Empty tuple
            score=0,
            larry_serving=True
        )
        
        # Dictionary to store probabilities of each state
        # Key: state, Value: probability
        prev_round = {initial_state: 1.0}
        
        # For each round
        for round_num in range(n_rounds):
            print(f"Round {round_num}: {len(prev_round)} states")
            curr_round = defaultdict(float)
            pruned_states = 0
            processed_states = 0
            
            # For each state in previous round
            for state, probability in prev_round.items():
                # Skip low probability states
                if probability < self.probability_threshold:
                    pruned_states += 1
                    continue
                
                processed_states += 1
                
                # Categorize symbols by their presence in memory
                larry_memory_set = set(state.larry_memory)
                robin_memory_set = set(state.robin_memory)
                
                # Find symbols in both memories
                both_remember = larry_memory_set.intersection(robin_memory_set)
                
                # Find symbols only in Larry's memory
                larry_only = larry_memory_set - robin_memory_set
                
                # Find symbols only in Robin's memory
                robin_only = robin_memory_set - larry_memory_set
                
                # Calculate number of symbols in neither memory
                total_remembered = len(both_remember) + len(larry_only) + len(robin_only)
                neither_count = self.total_symbols - total_remembered
                
                # Case 1: Both players remember (each symbol leads to a different state for Larry)
                if both_remember:
                    for symbol in both_remember:
                        next_state = self.get_next_state(state, symbol)
                        # Probability = 1 / total_symbols for each symbol
                        new_prob = probability * (1 / self.total_symbols)
                        if new_prob >= self.probability_threshold:
                            curr_round[next_state] += new_prob
                
                # Case 2: Only Larry remembers
                if larry_only:
                    # Each symbol in larry_only leads to a different state, so process all
                    for symbol in larry_only:
                        next_state = self.get_next_state(state, symbol)
                        # Probability = 1 / total_symbols for each symbol
                        new_prob = probability * (1 / self.total_symbols)
                        if new_prob >= self.probability_threshold:
                            curr_round[next_state] += new_prob
                
                # Case 3: Only Robin remembers
                if robin_only:
                    # Use the first symbol alphabetically for deterministic behavior
                    symbol = sorted(robin_only)[0]
                    next_state = self.get_next_state(state, symbol)
                    # Probability = (number only in Robin's memory) / total_symbols
                    new_prob = probability * (len(robin_only) / self.total_symbols)
                    if new_prob >= self.probability_threshold:
                        curr_round[next_state] += new_prob
                
                # Case 4: Neither remembers
                if neither_count > 0:
                    # Use a representative new symbol (one that's not in either memory)
                    used_symbols = larry_memory_set.union(robin_memory_set)
                    available_symbols = set(self.symbols) - used_symbols
                    
                    if available_symbols:
                        # Use the first symbol alphabetically for deterministic behavior
                        symbol = sorted(available_symbols)[0]
                        next_state = self.get_next_state(state, symbol)
                        # Probability = (number in neither memory) / total_symbols
                        new_prob = probability * (neither_count / self.total_symbols)
                        if new_prob >= self.probability_threshold:
                            curr_round[next_state] += new_prob
            
            print(f"  Processed {processed_states} states, pruned {pruned_states} low-probability states")
            prev_round = curr_round
        
        # Calculate expected score
        expected_score = 0.0
        for state, probability in prev_round.items():
            expected_score += state.score * probability
        
        print(f"DP solution completed in {time.time() - start_time:.2f} seconds")
        return expected_score, prev_round
    
    def print_state_statistics(self, states_dict):
        """Print statistics about the states."""
        score_counts = defaultdict(int)
        larry_memory_sizes = defaultdict(int)
        robin_memory_sizes = defaultdict(int)
        score_probability = defaultdict(float)
        total_probability = 0.0
        
        for state, prob in states_dict.items():
            score_counts[state.score] += 1
            larry_memory_sizes[len(state.larry_memory)] += 1
            robin_memory_sizes[len(state.robin_memory)] += 1
            score_probability[state.score] += prob
            total_probability += prob
        
        print("\nState Statistics:")
        print(f"Total states: {len(states_dict)}")
        print(f"Total probability: {total_probability}")
        
        print("\nScore distribution:")
        for score in sorted(score_counts.keys()):
            print(f"  Score {score}: {score_counts[score]} states, probability: {score_probability[score]:.6f}")
        
        # Calculate expected score
        expected_score = sum(score * prob for score, prob in score_probability.items())
        print(f"\nExpected score: {expected_score:.6f}")
        
        print("\nLarry memory size distribution:")
        for size in sorted(larry_memory_sizes.keys()):
            print(f"  Size {size}: {larry_memory_sizes[size]} states")
        
        print("\nRobin memory size distribution:")
        for size in sorted(robin_memory_sizes.keys()):
            print(f"  Size {size}: {robin_memory_sizes[size]} states")

    def analyze_high_probability_states(self, states_dict, top_n=10):
        """Print details of the highest probability states."""
        sorted_states = sorted(states_dict.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\nTop {min(top_n, len(sorted_states))} highest probability states:")
        total_prob_shown = 0.0
        
        for i, (state, prob) in enumerate(sorted_states[:top_n]):
            print(f"  {i+1}. {state} - Probability: {prob:.8f}")
            total_prob_shown += prob
            
            # Analyze this state
            larry_set = set(state.larry_memory)
            robin_set = set(state.robin_memory)
            both = larry_set.intersection(robin_set)
            larry_only = larry_set - robin_set
            robin_only = robin_set - larry_set
            neither = self.total_symbols - len(larry_set.union(robin_set))
            
            print(f"    Both remember: {len(both)} symbols")
            print(f"    Larry only: {len(larry_only)} symbols")
            print(f"    Robin only: {len(robin_only)} symbols")
            print(f"    Neither: {neither} symbols")
        
        print(f"\nTotal probability of top {min(top_n, len(sorted_states))} states: {total_prob_shown:.6f}")

# Main execution
if __name__ == "__main__":
    # Create a solver with memory size 5 and 10 symbols
    solver = SymbolicSolver(memory_size=5, total_symbols=10)
    rounds = 15
    start_time = time.time()
    expected_score, final_states = solver.solve_dp(rounds)
    end_time = time.time()
    
    print(f"\nExpected score after {rounds} rounds: {expected_score:.8f}")
    print(f"Total computation time: {end_time - start_time:.2f} seconds")

    
    # Print state statistics
