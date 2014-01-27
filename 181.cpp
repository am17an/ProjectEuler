#include <cstring>
#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

typedef long long LL;

LL dp[64][64];
LL groups[64][44][64][44];
#define LEN 100
int BLACKS,WHITES;
LL solve(int b, int rb){
  if(rb == 0) return 1;
  if(rb<0) return 0;

  LL &res = dp[b][rb];

  if(res!=-1) return res;
  res = 0;
  for(int i = b ; i<=rb ; ++i){
    res += solve(i,rb-i);
  }
  return res;
}

LL solveG(int b,int w, int rb, int rw){
  if(rw+rb == 0) return 1;
  if(rw <0 || rb<0) return 0;

  LL &res = groups[b][w][rb][rw];
  if(res!=-1) return res;
  res = 0;
  for(int i = b ; i <= rb ; ++i)
      res += solveG(i,w,rb-i,rw-w);
  for(int j = w; j<= rw; ++j)
      res += solveG(b,j, rb-b,rw-j);
  return res;
}
int main(){
  memset(dp,-1,sizeof(dp));
  memset(groups,-1,sizeof(groups));
  LL res = 0;
  cin >> BLACKS >> WHITES ; 
  for(int i = 0 ; i <= BLACKS; ++i)
    for(int j = 0 ; j <= WHITES ; ++j){
      res += solve(1,i)*solve(1,j)*solveG(1,1,BLACKS-i,WHITES-j);
    }
  cout << solveG(1,1,3,3) << endl;
  cout << res << endl;
}
