# Recursive implementation of a_n with memoization
memo_a = {1: 1}
def closed_form(n):
    if n in memo_a:
        return memo_a[n]
    
    if n % 2 == 0:  # Even case: a_{2n} = 2*a_n
        result = 2 * closed_form(n // 2)
    else:  # Odd case: a_{2n+1} = a_n - 3*a_{n+1}
        result = closed_form(n // 2) - 3 * closed_form(n // 2 + 1)
    
    memo_a[n] = result
    return result

def S_n(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    if n%2 == 0:
        return 4 - closed_form(n//2)
    else:
        return S_n(n-1) + closed_form(n)

s = 0
for i in range(1, 100):
    s += closed_form(i)
    print(i, closed_form(i), "Ours:", S_n(i), "Correct:", s)

print(S_n(int(1e12)))