

def d(n):
    count = 0
    while n != 0:
        count += n%10
        n //= 10

    return count


for i in range(1, 10000):
    if d(i) == d(137*i):
        print(i, i%9, (137*i)%9)
    if i%9 == 0 and not (137*i)%9 == 0:
        print("Hello", i)