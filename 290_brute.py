
def dsum(n):
    count = 0
    while n != 0:
        count += n%10
        n = int(n/10)

    return count


for i in range(10000):
    if dsum(i) == dsum(i*137):
        print(i, i%9)
