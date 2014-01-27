#!/usr/bin/python

N = 9
ans = [[0 for i in range(N)] for j in range(N)]
res = [[0 for i in range(N)] for j in range(N)]
base = [[0 for i in range(N)] for j in range(N)]

def matMul(a,b):
    ans = [[0 for i in range(N)] for j in range(N)]
    for i in xrange(N):
        for j in xrange(N):
            for k in xrange(N):
                ans[i][j] += (a[i][k]*b[k][j])%(int(1e+9))
    return ans

def matPow(exp):
    res = [[0 for i in range(N)] for j in range(N)]
    for i in range(N):
        res[i][i] = 1;
    base = [[0 for i in range(N)] for j in range(N)]
    base[0] = [1 for i in range(N)]
    for i in range(1,N-1):
        base[i][i-1] = 1
    
    while exp:
        if exp%2!=0:
            res = matMul(res,base)
        base = matMul(base,base)
        exp/=2
    return res

def PP(a):
    for i in range(N):
        print a[i]

res = 0
for i in range(1,18):
    res += matPow(13**i)[0][0]
    res %= int(1e+9)

print res
