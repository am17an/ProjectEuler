from math import factorial

def generate_combinations_with_sum(digits, max_occurrences, target_length, target_sum, current_combination=None, index=0, current_sum=0, all_combinations=None):
    """
    Generate all combinations of digits where each digit can appear up to max_occurrences times,
    with a specific length and sum.
    
    Args:
        digits: List of available digits
        max_occurrences: Maximum number of times each digit can appear
        target_length: Target length of the combination
        target_sum: Target sum of the combination
        current_combination: Current combination being built
        index: Current index in the digits list
        current_sum: Current sum of the combination
        all_combinations: List to store all generated combinations
    
    Returns:
        List of all valid combinations
    """
    if current_combination is None:
        current_combination = []
    if all_combinations is None:
        all_combinations = []
    
    # If we've reached the target length, check the sum
    if len(current_combination) == target_length:
        if current_sum == target_sum:
            all_combinations.append(current_combination.copy())
        return all_combinations
    
    # If the combination is already too long, return
    if len(current_combination) > target_length:
        return all_combinations
    
    # If the current sum is already greater than the target sum, return
    if current_sum > target_sum:
        return all_combinations
    
    # If it's impossible to reach the target sum even if we add the largest digits
    remaining_slots = target_length - len(current_combination)
    max_possible_sum = current_sum + remaining_slots * 9
    if max_possible_sum < target_sum:
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
            generate_combinations_with_sum(digits, max_occurrences, target_length, target_sum,
                                         current_combination, i, current_sum + digit, all_combinations)
            # Backtrack by removing the last digit
            current_combination.pop()
    
    return all_combinations

def find_complement(combination, full_set):
    """
    Find the complement of a combination from the full set.
    
    Args:
        combination: The combination to find the complement of
        full_set: The full set of digits
    
    Returns:
        The complement of the combination
    """
    # Create a copy of the full set
    complement = full_set.copy()
    
    # Remove each digit in the combination from the complement
    for digit in combination:
        complement.remove(digit)
    
    return complement

def is_divisible_by_11(even_digits, odd_digits):
    """
    Check if a number is divisible by 11 based on the sum of digits at even and odd positions.
    
    Args:
        even_digits: List of digits at even positions
        odd_digits: List of digits at odd positions
    
    Returns:
        True if the number is divisible by 11, False otherwise
    """
    # Calculate the sum of digits at even and odd positions
    even_sum = sum(even_digits)
    odd_sum = sum(odd_digits)
    
    # Check if the absolute difference is divisible by 11
    return abs(even_sum - odd_sum) % 11 == 0

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
        # Calculate permutations with leading zero
        zero_count = digit_counts[0]
        
        # Create a new digit counts dictionary without one zero
        leading_zero_counts = digit_counts.copy()
        leading_zero_counts[0] -= 1
        
        # If there are no more zeros, remove the entry
        if leading_zero_counts[0] == 0:
            del leading_zero_counts[0]
        
        # Calculate permutations with leading zero
        permutations_with_leading_zero = factorial(len(digits) - 1)
        
        # Adjust for repeated digits
        for count in leading_zero_counts.values():
            if count > 1:
                permutations_with_leading_zero //= factorial(count)
        
        # Subtract from total
        total_permutations -= permutations_with_leading_zero * zero_count
    
    return total_permutations

def main():
    # Available digits
    digits = list(range(10))  # 0 to 9
    
    # Full set of digits (each digit appears twice)
    full_set = []
    for digit in digits:
        full_set.extend([digit, digit])
    
    # Generate all combinations with sum 45 and length 10
    sum_45_combinations = generate_combinations_with_sum(digits, max_occurrences=2, target_length=10, target_sum=45, current_sum=0)
    
    print(f"Number of combinations with sum 45 and length 10: {len(sum_45_combinations)}")
    
    # Find complements and count permutations
    total_permutations = 0
    
    # For demonstration, show an example
    if sum_45_combinations:
        example_combo = sum_45_combinations[0]
        example_complement = find_complement(example_combo, full_set)
        
        # Verify that the complement also has a sum of 45
        assert sum(example_complement) == 45, "Complement should also have a sum of 45"
        
        # Count permutations with and without leading zeros
        combo_with_leading_zero = count_permutations(example_combo, allow_leading_zero=True)
        combo_without_leading_zero = count_permutations(example_combo, allow_leading_zero=False)
        complement_with_leading_zero = count_permutations(example_complement, allow_leading_zero=True)
        complement_without_leading_zero = count_permutations(example_complement, allow_leading_zero=False)
        
        # Calculate total permutations for this example
        example_total = 0
        
        # Check if combo and complement are the same
        if sorted(example_combo) == sorted(example_complement):
            example_total = combo_without_leading_zero * combo_with_leading_zero
        else:
            # (complement in even position) * (combo in odd position) + (combo in even position) * (complement in odd position)
            example_total = (complement_without_leading_zero * combo_with_leading_zero) + (combo_without_leading_zero * complement_with_leading_zero)
        
        print(f"\nExample:")
        print(f"Combination: {example_combo}")
        print(f"Sum of combination: {sum(example_combo)}")
        print(f"Complement: {example_complement}")
        print(f"Sum of complement: {sum(example_complement)}")
        print(f"Permutations of combo with leading zero: {combo_with_leading_zero}")
        print(f"Permutations of combo without leading zero: {combo_without_leading_zero}")
        print(f"Permutations of complement with leading zero: {complement_with_leading_zero}")
        print(f"Permutations of complement without leading zero: {complement_without_leading_zero}")
        print(f"Total permutations for this example: {example_total}")
        
        # Detailed explanation of the calculation
        print("\nDetailed calculation for the example:")
        print("1. When the complement is in even positions (no leading zeros):")
        print(f"   {complement_without_leading_zero} permutations")
        print("2. When the combination is in odd positions (can have leading zeros):")
        print(f"   {combo_with_leading_zero} permutations")
        print("3. Total for complement in even, combo in odd:")
        print(f"   {complement_without_leading_zero} * {combo_with_leading_zero} = {complement_without_leading_zero * combo_with_leading_zero}")
        print("4. When the combination is in even positions (no leading zeros):")
        print(f"   {combo_without_leading_zero} permutations")
        print("5. When the complement is in odd positions (can have leading zeros):")
        print(f"   {complement_with_leading_zero} permutations")
        print("6. Total for combo in even, complement in odd:")
        print(f"   {combo_without_leading_zero} * {complement_with_leading_zero} = {combo_without_leading_zero * complement_with_leading_zero}")
        print("7. Grand total:")
        print(f"   {complement_without_leading_zero * combo_with_leading_zero} + {combo_without_leading_zero * complement_with_leading_zero} = {example_total}")
    
    for combo in sum_45_combinations:
        # Find the complement
        complement = find_complement(combo, full_set)
        
        # Count permutations with and without leading zeros
        combo_with_leading_zero = count_permutations(combo, allow_leading_zero=True)
        combo_without_leading_zero = count_permutations(combo, allow_leading_zero=False)
        complement_with_leading_zero = count_permutations(complement, allow_leading_zero=True)
        complement_without_leading_zero = count_permutations(complement, allow_leading_zero=False)
        
        # Calculate permutations for this combination
        if sorted(combo) == sorted(complement):
            # If combo and complement are the same, just count once
            total_permutations += combo_without_leading_zero * combo_with_leading_zero
        else:
            # (complement in even position) * (combo in odd position) + (combo in even position) * (complement in odd position)
            total_permutations += (complement_without_leading_zero * combo_with_leading_zero) + (combo_without_leading_zero * complement_with_leading_zero)
    
    print(f"\nTotal number of permutations: {total_permutations}")
    
    # Explanation
    print("\nExplanation:")
    print("1. We generated all combinations of digits where each digit appears at most 2 times,")
    print("   with a sum of 45 and length 10.")
    print("2. For each combination, we found its complement from the full set {0,0,1,1,...,9,9}.")
    print("3. We calculated:")
    print("   a. Permutations with the combination in even positions (no leading zeros)")
    print("      and the complement in odd positions (can have leading zeros)")
    print("   b. Permutations with the complement in even positions (no leading zeros)")
    print("      and the combination in odd positions (can have leading zeros)")
    print("4. For each combination-complement pair, we added these two counts.")
    print("5. If the combination and its complement were identical, we only counted")
    print("   the permutations once to avoid double-counting.")

if __name__ == "__main__":
    main()
