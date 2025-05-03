#include <iostream>
#include <vector>

int main() {
    std::vector<int> squares;

    int i = 1;
    while(i*i < 100) {
        squares.push_back(i*i);
        i++;
    }

    for(int i = 1; i <= 100; ++i) {
        for(int j = squares.size() - 1 ; j >= 0 ; j--) {
            if(i%squares[j] == 0) {
                std::cout << i << " " << squares[j] << std::endl;
                break;
            }
        }
    }
}