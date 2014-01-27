#include <iostream>
#include <cstdio>
#include <vector>
#include <sstream>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;
int r = 0;
char s[5];
vector<string> f;
void dfs(int l,const string & curr){
  cout << curr << endl;
  if(l==5) f.push_back(curr); 
  string newcurr = curr+"0";
  dfs(l+1,newcurr);
  newcurr = curr + "1";
  dfs(l+1,newcurr);
}
int main(){
  dfs(0,"");
  cout << f.size() << endl;
 for(int i = 0 ; i < 32 ; ++i) cout << f[i] << endl; 
}

