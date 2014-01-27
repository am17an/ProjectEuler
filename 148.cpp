#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

typedef long long LL;
int main(){
  LL res = 0;
  for(int i = 0; i< 1000000000;++i){
    LL q=1,x = i;
    while(x){q*=(x%7+1);x/=7;}
    res+=q;
  }
  cout << res << endl;
}
