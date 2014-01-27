M = 1234567891011


def matrixMul(a,b):
    c = [ [0,0], [0,0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                c[i][j] += a[i][k]*b[j][k]
                c[i][j] %= M
    return c

def fib(exp):
  base = [[1,1],[1,0]]
  res = [[1,0],[0,1]]
  while exp:
      if exp%2 != 0:
          res = matrixMul(res,base)
      base = matrixMul(base,base)
      exp/=2
  return res[0][0]

#done till here 
# call -1
import gmpy

a = gmpy.next_prime(10**14)

res = 0
for i in range(100000):
   res += fib(a-1) 
   res %= M
   a = gmpy.next_prime(a)

print res
