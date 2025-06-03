from functools import cache

N = 18

def digit_sum(n):
    count = 0
    while n != 0:
        count += n%10
        n //= 10

    return count

@cache
def solve(idx, carry_in, s_n, s_137n):

    if idx == N:
        if s_137n + digit_sum(carry_in) == s_n:
            return 1
        return 0

    
    ans = 0
    for digit in range(10):
        new_value = carry_in + digit*137
        new_137_n = s_137n + new_value%10
        new_carry = new_value//10

        new_sn = s_n + digit

        ans += solve(idx+1, new_carry, new_sn, new_137_n)

    return ans


print(solve(0, 0, 0, 0))

total = 0
for i in range(1000000):
    if digit_sum(i) == digit_sum(137*i):
        total+=1

print(total)