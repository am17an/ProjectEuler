res = 0
s = 1
r = 1
from math import floor as floor
for i in range(2,16):
    s+=i
    r*=i**i
    q= pow((i/(s+0.)),s)*(r)
    print i,q 
    res += floor(q)
print res
