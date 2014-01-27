#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

const int MAXN = 5;

bool ok[MAXN][10];
int incorrect[MAXN][10];

int nh;
int current[MAXN];
int pos ;
pair<string, int> hints[30];
void dfs(int current_hint){
  if(current_hint == nh-2){
    // if you reach here you are done
    for(int i = 0 ; i < MAXN ; ++i){
      cout << current[i] ;
    }
    cout << endl;
  }
  // If all things are covered
  if(pos == MAXN){
    // check if current hint is compatible 
    // Use this - if hint has 2 correct, our string should only match 2 
    int same = 0;
    for(int i = 0 ; i < MAXN ; ++i){
      if(current[i] == hints[current_hint].first[i]) same++;
    }
    if(same!= hints[current_hint].second) return;
    dfs(current_hint+1);
  }

  if(hints[current_hint].second == 1){
    for(int i = 0 ; i < hints[current_hint].first.size() ; ++i){
      if(incorrect[i][hints[current_hint].first[i]-'0']== 0 && current[i] == -1) {
        current[i] = hints[current_hint].first[i]- '0'; pos++;
        for(int j = 0 ; j < hints[current_hint].first.size() ; ++j)if(i!=j)
          incorrect[j][hints[current_hint].first[j]-'0']++;
        dfs(current_hint+1);
        current[i] = -1; pos --;
        for(int j = 0 ; j < hints[current_hint].first.size(); ++j) if(i!=j)
          incorrect[j][hints[current_hint].first[j]-'0']--;
      }
    }
  }
  else if(hints[current_hint].second == 2){
    for(int i = 0 ; i < hints[current_hint].first.size() ; ++i)
      for(int j = i+1 ; j < hints[current_hint].first.size() ; ++j){
        if(incorrect[i][hints[current_hint].first[i] - '0'] == 0 && 
            incorrect[j][hints[current_hint].first[j] - '0'] == 0 && current[i] == -1
            && current[j] == -1){
              current[i] = hints[current_hint].first[i] - '0',pos++;
              current[j] = hints[current_hint].first[j] - '0',pos++;
              for(int k = 0 ; k < hints[current_hint].first.size(); ++k) if(k!=i && k!=j){
                incorrect[k][hints[current_hint].first[k]] ++;
              }
              dfs(current_hint + 1);
              current[i] = -1;pos--;
              current[j] = -1;pos--;
              
              for(int k = 0 ; k < hints[current_hint].first.size(); ++k) if(k!=i && k!=j){
                incorrect[k][hints[current_hint].first[k]] --;
              }

        }
      }
  }
}

int main(){
 nh = 5;
 hints[0] = make_pair("90342",2);
 hints[1] = make_pair("39458",2);
 hints[2] = make_pair("34109",1);
 hints[3] = make_pair("51545",2);
 hints[4] = make_pair("12531",1);
  
 incorrect[0][7] = 1;
 incorrect[1][0] = 1;
 incorrect[2][7] = 1;
 incorrect[3][9] = 1;
 incorrect[4][4] = 1;
 for(int i =0  ; i < 5 ; ++i) current[i] = -1;
 dfs(0);

}

