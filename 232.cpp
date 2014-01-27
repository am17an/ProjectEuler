#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

double dp[101][101][2];
bool vis[101][101][2];
const int N = 100;
double solve(int p1,int p2,int turn){
  if(p1>=N) return 0.0;
  if(p2>=N) return 1.0;
  
  double &res = dp[p1][p2][turn];
  if(vis[p1][p2][turn]) return res;
  vis[p1][p2][turn] = true; 
  res = 0;
  if(turn==0){
    res = 0.5*solve(p1+1,p2,1-turn) +  0.5*solve(p1,p2,1-turn);
  }else{
    double mx = 0.;
    for(int i = 1;p2 <= N && 1/((1<<i) + 0.) > 1e-9 ;++i) { // after this point, obviously won't be greater than max
      mx = max(mx, (1/((1<<i)+1.0)) * (2*solve(p1,p2+(1<<(i-1)), 0) + ((1<<i) -1)* solve(p1+1,p2,1)));
    }
    res = mx;
  } 
  return res;
}

int main(){
  printf("%.8lf\n", solve(0,0,0));
  cout << solve(0,0,0) << endl;
}
