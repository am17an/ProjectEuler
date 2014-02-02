#include "pe_utils.hpp"
#include <vector>
using namespace std;
std::vector<bool>
pe_utils::sieve(size_t n){
  vector<bool> primes(n,true);
  for(int i = 2; i*i <= n ; ++i){
    if(primes[i]){
      for(int j = i*i; j < n; j+=i)
        primes[j] =false;
    }
  }
  primes[0] = primes[1] = false;
  return primes;
}

std::vector<long long>
pe_utils::primes(size_t n){
  vector<bool> prime = sieve(n);
  vector<long long> result;
  for(int i = 0 ; i < n ; ++i){
    if(prime[i]) result.push_back((long long)i); 
  }
  return result;
}

long long 
pe_utils::fast_pow(long long base, long long exp, long long mod){
  typedef long long LL;
  LL res = 1;
  for(LL ex = exp;ex;ex>>=1){
    if(ex&1){
      res = ((res%mod)*(base%mod))%mod;
    }
    base = (base%mod)*(base%mod);
    base %=mod;
  }
  return res;
}

long long
pe_utils::gcd(long long a, long long b){
  return (b==0?a:gcd(b,a%b));
}
