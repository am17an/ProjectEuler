def compute_f(n_max):
    f = [0.0] * (n_max + 1)
    f[0] = 0.0
    if n_max >= 1:
        f[1] = 1.0

    for n in range(2, n_max + 1):
        total = 0.0
        for i in range(n):
            left = f[i - 1] if i >= 1 else 0.0
            right = f[n - i - 2] if (n - i - 2) >= 0 else 0.0
            total += 1 + left + right
        f[n] = total
    return f

def f(n):
    return 2 * n - bin(n).count('1')

# Compute and print f(0) to f(14)
f_values = compute_f(14)
for n, val in enumerate(f_values):
    print(f"f({n}) = {val:.10f}", f(n))
