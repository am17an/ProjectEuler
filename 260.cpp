#include <cstring>
#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

int N=100;
int dp[101][101][101];

int dfs(int x,int y,int z){
  if(dp[x][y][z] != -1){
    return dp[x][y][z];
  }
  if(x+y+z == 0) return 0;
  int &res = dp[x][y][z];
  for(int i = 1;i<=x;++i)
    if(dfs(x-i,y,z) == 0) {res = 1; return res;}
  for(int i = 1;i<=y;++i)
    if(dfs(x,y-i,z) == 0) { res = 1; return res;}
  for(int i = 1;i<=z;++i)
    if(dfs(x,y,z-i) == 0) { res = 1; return res;}

  for(int i = 1;i<=min(x,y); ++i)
    if(dfs(x-i,y-i,z) == 0) { res = 1; return res;}
  for(int i = 1;i<=min(x,z); ++i)
    if(dfs(x-i,y,z-i) == 0) { res = 1; return res;}
  for(int i = 1;i<=min(y,z); ++i)
    if(dfs(x,y-i,z-i) == 0) { res = 1; return res;}
  for(int i=1;i<=min(x,min(y,z)) ; ++i)
    if(dfs(x-i,y-i,z-i) == 0) { res =1 ; return res;}
  res =0; 
  return res; 
}

int main(){
  memset(dp,-1,sizeof(dp)); dp[0][0][0] = 0;
  long long r = 0;
  int curr = 0;
  vector<int> v;
  for(int x=0;x<=N;++x){
    for(int y=x;y<=N;++y)
      for(int z=y;z<=N;++z)
        if(dfs(x,y,z) == 0){
          r += (x+y+z);
          int newCur = x+y+z;
          cout << x << " " << y << " " << z << " " << newCur << endl;
          curr = newCur;
        }
  }
  cout << r << endl;

}
