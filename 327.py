
from functools import cache

def solve(rooms, C):
    if C >= rooms+1:
        return rooms+1

    next = solve(rooms-1, C)
    trips = (next-C+1)//(C-2)
    left_over = (next-C+1)%(C-2)

    #print(next, trips, left_over, rooms, C)
    #(6 - 3 + 3)

    if trips == 0:
        ans = C+next-C+3
    elif left_over != 0:
        ans = (trips+1)*C + left_over + 2
    else:
        ans = (trips+1)*C

    return ans


total = 0

for i in range(3, 41):
    total += solve(30, i)

print(total)
#print(solve(8, 8))