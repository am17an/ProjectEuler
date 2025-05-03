
import itertools,math

def number_of_doubles(pand):
    doubles = 0
    for x in range(0,10):
        if pand.count(str(x)) == 2:
            doubles += 1
    return doubles
    
def compute():
    total = 0
    poss = set(itertools.combinations("00112233445566778899", 10))
    fac_9 = int(math.factorial(9))
    fac_10 = int(math.factorial(10))
    for x in poss:
        zero_count = x.count('0')
        x_count = sum([int(y) for y in x])
        
        if zero_count == 0:
            if (2*x_count - 90) % 11 == 0:
                num_doubles = number_of_doubles(x)
                total += (fac_10/(2**num_doubles))*(fac_10/(2**num_doubles))
        
        if zero_count == 1:
            if (2*x_count - 90) % 11 == 0:
                num_doubles = number_of_doubles(x)
                total += (9*fac_9/(2**num_doubles))*(fac_10/(2**num_doubles))
        
        if zero_count == 2:
            if (2*x_count - 90) % 11 == 0:
                num_doubles = number_of_doubles(x)
                total += (8*fac_9/(2**num_doubles))*(fac_10/(2**num_doubles))
    return int(total)

print(compute())
