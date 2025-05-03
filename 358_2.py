from collections import deque

def last_k_digits_of_fraction(n, k=10):
    d = n + 1
    carry = 0
    last_digits = []

    for _ in range(n):
        carry = carry * 10 + 9
        digit = carry // d
        last_digits.append(digit)
        carry = carry % d

    return last_digits

n = 72509890
q = last_k_digits_of_fraction(n)
print("Last 10 digits:", sum(q), q[:11], q[-5:])
