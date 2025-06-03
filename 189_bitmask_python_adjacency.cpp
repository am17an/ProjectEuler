#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <chrono>
#include <utility>

using namespace std;

struct pair_hash {
    template <class T1, class T2>
    size_t operator() (const pair<T1, T2>& p) const {
        auto h1 = hash<T1>{}(p.first);
        auto h2 = hash<T2>{}(p.second);
        return h1 ^ (h2 << 1);
    }
};

// Convert number to base-3 string
string toBase3(int num, int length) {
    string result = "";
    for (int i = 0; i < length; i++) {
        result = char('0' + (num % 3)) + result;
        num /= 3;
    }
    return result;
}

// Generate triangular grid with Python adjacency logic
pair<int, vector<vector<int>>> generateTriangularGrid(int n) {
    vector<pair<int, int>> triangles;
    vector<vector<int>> neighbors;
    unordered_map<pair<int, int>, int, pair_hash> idMap;
    
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
    
    // Find neighbors for each triangle using Python logic
    for (int row = 0; row < n; row++) {
        for (int col = 0; col < 2 * row + 1; col++) {
            if(idMap.find(std::make_pair(row,col)) == idMap.end()) continue;
            int currentId = idMap[{row, col}];
            
            // Python logic: points_up = (col % 2 == 1) - odd columns point up
            bool pointsUp = (col % 2 == 1);
            
            vector<pair<int, int>> adjacentPositions;
            
            // Add left and right neighbors for all triangles
            adjacentPositions.push_back({row, col - 1});  // left
            adjacentPositions.push_back({row, col + 1});  // right
            
            // Add third neighbor based on orientation (Python logic)
            if (pointsUp) {
                // Upward triangles have a neighbor above
                adjacentPositions.push_back({row - 1, col - 1});
            } else {
                // Downward triangles have a neighbor below
                adjacentPositions.push_back({row + 1, col + 1});
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

// Check if a row coloring is internally valid (no adjacent same colors)
bool isValidRowColoring(const string& coloring) {
    for (int i = 0; i < coloring.length() - 1; i++) {
        if (coloring[i] == coloring[i + 1]) {
            return false;
        }
    }
    return true;
}

// Check compatibility between two consecutive rows using Python adjacency
bool areRowsCompatible(const string& prevRow, const string& currRow, int currRowIndex, const vector<vector<int>>& neighbors) {
    // Get the starting triangle ID for each row
    int prevRowStartId = 0;
    for (int r = 0; r < currRowIndex - 1; r++) {
        prevRowStartId += 2 * r + 1;
    }
    
    int currRowStartId = 0;
    for (int r = 0; r < currRowIndex; r++) {
        currRowStartId += 2 * r + 1;
    }
    
    // Check all triangles in current row against their neighbors in previous row
    for (int currCol = 0; currCol < currRow.length(); currCol++) {
        int currTriangleId = currRowStartId + currCol;
        char currColor = currRow[currCol];
        
        // Check all neighbors of this triangle
        for (int neighborId : neighbors[currTriangleId]) {
            // If neighbor is in the previous row
            if (neighborId >= prevRowStartId && neighborId < currRowStartId) {
                int prevCol = neighborId - prevRowStartId;
                char prevColor = prevRow[prevCol];
                
                if (currColor == prevColor) {
                    return false;
                }
            }
        }
    }
    
    return true;
}

// Generate all valid colorings for a single row
vector<string> generateValidRowColorings(int rowLength) {
    vector<string> validColorings;
    int totalStates = 1;
    for (int i = 0; i < rowLength; i++) {
        totalStates *= 3;
    }
    
    for (int state = 0; state < totalStates; state++) {
        string coloring = toBase3(state, rowLength);
        if (isValidRowColoring(coloring)) {
            validColorings.push_back(coloring);
        }
    }
    
    return validColorings;
}

// Debug function to verify adjacency matches Python
void debugAdjacency(int n) {
    auto [numTriangles, neighbors] = generateTriangularGrid(n);
    
    cout << "Adjacency for n=" << n << " (using Python logic):" << endl;
    for (int i = 0; i < numTriangles; i++) {
        cout << "Triangle " << i << " connects to: ";
        for (int neighbor : neighbors[i]) {
            cout << neighbor << " ";
        }
        cout << endl;
    }
    cout << endl;
}

// Main DP function
long long countTriangularColorings(int n) {
    if (n == 0) return 1;
    
    // Generate the adjacency information using Python logic
    auto [numTriangles, neighbors] = generateTriangularGrid(n);
    
    // dp[row][coloring] = number of ways to color up to this row with this coloring
    vector<unordered_map<string, long long>> dp(n);
    
    // Initialize first row
    vector<string> firstRowColorings = generateValidRowColorings(1);
    for (const string& coloring : firstRowColorings) {
        dp[0][coloring] = 1;
    }
    
    // Process each subsequent row
    for (int row = 1; row < n; row++) {
        int rowLength = 2 * row + 1;
        vector<string> currentRowColorings = generateValidRowColorings(rowLength);
        
        for (const string& currentColoring : currentRowColorings) {
            long long ways = 0;
            
            // Check compatibility with all colorings of previous row
            for (const auto& [prevColoring, prevWays] : dp[row - 1]) {
                if (areRowsCompatible(prevColoring, currentColoring, row, neighbors)) {
                    ways += prevWays;
                }
            }
            
            if (ways > 0) {
                dp[row][currentColoring] = ways;
            }
        }
    }
    
    // Sum all ways for the final row
    long long total = 0;
    for (const auto& [coloring, ways] : dp[n - 1]) {
        total += ways;
    }
    
    return total;
}

int main() {
    cout << "Triangular grid 3-coloring using bitmask DP with Python adjacency:" << endl;
    
    // First show the adjacency for n=3 to compare with Python output
    debugAdjacency(3);
    
    // Test with expected values (known correct values for first 5)
    vector<long long> expected = {3, 24, 480, 24000, 2976000};
    
    for (int n = 1; n <= 8; n++) {
        auto start = chrono::high_resolution_clock::now();
        
        long long result = countTriangularColorings(n);
        
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> duration = end - start;
        
        cout << "n=" << n << ": " << result << " valid 3-colorings (Time: " 
             << duration.count() << " seconds)";
        
        if (n <= expected.size() && result == expected[n-1]) {
            cout << " ✓";
        } else if (n <= expected.size()) {
            cout << " ✗ (expected " << expected[n-1] << ")";
        }
        cout << endl;
        
        // Stop if it takes too long
        if (duration.count() > 30) {
            cout << "Stopping due to time limit" << endl;
            break;
        }
    }
    
    return 0;
} 