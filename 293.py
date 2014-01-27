#!/usr/bin/env python

import gmpy

#do for powers of 2
prime = [True for i in xrange(100000)]

for i in xrange(2,100000):
    if prime[i]:
        for j in xrange(i*i,100000,i):
            prime[j] = False
pr = []
for i in xrange(2,100000):
    if prime[i]:
        pr.append(i)

candidates = []
print pr[:10]

def dfs(current, pos):
    if current > 1e+9:
        return
    candidates.append(current)
    dfs(current*pr[pos],pos)
    dfs(current*pr[pos],pos+1)

dfs(1,0);
candidates = list(set(candidates))
candidates.sort()
candidates = candidates[1:]
print candidates[:10]
res = set()
for i in candidates:
    curr = i+2
    while 1:
        if gmpy.is_prime(curr):
            res.add(curr-i)
            break
        else:
            curr += 1

print sum(res) 
