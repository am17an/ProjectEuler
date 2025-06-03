def generate_fibonacci(limit):
    fib = [1, 2]
    while fib[-1] + fib[-2] <= limit:
        fib.append(fib[-1] + fib[-2])
    return fib

def count_representations(n, fib_numbers):
    def count_ways(target, index, used):
        if target == 0:
            return 1
        if target < 0 or index >= len(fib_numbers):
            return 0
        
        # Try using current Fibonacci number
        ways = 0
        if fib_numbers[index] <= target and not used[index]:
            used[index] = True
            ways += count_ways(target - fib_numbers[index], index + 1, used)
            used[index] = False
        
        # Skip current Fibonacci number
        ways += count_ways(target, index + 1, used)
        return ways
    
    used = [False] * len(fib_numbers)
    return count_ways(n, 0, used)

def main():
    # Generate Fibonacci numbers up to 200
    fib_numbers = generate_fibonacci(200)
    
    # Calculate f(n) for numbers 1 to 200
    results = []
    sum_ = 0
    for n in range(1, 201):
        f_n = count_representations(n, fib_numbers)
        sum_ += f_n
        results.append(f_n)
        print(f"f({n}) = {f_n}, sum:: {sum_}")

if __name__ == "__main__":
    main()
