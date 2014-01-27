#include <set>
#include <iostream>
#include <vector>

using namespace std;
vector<bool> prime(24002,true);
vector<int> sieve(size_t n)
{
  for(int i = 2; i*i<=n; ++i)
  {
    if(prime[i])
      for(int j = i*i;j<n;j+=i) prime[j] = false;
  }
  vector<int> pr;
  for(int i = 2; i < n ; ++i) if(prime[i]) pr.push_back(i);
  return pr;
}
vector<pair<int, int> > factor_sums[24002];
int best[12002];
#define MP make_pair

int main()
{
  for(int i = 2; i <= 12001; ++i) best[i] = 1e+9;
  vector<int> f = sieve(24000);
  //for(int i = 0 ; i < f.size() ; ++i) factor_sums[f[i]].push_back(MP(f[i],1));
  factor_sums[2].push_back(MP(2,1));
  factor_sums[3].push_back(MP(3,1));
  for(int i = 4; i <= 24000 ; ++i)
  {
    // factorize
    factor_sums[i].push_back(MP(i,1));
    for(int j = 2 ; j*j<=i ; ++j)
    {
      if(i%j == 0)
      {
        for(int k = 0 ; k < factor_sums[j].size() ; ++k)
        {
          for(int l = 0 ; l < factor_sums[i/j].size() ; ++l)
          {
            if(factor_sums[j][k].first + factor_sums[i/j][l].first <=i)
            {
              factor_sums[i].push_back(MP(factor_sums[j][k].first + factor_sums[i/j][l].first,
                                            factor_sums[j][k].second + factor_sums[i/j][l].second));
              int n1= i - factor_sums[j][k].first - factor_sums[i/j][l].first;
              if(factor_sums[j][k].second + factor_sums[i/j][l].second + n1 <=12000)
              best[factor_sums[j][k].second + factor_sums[i/j][l].second + n1] = min(
                  i, best[factor_sums[j][k].second + factor_sums[i/j][l].second + n1]);
            }
          }
        }
      }
    }
  }
  set<int> res;
  for(int i = 2; i <=12000; ++i) res.insert(best[i]);
  int r = 0;
  for(set<int>::iterator it = res.begin(); it!= res.end(); ++it) r +=*it;
  cout << r << endl;
}

