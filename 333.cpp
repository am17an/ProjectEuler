#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <unordered_map>

std::map<std::pair<int, int>, int> memo;
std::vector<int> parts;

std::map<int, std::vector<int>> graph;

bool is_prime[1000001];


void sieve() {

    std::fill(std::begin(is_prime), std::end(is_prime), true);

    is_prime[1] = false;
    int limit = 1000001;
    for(int i = 2; i < limit; ++i) {
        if(is_prime[i]) {
            for(int k = i+i; k < limit;k+=i) {
                is_prime[k] = false;
            }
        }
    }
}



int ways(int n, int k, std::vector<int> & current_path) {
    if(n == 0) {
        return 1;
    }

    int64_t ans = 0;
    for(int i = k ; i >= 0; i--) {
        if(n - parts[i] >= 0) {
            bool is_ok = true;
            for(auto other: current_path) if(other%parts[i] == 0) {
                is_ok = false;
                break;
            }

            if(is_ok) {
                current_path.push_back(parts[i]);
                ans += ways(n-parts[i], i, current_path);
                current_path.pop_back();
            }
        }

        if(ans > 1) break;
    }

    return ans;
}

int main() {
    
    int limit = 1e6;
    for(int64_t twos=1; twos <= limit; twos*=2) {
        for(int64_t threes=1; threes <= limit; threes*=3) {
            int64_t total = twos*threes;
            if(total <= limit) {
                parts.push_back(total);
            }
        }
    }
    std::sort(parts.begin(), parts.end());

    for(int i = 0; i < parts.size(); ++i) {
        for(int j = i+1; j < parts.size(); ++j) {
            if(parts[j]%parts[i] != 0) {
                graph[parts[j]].push_back(parts[i]);
            }
        }
    }

    for(int i = 0 ; i < parts.size(); ++i) {
        std::sort(graph[parts[i]].begin(), graph[parts[i]].end());
        std::reverse(graph[parts[i]].begin(), graph[parts[i]].end());
    }

    sieve();

    int total = 0;


    std::vector<int> current_path{};
    std::cout << ways(999983, parts.size()-1, current_path) << std::endl;

    for(int i = 1; i < limit; ++i) {
        if(i%10000 == 0) {
            std::cout << "Done with " << i << std::endl;
        }
        if(is_prime[i]) {
            std::vector<int> current_path{};
            if(ways(i, parts.size() -1 , current_path) == 1) {
                total += i;
            }
        }
    }

    std::cout << total << std::endl;

}
