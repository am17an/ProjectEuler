from math import log
def find_possible_values(L, until):

    L1 = log(2, 10)
    L2 = log(2, 10)

    D1 = log(L, 10)
    D2 = log(L+1, 10)

    count = 0
    for i in range(1, 200000000):
        d1 = i*L1 - D1
        d2 = i*L1 - D2

        if int(d1) != int(d2):
            count += 1
            #print(i, count)

            if count == until:
                print("Found", until, "values", i)
                break
        else:
            #how far are we from the next integer
            diff = int(d1) - d1
            i += diff/L1

    print(count)


find_possible_values(123, 678910)