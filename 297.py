from functools import lru_cache

@lru_cache
def a(n):
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1
    if n == 3:
        return 2

    return 2*a(n-1) + a(n-2) - 2*a(n-3) - a(n-4)



@lru_cache
def fibs(n):
    if n == 0:
        return 1
    if n == 1:
        return 2
    
    return fibs(n-1) + fibs(n-2)

def solve(n, max_fib):
    print(n, max_fib)
    if n <= 3:
        return a(n)

    count = 0 
    fibs_list = [fibs(i) for i in range(max_fib)]
    for fib in fibs_list[::-1]:
        if n >= fib:
            print("Using fib ", fib)
            last_max = fibs_list.index(fib)
            count += (n - fib) + fib + solve(n - fib, 50)
            print(count)
            n -= fib
            return count + solve(n, max_fib)



print(fibs(100) < 10**17)
print(solve(10**6, 100))