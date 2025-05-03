from math import factorial

def generate_combinations(digits, max_occurrences, max_length, current_combination=None, index=0, all_combinations=None):
    """
    Generate all combinations of digits where each digit can appear up to max_occurrences times,
    with a total length up to max_length.
    
    Args:
        digits: List of available digits
        max_occurrences: Maximum number of times each digit can appear
        max_length: Maximum length of the combination
        current_combination: Current combination being built
        index: Current index in the digits list
        all_combinations: List to store all generated combinations
    
    Returns:
        List of all valid combinations
    """
    if current_combination is None:
        current_combination = []
    if all_combinations is None:
        all_combinations = []
    
    # Add the current combination if it's not empty and has the target length
    if current_combination and len(current_combination) == max_length:
        all_combinations.append(current_combination.copy())
    
    # If we've reached the maximum length, return
    if len(current_combination) >= max_length:
        return all_combinations
    
    # Try adding each digit from the current index
    for i in range(index, len(digits)):
        digit = digits[i]
        # Count occurrences of this digit in the current combination
        occurrences = current_combination.count(digit)
        
        # If we haven't used this digit the maximum number of times
        if occurrences < max_occurrences:
            # Add this digit to the combination
            current_combination.append(digit)
            # Recursively generate combinations with this digit added
            generate_combinations(digits, max_occurrences, max_length, 
                                 current_combination, i, all_combinations)
            # Backtrack by removing the last digit
            current_combination.pop()
    
    return all_combinations

def count_permutations(digits, allow_leading_zero=True):
    """
    Count the number of permutations of a set of digits.
    
    Args:
        digits: The set of digits to permute
        allow_leading_zero: Whether to allow leading zeros
    
    Returns:
        The number of permutations
    """
    # Count the occurrences of each digit
    digit_counts = {}
    for digit in digits:
        if digit in digit_counts:
            digit_counts[digit] += 1
        else:
            digit_counts[digit] = 1
    
    # Calculate the total number of permutations
    total_permutations = factorial(len(digits))
    
    # Adjust for repeated digits
    for count in digit_counts.values():
        if count > 1:
            total_permutations //= factorial(count)
    
    # If leading zeros are not allowed, subtract permutations with leading zero
    if not allow_leading_zero and 0 in digit_counts:
        # Calculate permutations without leading zero
        # This is equivalent to calculating permutations where the first position
        # can only be filled with non-zero digits
        
        # Number of ways to choose a non-zero digit for the first position
        non_zero_choices = len(digits) - digit_counts[0]
        
        # Number of ways to arrange the remaining digits
        remaining_perms = factorial(len(digits) - 1)
        
        # Adjust for repeated digits in the remaining positions
        remaining_digit_counts = digit_counts.copy()
        # We've used one of the non-zero digits, so decrement its count
        # We need to account for all possible non-zero digits that could be used
        
        # Calculate permutations without leading zero
        permutations_without_leading_zero = 0
        
        for digit in range(1, 10):  # Consider each non-zero digit
            if digit in digit_counts and digit_counts[digit] > 0:
                # Create a copy of digit counts with this digit decremented
                temp_counts = digit_counts.copy()
                temp_counts[digit] -= 1
                
                # If the count becomes zero, remove the entry
                if temp_counts[digit] == 0:
                    del temp_counts[digit]
                
                # Calculate permutations with this digit in the first position
                digit_perms = factorial(len(digits) - 1)
                
                # Adjust for repeated digits
                for count in temp_counts.values():
                    if count > 1:
                        digit_perms //= factorial(count)
                
                # Add to the total permutations without leading zero
                permutations_without_leading_zero += digit_perms
        
        # The total permutations is the number of permutations without leading zero
        total_permutations = permutations_without_leading_zero
    
    return total_permutations

def main():
    """
    Solve Project Euler Problem 491:
    
    We call a positive integer double pandigital if it uses all the digits 0 to 9 exactly twice 
    (with no leading zero). For example, 40561817703823564929 is one such number.
    
    How many double pandigital numbers are divisible by 11?
    """
    # The sum of all digits 0-9 appearing twice
    total_sum = 2 * sum(range(10))  # 2 * (0+1+2+...+9) = 2 * 45 = 90
    
    # Generate all possible subsets of 10 digits from the 20 digits (0-9 each appearing twice)
    digits = list(range(10))
    all_subsets = generate_combinations(digits, max_occurrences=2, max_length=10)
    
    print(f"Number of subsets with length 10: {len(all_subsets)}")
    
    # Count double pandigital numbers divisible by 11
    total_count = 0
    
    # A number is divisible by 11 if and only if the alternating sum of its digits is divisible by 11
    # For a 20-digit number, this is equivalent to:
    # (d1 + d3 + ... + d19) - (d2 + d4 + ... + d20) ≡ 0 (mod 11)
    # If we place subset S1 in odd positions and subset S2 in even positions:
    # sum(S1) - sum(S2) ≡ 0 (mod 11)
    # Since S1 and S2 partition the full set, sum(S1) + sum(S2) = 90
    # This gives us: sum(S1) - (90 - sum(S1)) ≡ 0 (mod 11)
    # Simplifying: 2*sum(S1) - 90 ≡ 0 (mod 11)
    # Or: sum(S1) ≡ 45 (mod 5.5)
    # Since sum(S1) must be an integer, this means:
    # sum(S1) = 45 + k*11/2 where k is even
    # So sum(S1) can be 45, 45±11, 45±22, ...
    
    # Count valid subsets
    valid_subsets = []
    for subset in all_subsets:
        subset_sum = sum(subset)
        # Check if the subset sum satisfies the divisibility condition
        if (2 * subset_sum - total_sum) % 11 == 0:
            valid_subsets.append(subset)
    
    print(f"Number of valid subsets: {len(valid_subsets)}")
    
    # Calculate the total number of double pandigital numbers divisible by 11
    for subset in valid_subsets:
        # Create the complement subset (the digits not in the subset)
        complement = []
        digit_counts = {}
        for d in range(10):
            digit_counts[d] = 2  # Each digit appears twice in the full set
        
        for d in subset:
            digit_counts[d] -= 1
        
        for d in range(10):
            for _ in range(digit_counts[d]):
                complement.append(d)
        
        # Check if subset and complement are the same (have the same digits with the same frequencies)
        is_same = sorted(subset) == sorted(complement)
        
        # Count permutations with subset in odd positions (no leading zero restriction)
        # and complement in even positions (can have leading zero)
        subset_perms = count_permutations(subset, allow_leading_zero=False)
        complement_perms = count_permutations(complement, allow_leading_zero=True)
        count1 = subset_perms * complement_perms
        
        # Count permutations with complement in odd positions (no leading zero restriction)
        # and subset in even positions (can have leading zero)
        complement_perms_no_leading_zero = count_permutations(complement, allow_leading_zero=False)
        subset_perms_with_leading_zero = count_permutations(subset, allow_leading_zero=True)
        count2 = complement_perms_no_leading_zero * subset_perms_with_leading_zero
        
        # If subset and complement are the same, we're double counting, so divide by 2
        total_count += count1
        
        # Print an example for the first valid subset
        if subset == valid_subsets[0]:
            print(f"\nExample for a valid subset:")
            print(f"Subset: {subset}")
            print(f"Sum of subset: {sum(subset)}")
            print(f"Complement: {complement}")
            print(f"Sum of complement: {sum(complement)}")
            print(f"(2 * sum(subset) - total_sum) % 11: {(2 * sum(subset) - total_sum) % 11}")
            print(f"Permutations of subset without leading zero: {subset_perms}")
            print(f"Permutations of subset with leading zero: {subset_perms_with_leading_zero}")
            print(f"Permutations of complement without leading zero: {complement_perms_no_leading_zero}")
            print(f"Permutations of complement with leading zero: {complement_perms}")
            print(f"Count for subset in odd positions: {count1}")
            print(f"Count for complement in odd positions: {count2}")
            print(f"Total count for this subset: {count1 + count2}")
    
    print(f"\nTotal number of double pandigital numbers divisible by 11: {total_count}")
    
    # Explanation
    print("\nExplanation:")
    print("1. A number is divisible by 11 if and only if the alternating sum of its digits is divisible by 11.")
    print("2. For a 20-digit number, this means: (d1 + d3 + ... + d19) - (d2 + d4 + ... + d20) ≡ 0 (mod 11)")
    print("3. If we place subset S1 in odd positions and subset S2 in even positions:")
    print("   sum(S1) - sum(S2) ≡ 0 (mod 11)")
    print("4. Since S1 and S2 partition the full set, sum(S1) + sum(S2) = 90")
    print("5. This gives us: 2*sum(S1) - 90 ≡ 0 (mod 11)")
    print("6. For each valid subset, we calculated:")
    print("   a. Permutations with the subset in odd positions (no leading zeros)")
    print("      and its complement in even positions (can have leading zeros)")
    print("   b. Permutations with the complement in odd positions (no leading zeros)")
    print("      and the subset in even positions (can have leading zeros)")
    print("7. We added these two counts for each valid subset to get the total.")

if __name__ == "__main__":
    main()
