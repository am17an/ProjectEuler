#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#define FOR(i,n) for(int i = 0 ; i < n ; ++i)
using namespace std;

typedef long long LL;
#define N 9
LL mat[N][N];
LL ans[N][N];
LL base[N][N];
int M=1e+8;
void matMul(LL a[N][N], LL b[N][N]){
  LL res[N][N];
  FOR(i,N)FOR(j,N)res[i][j] = 0LL;
  FOR(i,N)FOR(j,N)FOR(k,N)res[i][j]=(a[i][k]*b[k][j])%M;
  FOR(i,N) FOR(j,N) a[i][j]=res[i][j];
}
void matPow(LL exp){
  FOR(i,N)FOR(j,N)ans[i][j]=0LL;FOR(i,N)a[i][i]=1;
  FOR(i,N)FOR(j,N)base[i][j]=(j>=i?1:0);
  for(LL ex=exp;ex;ex>>=1){
    if(ex&1) matMul(ans,base); matMul(base,base); 
  }  
}
void printGrid(LL a[N][N]){
  FOR(i,n){
    FOR(j,N) cout << a[i][j] << endl;
    cout << endl;
  }
}
int main(){
  matPow(5);
  printGrid(ans); 
}

