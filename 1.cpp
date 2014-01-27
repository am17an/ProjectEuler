#define F(x) XF(#X)
#include <cstdio>
int main(){
  printf("%s",F("hello"));
}
