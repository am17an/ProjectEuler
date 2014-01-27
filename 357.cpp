#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;
#define MAXN 100000002
typedef long long LL;
bool prime[MAXN];
vector<LL> pr;

void sieve()
{
  for(LL i = 2 ; i < MAXN ; ++i) prime[i] = true;
  for(LL i = 2; i*i < MAXN ; ++i)
  {
    if(prime[i])
    {
      for(LL j = i*i ; j < MAXN ; j+=i)
        prime[j] = false;
    }
  }
  for(LL i = 2; i < MAXN ; ++i) if(prime[i]) pr.push_back(i); 
}

int main()
{
  sieve();
  long long res = 0;
  for(LL i = 1 ; i < MAXN; ++i)
  {
    bool fl = true;
    if(prime[i] && i>2) continue;
    if(!prime[i+1]) continue;
    for(LL j = 1 ; j*j <= i; ++j)
    {
      if(i%j == 0)
      {
        if(!prime[j+ i/j])
        {
          fl = false;
          break;
        }
      }
    }
    if(fl) {  
      res += i;
    }
  }
  cout << res << endl;
}
