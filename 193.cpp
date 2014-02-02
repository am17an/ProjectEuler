#include <iostream>
#include <cstdio>
#include <cassert>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#include "pe_utils.hpp"

typedef long long LL;
using namespace std;

LL limit = 1LL<<50;

LL res = 0;

vector<long long> primes;

void dfs(int card, LL val,int curr){
  if(val<0) return;
  if(curr>=primes.size()) return;
  if(val>=limit || curr>=primes.size()) return;
  cout << card << " " << val << " " << curr << " " << limit << endl;
  assert(curr < primes.size()); 
  // take
  if(val*primes[curr]<limit){
    if(val*primes[curr]<0) return;
    
    cout << val*primes[curr] << " " ;
    res += (card%2==0?((limit/val)):-(limit/val));
    dfs(card+1,val*primes[curr],curr+1);
  }
  else{
    return;
  }
  // You can also NOT take it..
  dfs(card, val,curr+1);

}

int main(){
  primes = pe_utils::primes(1<<25);
  cout << primes.size() << endl;
  for(int i = 0 ; i < primes.size() ; ++i) primes[i] = primes[i]*primes[i];
  for(int j=primes.size();j>=primes.size()-10;j--) cout << primes[j] << endl;
  dfs(0,1,0);
  cout << res << endl;
}

