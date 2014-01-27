n = 1000
r = 0
squares = [i*i for i in range(1,100)]
for i in range(1,n):
    q = 0
    for j in str(i):
        q += int(j)*int(j)
    if q in squares:
        print i
        r += i

print r
