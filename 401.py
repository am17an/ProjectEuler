def getDivisors(n):
     r = set()
     for i in xrange(1,n):
             if i*i>n:
                     break
             if n%i==0:
                     r.add(i)
                     r.add(n/i)
     return r

def euler400(n):
    f = list(getDivisors(n))
    f.sort()
    print f

euler400(100)
