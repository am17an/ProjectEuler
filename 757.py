def find_special_numbers(limit):
    results = set()
    x = 1
    while True:
        x_term = x * (x + 1)
        if x_term * x_term > limit:
            break
        y = 1
        while True:
            val = x_term * y * (y + 1)
            if val > limit:
                break
            results.add(val)
            y += 1
        x += 1
    return sorted(results)

print(len(find_special_numbers(int(1e14))))