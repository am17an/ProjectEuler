#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

int main(){
  long long start = 1e+15 + 2e+8; 
//  int seq[] = {0,-1,0,-1,-1,1,1,-1,0,0};
  int seq[] = {1, 0, 0, 0, 1, -1, -1, -1, 0, 0, 1, 0, 0, -1, -1, 0, -1, 0, -1, -1, 0, 0, 1, 0, 0, -1, 1, 1, 0, -1} ;
  for(;;){
    int current = 0;
    int num = start;
    cout << start << endl;
    while(true){
      if(current == sizeof(seq)/sizeof(int)){
        cout << start << endl;
        exit(0);
      }
      if(num == 1) break;
      if(num % 3 == 0){
        num/=3;
        if(seq[current]!=0)
         break; 
      }
      else if(num%3 == 1){
        num = (4*num+2)/3;
        if(seq[current]!=1)
          break;
      }
      else{
        num = (2*num-1)/3;
        if(seq[current]!=-1)
          break;
      }
      current++; 
    }
    start++;
  }
}
