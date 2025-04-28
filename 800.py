from math import log
def primes(N):
    sieve = [True] * (N+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5)+1):
        if sieve[i]:
            sieve[i*i:N+1:i] = [False] * len(range(i*i, N+1, i))
    return [i for i in range(N+1) if sieve[i]]


def main(): 
    N = 800800

    MaxPrime = 30000000

    current_primes = primes(int(MaxPrime))

    left, right = 0, 1
    count = 0

    for i in range(len(current_primes)):
        #binary search for the rightmost prime that satisfies the condition 
        #print("Doing for ", current_primes[i])
        left, right = i+1, len(current_primes)-1
        while left <= right:
            mid = (left + right) // 2
            if current_primes[i] * log(current_primes[mid]) + current_primes[mid] * log(current_primes[i]) <= N * log(N):
                left = mid + 1
            else:
                right = mid - 1
        count += right - i 

    print(count)


if __name__ == "__main__":
    main()

    