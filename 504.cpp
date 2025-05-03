#include <iostream>
#include <vector>
#include <algorithm>

int M = 100;

int gcd(int a, int b) {
    if (b == 0)
        return a;
    return gcd(b, a % b);
}

int main() {

    std::vector<int> squares;

    int i = 1;
    while(i*i < 1e9) {
        squares.push_back(i*i);
        i++;
    }

    int count = 0;

    for(int a = 1; a <= M;++a) {
        if(a%10 == 0) {
            std::cout << "henlo " << a << std::endl;
        }
        for(int b = 1 ; b <= M; ++b) {
            for(int c = 1 ; c <= M; c++) {
                for(int d = 1 ; d <= M; d++) {
                    int lattice = (a*b + b*c + c*d + d*a)/2;
                    int gcdsum = (gcd(a, b) + gcd(b,c) + gcd(c,d) + gcd(d, a))/2;
                    lattice -= gcdsum;

                    lattice += 1;

                    if(std::binary_search(squares.begin(), squares.end(), lattice)) {
                        count++;
                    }
                }
            }
        }
    }

    std::cout << count << std::endl;
	
}
