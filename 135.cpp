#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#include <sstream>
#include "pe_utils.hpp"

using namespace std;
typedef long long LL;
string toString(int x){
  stringstream ss;
  ss << x;
  string y;
  ss >> y;
  return y;
}

LL modular_inverse(LL a, LL p){
  return pe_utils::fast_pow(a,p-2,p);
}


LL pows[] = {1,10,100,1000,10000,100000,1000000};
int main(){
  vector<long long> prime = pe_utils::primes(1500000);
  long long r = 0;
  for(int i = 3; i < prime.size() ; ++i){
    if(prime[i-1] > 1000000) break;
    int digs = toString(prime[i-1]).size();
    LL p = pows[digs]%prime[i]; 
    LL ans = (modular_inverse(p,prime[i])%prime[i]) * ((prime[i] - prime[i-1])%prime[i]);
    ans %= prime[i];
    cout << ans*pows[digs] + prime[i-1] << endl;
    r += ans*pows[digs] + prime[i-1];
     
  }
  cout << r << endl;
}
