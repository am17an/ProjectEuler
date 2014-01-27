#include <cstring>
#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#define FOR(i,n) for(int i = 0 ; i < (int)n ; ++i)
using namespace std;
const int MAXN = 15;

int dp[MAXN][(1<<MAXN)];

int mat[MAXN][MAXN];

int dfs(int row, int mask)
{
  if(row == MAXN - 1)
  {
    // Check which bit is not set
    for(int i = 0 ; i < MAXN ; ++i)
    {
      if((mask&(1<<i))!=0) continue;
      return mat[row][i];
    }
  }

  int & res = dp[row][mask];
  if(res != -1) return res;
  res = 0;
  for(int i = 0 ; i < MAXN ; ++i)
  {
    if((mask&(1<<i))!=0) continue;
    int newmask = mask | (1<<i);
    res = max( res, dfs(row+1,newmask) + mat[row][i]);
  }
  return res;
}

int main()
{
  FOR(i,MAXN) FOR(j,MAXN) cin >> mat[i][j];
  memset(dp,-1,sizeof(dp)); 
  cout << dfs(0,0) << endl;
}
