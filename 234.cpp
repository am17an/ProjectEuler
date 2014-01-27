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
  LL N = 10;
  vector<LL> pr = pe_utils::primes(ceil(sqrt(N)));
  LL res = 0;
  for(int i = 0 ; i < pr.size() ; ++i) cout << pr[i] << endl;
  for(int i = 0 ; i < pr.size()-1 ; ++i){
    // pr[i]*pr[i] , 
    LL l = pr[i]*pr[i]+1;
    LL r = min(N,pr[i+1]*pr[i+1]-1);
    // Multiples of pr[i];
    LL mp1 = r/pr[i] - (l-1)/pr[i];
    LL mp2 = r/pr[i+1] - (l-1)/pr[i+1];
    // Multiples of both of them?
    LL lcm = pr[i]*pr[i+1];
    LL intersection = r/lcm - (l-1)/lcm;
    cout << mp1 << " " << mp2 << " " << intersection << endl;
    res += pr[i]*(mp1*(mp1+2))/2 + pr[i+1]*(mp2*(mp2+1))/2 - lcm*(intersection*(intersection+1));
  }
  cout << res << endl;
}

