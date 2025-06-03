
from sympy import primefactors,lcm

def divisibility_streak(n):
    streak = 1
    while True:
        if (n+streak-1)%streak != 0:
            break
        streak += 1
    return streak - 1

def create_number(n):
    current_number = 2
    for i in range(2, n+1):
        current_number = lcm(i, current_number)
    
    return current_number


total = 0
for i in range(1, 32):
    p1 = create_number(i)
    p2 = create_number(i+1)

    total += (4**i)//p1 - (4**i)//p2

    print(i, p1, p2)

print(total)

