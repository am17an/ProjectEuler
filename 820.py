def find_nth_digit(x, n):
    """
    Find the nth digit in the fractional part of 1/x.
    If the digit doesn't exist (n exceeds the length of the expansion), return 0.
    
    Args:
        x: The denominator in the fraction 1/x
        n: The position of the digit to find (1-indexed)
    
    Returns:
        The nth digit in the fractional part, or 0 if it doesn't exist
    """
    if n <= 0:
        return 0
    
    # Handle the special case where x is 1
    if x == 1:
        return 0
    
    # Dictionary to store the position where each remainder first appears
    remainders = {}
    
    # Initialize variables
    remainder = 1  # Start with numerator 1
    position = 0
    
    # Store digits of the decimal expansion
    digits = []
    
    # Perform long division
    while remainder != 0 and remainder not in remainders:
        remainders[remainder] = position
        remainder *= 10
        digits.append(remainder // x)
        remainder %= x
        position += 1
    
    # If remainder is 0, the decimal expansion terminates
    if remainder == 0:
        if n <= len(digits):
            return digits[n-1]
        else:
            return 0
    
    # Find the start of the repeating part
    start_repeat = remainders[remainder]
    
    # Calculate the period length
    period_length = position - start_repeat
    
    # Handle non-repeating part
    if n <= start_repeat:
        return digits[n-1]
    
    # Handle repeating part
    adjusted_n = (n - start_repeat - 1) % period_length + start_repeat
    return digits[adjusted_n]

def get_period_length(x):
    """
    Find the length of the repeating part in the decimal expansion of 1/x.
    
    Args:
        x: The denominator in the fraction 1/x
    
    Returns:
        The length of the period, or 0 if the decimal terminates
    """
    if x == 1:
        return 0
    
    # Dictionary to store the position where each remainder first appears
    remainders = {}
    
    # Initialize variables
    remainder = 1
    position = 0
    
    # Perform long division until we find a repeating remainder or termination
    while remainder != 0 and remainder not in remainders:
        remainders[remainder] = position
        remainder = (remainder * 10) % x
        position += 1
    
    # If remainder is 0, the decimal expansion terminates
    if remainder == 0:
        return 0
    
    # The period length is the current position minus the position 
    # where the remainder was first seen
    return position - remainders[remainder]

# Example usage
if __name__ == "__main__":
    # Test case: 1/7 = 0.142857142857... (period 6)

    count = 0
    for i in range(1, 10**7):
        print("Doing ", i)
        if i%100000 == 0:
            print("Done ", i)
        count += find_nth_digit(i, 10**7)

    print(count)

