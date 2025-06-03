
N = 6
maxX = 2**N
maxY = 2**N

originX = 2**(N-1)
originY = 2**(N-1)

def incircle(x, y):
    return (x-originX)**2 + (y-originY)**2 <= 2**(2*N-2)

def solve(x, y, l):

    if l == 1:
        #return 0
        if incircle(x, y):
            return 2
        else:
            return 2

    r = l//2

    all_black = True 
    all_white = True 
    #print("Searching pixels", x-r, x+r, y-r, y+r)
    points = [(x-r, y+r-1), (x-r, y-r), (x+r-1, y+r-1), (x+r-1, y-r)]

    #for xp in range(x-r, x+r):
    #    for yp in range(y-r, y+r):
    #        if incircle(xp, yp):
    #            all_white = False
    #        else:
    #            all_black = False

    if not(all(incircle(p[0],p[1]) for p in points)):
        all_black = False

    if not(all(not incircle(p[0],p[1]) for p in points)) or l == maxX:
        all_white = False

    #points = [(x+r, y+r), (x+r, y-r), (x-r, y-r), (x-r, y+r)]
    if all_black or all_white:
        return 2

    a1 = solve(x + l//4, y + l//4, r)
    a2 = solve(x - l//4, y + l//4, r)
    a3 = solve(x + l//4, y - l//4, r)
    a4 = solve(x - l//4, y - l//4, r)

    #print("ans", x, y, l, a1, a2, a3, a4)

    return 1 + a1 + a2 + a3 + a4
    


for i in range(24, 25):
    N = i
    maxX = 2**N
    maxY = 2**N

    originX = 2**(N-1)
    originY = 2**(N-1)

    print(solve(originX, originY, maxX))