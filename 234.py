N = input()
import math
import gmpy
n =   gmpy.next_prime(int(math.ceil(math.sqrt(N))))
print n
pr = [True for i in range(n+1)]
for i in range(2,n+1):
    if i*i>n:
        break
    if pr[i]:
        for j in range(i*i,n+1,i):
            pr[j] = False

primes = []
for i in range(2,n+1):
    if pr[i]:
        primes.append(i)
print primes

def sum_of_multiples(l,r,n):
    m1 = r/n
    m2 = (l-1)/n
    if m1+m2==0:
        return 0
    ans = n*(m1*(m1+1))/2 - n*(m2*(m2+1))/2
    return ans

ans = 0
pr = primes
for i in xrange(len(pr)-1):
    l1 = pr[i]
    l2 = pr[i+1]
    l3 = pr[i]*pr[i+1]
    left,right = l1*l1+1,min(N,l2*l2-1)
    ans += sum_of_multiples(left,right,l1)
    ans += sum_of_multiples(left,right,l2)
    ans -=2*sum_of_multiples(left,right,l3)
    #print ans,l1,l2,l3,left,right

print ans
