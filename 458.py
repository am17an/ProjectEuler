from itertools import permutations, product
from tqdm import tqdm  # For progress bar

def is_subsequence(pattern, text):
    """Check if pattern is a subsequence of text."""
    it = iter(text)
    return all(c in it for c in pattern)

def count_valid_arrangements():
    # Define letters and length
    letters = ['p', 'r', 'o', 'j', 'e', 'c', 't']
    length = 8
    
    # Generate all permutations of "project"
    project_permutations = list(permutations(letters))
    print(f"Generated {len(project_permutations)} permutations")
    
    # Calculate total possible arrangements
    total = 7**8
    print(f"Total possible arrangements: {total}")
    
    # Counter for valid arrangements
    valid_count = 0
    
    # Generate and check all arrangements
    all_arrangements = product(letters, repeat=length)
    
    # Use tqdm for progress tracking
    for arrangement in tqdm(all_arrangements, total=total):
        # Check if arrangement contains any permutation as a subsequence
        contains_permutation = False
        for perm in project_permutations:
            if is_subsequence(perm, arrangement):
                contains_permutation = True
                break
        
        if not contains_permutation:
            valid_count += 1
    
    return valid_count

if __name__ == "__main__":
    print("Counting valid arrangements...")
    result = count_valid_arrangements()
    print(f"Number of valid arrangements: {result}")
    print(f"Expected result from inclusion-exclusion: 5,623,681")
