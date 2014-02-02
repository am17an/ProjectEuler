#ifndef pe_utils_hpp
#define pe_utils_hpp

#include <vector>
struct pe_utils{
  static std::vector<bool> sieve(size_t n);
  static std::vector<long long> primes(size_t n);
  static long long fast_pow(long long , long long , long long);
  static long long gcd(long long a, long long b);
};

#endif


