f = []
N = 8
for i in range(0,(1<<N)):
    f.append(str.zfill(bin(i)[2:],N))
mat = [[] for j in range(1<<N)]

for i in range((1<<N)):
    for j in range((1<<N)):
        if f[i][1:] == f[j][:-1] and i!=j:
            mat[i].append(j)

used = set()
r = set()
def dfs(curr,s):
    if len(used)==(1<<N) - (N-1):
        r.add(s)
    for i in xrange(len(mat[curr])):
        if not mat[curr][i] in used:
            used.add(mat[curr][i])
            dfs(mat[curr][i], s +f[mat[curr][i]][-1])
            used.remove(mat[curr][i]) 

used.add(0)
dfs(0,f[0])
res = 0
for j in r:
    jj = set()
    for i in xrange(N,len(j)):
        jj.add(j[i-N:i])
    k = 1
    for i in xrange((1<<N)-(N-1), (1<<N)):
        jj.add(j[i:] + j[:k])
        k+=1
    if len(jj) == (1<<N) -1:
        res += int(j,2)
print res
