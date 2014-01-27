#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>
#include "pe_utils.hpp"
using namespace std;


int best[1000005];

int main(){
  
  for(int i = 2 ; i < 1000000; ++i) best[i] = 1+((i-1)%9);
// sucks
  for(int i = 4 ; i < 1000000; ++i){
    int b1=0,b2=0,b3=0,b4=0;
    for(int j = 2 ; j*j <=i ; ++j){
      if(i%j == 0){
        if((best[j] + best[i/j]) > best[i]){
            best[i] = best[j] + best[i/j];
            b1 = j, b2= i/j;
            b3 = best[j], b4 = best[i/j];
        }
      }
    }
  }
  long long r= 0;
  for(int i = 2;i<1000000;++i)r+=best[i];
  cout << r << endl;
}

