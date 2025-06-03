from functools import cache


@cache
def solve(n, face, seen, do_pair):

    if n == 1:
        if seen == 1:
            return 1/13.0
        return 0

    current_prob = (4-seen+1)/(52-n+1)
    #print("CurrentProb", current_prob, seen, n)


    if do_pair:
        return current_prob*solve(n-1, face, seen-1, False)
    else:
        prob = 0.
        for i in range(13):
            if i == face:
                continue
            for j in range(1, 5):
                prob += current_prob*solve(n-1, i, j, False)
        return prob



prob = 0.
ans = 0
for n in range(2, 4):
    prob = 0.
    for face in range(13):
        for seen in range(2, 5):
            prob += solve(n, face, seen, True)

    print(n, prob)
    ans += n*prob


print(solve(3, 3, 4, True))
print(prob)