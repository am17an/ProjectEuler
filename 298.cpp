#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#include <cstring>
#define PB push_back
#define TURNS 10
using namespace std;

double dp2[51][11][11][11][11][11];
bool done1[51][11][11][11][11][11];
bool done2[51][11][11][11][11][11];
double dp1[51][11][11][11][11][11];
vector<int> newOrder(const vector<int> & a, int n){
  int c = -1;
  for(int i = 0 ; i < 5 ; ++i) if(a[i] == n) c = i;
  vector<int> q = a;
  if(c>=0){
    vector<int> f ;
    f.push_back(n);
    q.erase(q.begin() + c);
    for(int i =0 ; i < 4 ; ++i)
      f.push_back(q[i]);
    return f;
  }
  else{
    // do a right shift
    vector<int> f;
    f.push_back(n);
    for(int i = 0 ; i < 4 ; ++i){
      f.push_back(a[i]);
    }
    return f;
  }
}

vector<int> newOrder2(const vector<int> & a, int n){
  int c = -1;
  for(int i = 0 ; i < 5 ; ++i) if(a[i] == n) c = i;
  vector<int> q = a;
  if(c>=0){
    return q;
  }
  else{
    vector<int> f;
    for(int i = 1 ; i < 5 ; ++i)
      f.push_back(q[i]);
    f.push_back(n);
    return f;
  }
}

inline bool contains(const vector<int> &a , int n){
  for(int i = 0 ; i < a.size() ; ++i) if(a[i] == n) return true;
  return false;
}

double solve(int turn, int a, int b, int c,int d,int e){
  if(turn >= TURNS){
    return 0;
  }
  if(done1[turn][a][b][c][d][e]) return dp1[turn][a][b][c][d][e];
  done1[turn][a][b][c][d][e] = true;
  double & res =  dp1[turn][a][b][c][d][e];
  vector<int> poss;
  poss.PB(a);   
  poss.PB(b);   
  poss.PB(c);   
  poss.PB(d);   
  poss.PB(e);   
  res = 0.;
  for(int i = 1 ; i <= 10 ; ++i){
      if(contains(poss,i)){
          vector<int> f = newOrder(poss,i); // move number to front
          res += 0.1 * (solve(turn+1,f[0],f[1],f[2],f[3],f[4]) +1);
      }else{
          vector<int> f = newOrder(poss,i); // do a left shift
          res += 0.1 * (solve(turn+1,f[0],f[1],f[2],f[3],f[4]));
      }
  }
  
//  cout << turn << " " << a << " " << b << " " << c << " " << d << " " << e <<  " " << res << endl;
  return res;
}

double solve2(int turn, int a, int b, int c,int d,int e){
  if(turn >= TURNS){
    return 0;
  }
  if(done2[turn][a][b][c][d][e]) return dp2[turn][a][b][c][d][e];
  done2[turn][a][b][c][d][e] = true;
  double & res =  dp2[turn][a][b][c][d][e];
  vector<int> poss;
  poss.PB(a);   
  poss.PB(b);   
  poss.PB(c);   
  poss.PB(d);   
  poss.PB(e);   
  res = 0.;
  for(int i = 1 ; i <= 10 ; ++i){
      if(contains(poss,i)){
          vector<int> f = newOrder2(poss,i); // move number to front
          res += 0.1 * (solve2(turn+1,f[0],f[1],f[2],f[3],f[4]) +1);
      }else{
          vector<int> f = newOrder2(poss,i); // do a left shift
          res += 0.1 * (solve2(turn+1,f[0],f[1],f[2],f[3],f[4]));
      }
  }
  
//  cout << turn << " " << a << " " << b << " " << c << " " << d << " " << e <<  " " << res << endl;
  return res;
}
template <typename T>
void print( T a ){
  cout << a << endl; 
}
int main(){
  vector<int> f;
//  double l = solve(0,0,0,0,0,0);
 // double r = solve2(0,0,0,0,0,0);
  // returns equal values of L and R but |L-R| might not be zero 
  // printf("%.9lf\n",l);
  //printf("%.9lf\n",r);
  //printf("%.8lf\n",l-r);
  print(1);
  print("vello");
}
