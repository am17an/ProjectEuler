#include <iostream>
#include <climits>
#include <cstring>
#include <cassert>


const int N = 9;
const int ROWS = 12; 

int64_t dp[ROWS][(1<<N)][(1<<N)][(1<<N)];

//trinomoes


int findFirstUnsetBit(unsigned int num) {
    // Flip all bits, then find first set bit in the flipped number
    unsigned int flipped = ~num;
    // __builtin_ffs returns position of first set bit (1-indexed)
    // or returns 0 if no bits are set
    int result = __builtin_ffs(flipped);
    // Convert to 0-indexed or return -1 if all bits are set
    return result == 0 ? -1 : result - 1;
}

bool taken(int row, int pos) {
    return (row & (1<<pos)) != 0;
}



int64_t solve(int current_row, int r1, int r2, int r3) {

    //std::cout << current_row << " " << r1 << " " << r2 << " " << r3 << " " <<  std::endl;

    if(current_row >= ROWS) 
    {
     //   std::cout << "done" << std::endl;
        return 1;
    }

    int64_t & memo = dp[current_row][r1][r2][r3]; 

    if(memo != -1) return memo;

    memo = 0;

    int f = findFirstUnsetBit(r1);

    //std::cout << "First unset bit " << f << " " << r1 << std::endl;


    if(f >= N) {
        assert(r1 == (1<<N) - 1);
        //std::cout << "Solving new row" << current_row + 1 <<  std::endl;
        memo = solve(current_row+1, r2, r3, 0);
        return memo;
    }

    // Place 4 Ls
    if(current_row + 1 < ROWS) {
        if(f + 1 < N && !taken(r1, f+1) && !taken(r2, f)) {
            int new_r1 = r1 | 1<<f;
            new_r1 |= 1<<(f+1);
            int new_r2 = r2 | 1<<f;
            memo += solve(current_row, new_r1, new_r2, r3);
        }
        if(f + 1 < N && !taken(r1, f+1) && !taken(r2, f+1)) {
            int new_r1 = r1 | 1<<f;
            new_r1 |= 1<<(f+1);
            int new_r2 = r2 | 1<<(f+1);
            memo += solve(current_row, new_r1, new_r2, r3);
        }
        if(f+1<N && !taken(r2, f) && !taken(r2, f+1)) {
            int new_r1 = r1 | 1<<f; 
            int new_r2 = r2 | 1<<f;
            new_r2 |= 1<<(f+1);
            memo += solve(current_row, new_r1, new_r2, r3);
        }
        if(f-1 >= 0 && !taken(r2, f) && !taken(r2, f-1)) {
            int new_r1 = r1 | 1<<f; 
            int new_r2 = r2 | 1<<f;
            new_r2 = new_r2 | 1<<(f-1);

            memo += solve(current_row, new_r1, new_r2, r3);
        }
    }

    if(current_row+2 < ROWS) {
       // std::cout <<" TKKEN" <<  !taken(r2, f) << " " << !taken(r3, f) << " " << r2 << " " << f << std::endl;
        if(!taken(r2, f) && !taken(r3, f)) {
            //std::cout << "Big one" << std::endl;
            int new_r1 = r1 | 1<<f;
            int new_r2 = r2 | 1<<f;
            int new_r3 = r3 | 1<<f;
            memo += solve(current_row, new_r1, new_r2, new_r3);
        }
    }
    if(f+2 < N && !taken(r1, f+1) && !taken(r1, f+2)) {
        int new_r1 = r1 | 1<<f;
        new_r1 |= 1<<(f+1);
        new_r1 |= 1<<(f+2);

        memo += solve(current_row, new_r1, r2, r3);
    }

    return memo;
}

int main() {
    memset(dp, -1, sizeof(dp));
    std::cout << solve(0, 0, 0, 0) << std::endl;

}

