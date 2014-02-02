#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <cassert>
#include <algorithm>

#define MAXN 20
#define MAX_HINTS 25
using namespace std;

string hints[MAX_HINTS];
int correct[MAXN];
int incorrect[MAXN][10];
int chosen[MAXN];
int nhints,nsize;

void input(){
  
  string x;
  int y,k=0;
  while(cin>> x && cin >> y){
    correct[k] = y;
    hints[k++] = x;
    cout << x << " " << y << endl;
  }
  nhints = k;
  nsize = hints[0].size();
  cout << nhints << " " << nsize << endl;
}


void output(){
  long long r=0;
  bool go=true;
  for(int i = 0 ; i < nsize; ++i){
    cout << chosen[i] ;
    //assert(chosen[i]!=-1);
  }
  cout << endl;
}

void print(int arr[]){
  for(int i = 0 ; i < nsize;++i){
    cerr << arr[i] << " ";
  }
  cerr << endl;
}

int total = 0;

void dfs(int curr, int p, int t){
  if(curr >= nhints){
     output();
      return;
  }
  // move on to next string
  if(curr == nhints-1){
    print(chosen);
  }
  if(p >= nsize){
    if(t == correct[curr]){
      dfs(curr+1,0,0);
    }
    return;
  }
  // choose to take 
  if(nsize-p<correct[curr]-t)return;
  if(t< correct[curr]){
      if((incorrect[p][hints[curr][p]-'0']==0) && (chosen[p] == -1 || chosen[p] ==  (hints[curr][p]-'0'))){
        bool ok = false;
        if(chosen[p] == hints[curr][p]-'0') ok = true;
        chosen[p] = hints[curr][p]-'0';
        if(!ok) total++;
        dfs(curr,p+1,t+1);
        chosen[p] = -1;
        if(!ok)total--;
        if(ok) chosen[p] = hints[curr][p]-'0';
      }
  }
  
  if(chosen[p] != hints[curr][p] -'0'){  
    incorrect[p][hints[curr][p]-'0'] ++ ;
    dfs(curr,p+1,t);
    incorrect[p][hints[curr][p]-'0'] --;
  }
}

int main(){
  for(int i = 0 ; i < MAXN; ++i) chosen[i] = -1;
  input();
  dfs(0,0,0);
}
