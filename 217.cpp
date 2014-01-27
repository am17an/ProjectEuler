#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <cstring>
#include <algorithm>

using namespace std;
typedef long long LL;
int M = 14348907;

int DIGS = 1;
LL dp[48][216];
LL sum[48][216];
int pows[48];

bool first(int i){
  int ceil = (DIGS%2!=0?DIGS/2+1:DIGS/2);
  return (i<=ceil);
}
bool last(int i){
  int ceil = (DIGS%2!=0?DIGS/2+1:DIGS/2);
  return (i>ceil);
}
LL solve(){
  memset(dp,0,sizeof(dp));
  memset(sum,0,sizeof(sum));
  dp[0][0] = 1;
  pows[0] = 1;
  for(int i = 1; i <48; ++i) pows[i] = (10*pows[i-1])%M;
  for(int i = 1; i <= DIGS; ++i){
    if(DIGS%2!=0 && i==(DIGS/2+1)){
       for(int j= 0 ; j < 216 ; ++j)
         for(int k = 0 ; k < 10 ; ++k){
             dp[i][j] = (dp[i-1][j] + dp[i][j])%M;
             sum[i][j] += (k*pows[i-1]*dp[i-1][j]) + sum[i-1][j];
             sum[i][j]%=M;
             }
     }
    else if(first(i)){
       for(int j= 0 ; j < 216 ; ++j)
         for(int k = 0 ; k < 10 ; ++k)
           if(j-k>=0){
             dp[i][j] = (dp[i-1][j-k] + dp[i][j])%M;
             sum[i][j] += (k*pows[i-1]*dp[i-1][j-k]) + sum[i-1][j-k];
             sum[i][j]%=M;
           }
    }
    else if(last(i)){
       for(int j= 0 ; j < 216 ; ++j)
         for(int k = (i==DIGS?1:0) ; k < 10 ; ++k)
           if(j+k<216){
             dp[i][j] = (dp[i-1][j+k] + dp[i][j])%M;
             sum[i][j] += (k*pows[i-1]*dp[i-1][j+k]) + sum[i-1][j+k];
             sum[i][j]%=M;
            }
     } 

  } 
  return sum[DIGS][0];
}

int main(){
  LL res =0;
  for(DIGS=1;DIGS<=47;++DIGS) res = (res+solve())%M;
  cout << res << endl;
}
