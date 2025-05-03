def generate_fibonacci(limit):
    """Generate Fibonacci numbers up to limit."""
    fibs = [1, 2]
    while fibs[-1] + fibs[-2] <= limit:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def get_zeckendorf_representation(n, fibs):
    """Get the Zeckendorf representation of n."""
    if n == 0:
        return []
    
    result = []
    i = len(fibs) - 1
    
    while n > 0:
        if fibs[i] <= n:
            result.append(fibs[i])
            n -= fibs[i]
            i -= 1
            if i >= 0:
                i -= 1  # Skip one Fibonacci number to ensure non-consecutive
        else:
            i -= 1
    
    return result


fibs = generate_fibonacci(10**17)


count = 0


for fib in range(101): 
    count = 0
    if fib in fibs:
        print("Fib", fib)
    for i in range(fib):
        count += len(get_zeckendorf_representation(i, fibs))

    print(fib, count)


print(count)
