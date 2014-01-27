from math import ceil
def ceil(n):
    if n%2!=0:
        return n/2+1
    return n/2

res = 0
DIGS = 4
for i in range(10**(DIGS-1), 10**DIGS):
    s = map(int,str(i))
    if s[0] +s[1] == s[2] + s[3]:
        print s
        print i
        res += i

print res
