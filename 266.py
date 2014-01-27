prime = [True for i in range(190)]
pr = []

for i in range(2,190):
    if i*i>=190: 
        break
    if prime[i]:
        for j in range(i*i,190,i):
            prime[j] = False
for i in range(2,190):
    if prime[i]:
        pr.append(i)
r = reduce(lambda x,y:x*y,pr,1)

from math import sqrt, floor

target = floor(sqrt(r))

def make(f):
    A = []
    for i in xrange((1<<21)):
        res = 1
        for j in xrange(21):
            if i&(1<<j) != 0:
                res *= f[j]
        A.append(res)
    return A

A = make(pr[:21])
B = make(pr[21:])
A.sort()
B.sort()


closest = 1e+50
res = 0
from bisect import bisect_right,bisect_left

for i in xrange(1<<21):
    if A[i]>target:
        break # this basically means no other case will be good enough
    v = target/A[i]
    pos = bisect_right(B,v)
    if pos!=len(B):
        if target - B[pos]*A[i] >=0:
            if target - B[pos]*A[i] < closest:
                closest =  target - B[pos]*A[i] 
                res = B[pos]*A[i]
    if pos>0:
        pos -=1
    if pos!=len(B):
        if target - B[pos]*A[i] >=0:
            if target - B[pos]*A[i] < closest:
                closest =  target - B[pos]*A[i] 
                res = B[pos]*A[i]

    #search left and right for something? 

print "%16d"%(res%long(1e+16))

