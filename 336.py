from functools import lru_cache,cache
from itertools import permutations

target = "ABCDEFGHIJK" 

@cache
def calculate_no(perm):
    target = "ABCDEFGHIJK" 
    #print(perm)

    if perm == target:
        return 0
    
    to_change = "A"
    for i, letter in enumerate(target):
        if perm[i] != letter:
            to_change = letter
            index = i
            break 

    letter_index = perm.index(to_change)
    #reverse yourself 

    if letter_index == len(target) - 1:
        if index == 0:
            return 1 + calculate_no(perm[::-1])
        else:
            return 1 + calculate_no(perm[:index] + perm[index:][::-1])
    else:
        #reverse till the end
        return 1 + calculate_no(perm[:letter_index] + perm[letter_index:][::-1])


cal = {}

for i, perm in enumerate(permutations(target)):
    if i%100000 == 0:
        print("Done with", i)
    p = ''.join(perm)
    m = calculate_no(p)

    if m not in cal:
        cal[m] = []
    cal[m].append(p)

#calculate_no("ABDECF")

a = max(cal.keys())
print(sorted(cal[a])[2010], len(cal[a]))
