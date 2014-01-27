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

vector<LL> cubes;

int main(){
  vector<bool> prime = pe_utils::sieve(1000000);
  LL prev = 1;
  int res = 0;
  for(LL i =2 ; ;++i){
    LL curr = i*i*i;
    if (curr-prev >= 1000000) break; 
    if(prime[curr-prev]) res++;
    prev = curr;
  }
  cout << res << endl;
}


