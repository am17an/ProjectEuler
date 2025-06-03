import sympy

if __name__ == '__main__':
    p = 1009
    q = 3643
    n = p * q
    phi_n = n - p - q + 1
    result = 0
    min_res = 9999999999999
    for e in range(1, phi_n):
        if sympy.gcd(e, phi_n) != 1:
            continue
        num_unconcealed = (sympy.gcd(e-1, p-1) + 1) * (sympy.gcd(e-1, q-1) + 1)
        if num_unconcealed < min_res:
            min_res = num_unconcealed
            result = e
        elif num_unconcealed == min_res:
            result += e
    print("The result is: {0}".format(result))
