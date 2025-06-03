#include <iostream>
#include <vector>
#include <map>
#include <utility>
#include <functional>
#include <chrono>
#include <unordered_map>

using namespace std;

// Use a hash function for pair to use unordered_map
struct pair_hash {
    template <class T1, class T2>
    size_t operator() (const pair<T1, T2>& p) const {
        auto h1 = hash<T1>{}(p.first);
        auto h2 = hash<T2>{}(p.second);
        return h1 ^ (h2 << 1);
    }
};

// Generate triangular grid and return number of triangles and neighbor information
pair<int, vector<vector<int>>> generateTriangularGrid(int n) {
    vector<pair<int, int>> triangles;
    vector<vector<int>> neighbors;
    unordered_map<pair<int, int>, int, pair_hash> idMap;
    
    // Pre-allocate memory
    int totalTriangles = n * n;
    triangles.reserve(totalTriangles);
    neighbors.reserve(totalTriangles);
    
    // Generate all triangles
    int triangleId = 0;
    
    for (int row = 0; row < n; row++) {
        for (int col = 0; col < 2 * row + 1; col++) {
            triangles.push_back({row, col});
            idMap[{row, col}] = triangleId;
            neighbors.push_back(vector<int>());
            triangleId++;
        }
    }
    
    // Find neighbors for each triangle
    for (int row = 0; row < n; row++) {
        for (int col = 0; col < 2 * row + 1; col++) {
            int currentId = idMap[{row, col}];
            
            // Check if triangle points up (even col) or down (odd col)
            bool pointsUp = (col % 2 == 0);
            
            // Add left and right neighbors for all triangles
            vector<pair<int, int>> adjacentPositions = {
                {row, col - 1},  // left
                {row, col + 1},  // right
            };
            
            // Add third neighbor based on orientation
            if (pointsUp) {
                // Upward triangles have a neighbor above
                adjacentPositions.push_back({row - 1, col / 2});
            } else {
                // Downward triangles have a neighbor below
                adjacentPositions.push_back({row + 1, col - 1});
            }
            
            for (auto [adjRow, adjCol] : adjacentPositions) {
                if (adjRow >= 0 && adjRow < n && adjCol >= 0 && adjCol < 2 * adjRow + 1) {
                    auto it = idMap.find({adjRow, adjCol});
                    if (it != idMap.end()) {
                        neighbors[currentId].push_back(it->second);
                    }
                }
            }
        }
    }
    
    return {triangles.size(), neighbors};
}

// Count valid colorings using backtracking
long long countColoringsBacktrack(int numTriangles, const vector<vector<int>>& neighbors, int numColors = 3) {
    vector<int> coloring(numTriangles, -1);
    
    // Check if assigning color to triangle is valid
    auto isValid = [&](int triangle, int color) {
        for (int neighbor : neighbors[triangle]) {
            if (coloring[neighbor] == color) {
                return false;
            }
        }
        return true;
    };
    
    // Recursive backtracking function
    function<long long(int)> backtrack = [&](int triangle) {
        if (triangle == numTriangles) {
            return 1LL;
        }
        
        long long count = 0;
        for (int color = 0; color < numColors; color++) {
            if (isValid(triangle, color)) {
                coloring[triangle] = color;
                count += backtrack(triangle + 1);
                coloring[triangle] = -1;
            }
        }
        
        return count;
    };
    
    return backtrack(0);
}

int main() {
    // Calculate for n = 1 to 8
    for (int n = 1; n <= 8; n++) {
        auto start = chrono::high_resolution_clock::now();
        
        auto [numTriangles, neighbors] = generateTriangularGrid(n);
        long long validColorings = countColoringsBacktrack(numTriangles, neighbors);
        
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> duration = end - start;
        
        cout << "n=" << n << ": " << numTriangles << " triangles, " << validColorings 
             << " valid 3-colorings (Time: " << duration.count() << " seconds)" << endl;
    }
    
    return 0;
} 
