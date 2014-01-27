cap = [ set() for i in range(19)]
from fractions import Fraction
cap[1].add(Fraction(60,1))

def paralell(x,y):
    return Fraction(x + y)
def series(x,y):
    return Fraction(x*y,x+y)

r = set()
for i in range(2,19):
    print "Processing ",i
    for j in range(1,i):
        for val in cap[j]:
            for val2 in cap[i-j]:
                r.add(paralell(val,val2))
                r.add(series(val,val2))

print len(r)
