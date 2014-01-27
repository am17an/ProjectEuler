#brute force
from copy import deepcopy

r = set()
def dfs(b,w,curr):
    if b + w == 0:
       f = ''.join(sorted(curr))
       r.add(f)

    for i in range(1,b+1):
        for j in range(1,w+1):
            if i+j>0:
                newcurr = deepcopy(curr)
                newcurr.append(i*"B" + j*"W" + ",")
                dfs(b-i,w-j,newcurr)

b = input()
w = input()

dfs(b,w,[])

print r
print len(r)
