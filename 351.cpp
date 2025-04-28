//use OEIS 
//

#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

// Function to calculate the sum of Euler's totient function up to N
long long sumOfTotient(long long N) {
    // Initialize phi array (phi[i] will store the value of Euler's totient function for i)
    vector<long long> phi(N + 1);

    // Initialize all values: phi[i] = i
    for (long long i = 1; i <= N; i++) {
        phi[i] = i;
    }

    // Sieve approach to calculate phi values
    for (long long p = 2; p <= N; p++) {
        // If phi[p] == p, then p is prime
        if (phi[p] == p) {
            // For a prime p, phi(p) = p-1
            phi[p] = p - 1;

            // Update phi values for all multiples of p
            for (long long i = 2 * p; i <= N; i += p) {
                // phi(i) = phi(i) * (1 - 1/p)
                phi[i] = (phi[i] / p) * (p - 1);
            }
        }
    }

    // Sum all phi values from 1 to N
    long long sum = 0;
    for (long long i = 1; i <= N; i++) {
        sum += phi[i];
    }

    return sum;
}

int main() {
    // Test cases
    cout << "Sum for N = 10: " << sumOfTotient(10) << endl;      // Should be 32
    cout << "Sum for N = 100: " << sumOfTotient(100) << endl;    // Should be 3044
    cout << "Sum for N = 1000: " << sumOfTotient(1000) << endl;  // Should be 304192

    // Calculate for 10^8 (may take some time)
    long long N = 100000000; // 10^8

    cout << "Calculating sum for N = " << N << "..." << endl;
    long long result = sumOfTotient(N);
    cout << "Sum of φ(n) from n=1 to " << N << " is: " << result << endl;

    return 0;
}
