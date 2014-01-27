
def gcd(a,b):
    if b == 0:
        return a
    return gcd(b,a%b)

def term(num):
    while num%2 == 0:
        num/=2
    while num%5 == 0:
        num /=5
    if num > 1:
        return False
    return True
N = 100
import math
resi = 0
for i in range(5,N+1):
    res = float('-inf')
    num = 1
    for j in range(1,N):
        part = i/(j+0.)
        if j*math.log(part) > res :
            res = j* math.log(part)
            num = j
    print i,(i/(num+0.))**num
    if term(num/gcd(i,num)):
        resi += -i
    else:
        resi += i

print resi
