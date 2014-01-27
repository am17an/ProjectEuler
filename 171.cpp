#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

typedef long long LL;

LL dp[21][1700];
int M = 1e+9;

LL sum[21][1700];

LL pows[21];
int main(){
  pows[0] = 1;
  for(int i = 1; i <=20 ; ++i){
    pows[i] = (10*pows[i-1])%M;
  }

  dp[0][0] = 1;
  sum[0][0] = 0;
  for(int i = 1; i <=20; ++i){
    for(int j = 0 ; j < 1700; ++j){
      for(int k = 0; k <10;++k){
         if(j-k*k>=0){
           dp[i][j]  = (dp[i][j] + dp[i-1][j-k*k])%M;
           sum[i][j] += (k*pows[i-1] * dp[i-1][j-k*k])%M + (sum[i-1][j-k*k])%M;
           sum[i][j]%=M;
         }
      }
    }
  }
  int curr= 1;
  vector<bool> squares(1700,false); 
  for(curr=1;curr*curr<1700;++curr) squares[curr*curr] = true;
  LL res = 0;
  for(int i = 20; i <=20 ;++i){
    for(int j = 0 ; j < 1700 ; ++j){
      if(squares[j]) res=(res+sum[i][j])%M;
    }
  }
  for(int i = 1; i <=10 ; ++i) cout << sum[1][i] << endl;
  cout << res << endl;
}
