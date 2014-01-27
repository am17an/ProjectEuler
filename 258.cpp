#define N 2000
#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#define FOR(i,n) for(int i =0 ; i < n ; ++i)
using namespace std;
typedef long long LL;

LL mat[N][N];
LL mat2[N][N];
LL ans[N][N];

int M = 20092010;
inline LL safe(LL x, LL y)
{
  if(x*y >= M)
  {
    return (x*y)%M;
  }
  return (x*y);
}
void matMul(LL mat[N][N], LL mat2[N][N])
{
  FOR(i,N) FOR(j,N) ans[i][j] = 0;
  FOR(i,N) FOR(j,N) FOR(k,N)  ans[i][j] += safe(ans[i][k],ans[k][j]);
  FOR(i,N) FOR(j,N) mat[i][j] = ans[i][j]; 
}

void matExp(LL exp)
{
  for(LL ex = exp;ex;ex>>=1)
  {
    cout << ex << endl;
    if(ex&1)
    {
      matMul(mat,mat2);
    }
    matMul(mat2,mat2);
  }
}
int main()
{
  // mat2 is your base
  cout <<" START " << endl;
  FOR(i,N-1) mat2[i][i+1] = 1;
  mat2[0][1998] = 1; mat2[0][1999] = 1;
  FOR(i,N) mat[i][i] = 1; 
  int res = 0;
  cout << "HERE" << endl;
  matExp(1);
  cout << "AGAIN HERE" << endl;
  for(int i = 0 ; i < 2000 ; ++i)  
      res += mat[0][i];
  cout << res << endl;
}
