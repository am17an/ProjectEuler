#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#include "pe_utils.hpp"

using namespace std;
typedef long long LL;

int main(){
  vector<LL> primes = pe_utils::primes(10000000);
  LL r = 0;
  for(int i = 0 ; i < primes.size() ; ++i) {
    if(primes[i]!=2 && primes[i]!=5){
      LL p = primes[i];
      r += pe_utils::fast_pow(10,p-2,p);
    }
  }
  cout << r << endl;
}

