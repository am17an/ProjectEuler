import math
N = 71328803586048

def sum_of_squares_alternating(k, use):
    return (-1)**((k+use)%2)*(k*(k+1))//2

def solve(f, r):
    first = (f**2)//2

    if r == 1:
        return first

    if f % 2 == 0 or f == 1:
        r += 1

    a1 = sum_of_squares_alternating(f+r-2, f%2) - sum_of_squares_alternating(f-1, f%2)

    if r%2 == 0:
        return a1 - first
    else:
        return first - a1

    

ans = 0
MOD = 10**8
# Use integer square root to avoid floating point precision issues
sqrt_N = int(math.isqrt(N))
for i in range(1, sqrt_N + 1):
    if N%i == 0:
        ans += solve(i, N//i)%MOD
        if i != N//i:
            ans += solve(N//i, i)%MOD

        ans %= MOD

print(ans)
print(solve(81, 1))


for i in range(1, 20):
    print(1, i, solve(1, i))