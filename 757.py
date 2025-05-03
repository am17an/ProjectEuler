
squares = []
for i in range(1, 1000):
    squares.append(i*i)


cumsums = []
for i in range(len(squares)):
    for j in range(i, len(squares)):
        cumsums.append(squares[i] + squares[j])



cumsums = sorted(cumsums)
count = 0
for i in range(1, len(cumsums)):
    if cumsums[i] - cumsums[i-1] == 1:
        print(cumsums[i], cumsums[i-1])
        count += 1

print(count)

        
