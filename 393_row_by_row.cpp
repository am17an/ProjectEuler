#include <iostream>
#include <vector>
#include <set>
#include <chrono>
#include <algorithm>
#include <functional>

using namespace std;
using namespace std::chrono;

struct Position {
    int row, col;
    
    Position(int r, int c) : row(r), col(c) {}
    
    bool operator<(const Position& other) const {
        if (row != other.row) return row < other.row;
        return col < other.col;
    }
    
    bool operator==(const Position& other) const {
        return row == other.row && col == other.col;
    }
};

struct Edge {
    Position p1, p2;
    
    Edge(Position pos1, Position pos2) : p1(pos1), p2(pos2) {
        // Ensure canonical ordering
        if (p2 < p1) {
            p1 = pos2;
            p2 = pos1;
        }
    }
    
    bool operator<(const Edge& other) const {
        if (!(p1 == other.p1)) return p1 < other.p1;
        return p2 < other.p2;
    }
};

vector<Position> getNeighbors(int row, int col, int n) {
    vector<Position> neighbors;
    // Up, Down, Left, Right
    int directions[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    
    for (int i = 0; i < 4; i++) {
        int newRow = row + directions[i][0];
        int newCol = col + directions[i][1];
        
        if (newRow >= 0 && newRow < n && newCol >= 0 && newCol < n) {
            neighbors.push_back(Position(newRow, newCol));
        }
    }
    
    return neighbors;
}

// Generate all possible movement patterns for a single row
void generateRowMoves(int row, int n, vector<vector<Position>>& allRowMoves) {
    vector<Position> currentRowMoves;
    
    function<void(int)> backtrack = [&](int col) {
        if (col == n) {
            allRowMoves.push_back(currentRowMoves);
            return;
        }
        
        Position startPos(row, col);
        vector<Position> neighbors = getNeighbors(row, col, n);
        
        for (const Position& dest : neighbors) {
            currentRowMoves.push_back(dest);
            backtrack(col + 1);
            currentRowMoves.pop_back();
        }
    };
    
    backtrack(0);
}

// Check if a row movement pattern is internally valid (no conflicts within the row)
bool isValidRowPattern(int row, int n, const vector<Position>& rowMoves) {
    set<Position> occupiedPositions;
    set<Edge> usedEdges;
    
    for (int col = 0; col < n; col++) {
        Position startPos(row, col);
        Position destPos = rowMoves[col];
        
        // Check if destination is already occupied by another ant in this row
        if (occupiedPositions.find(destPos) != occupiedPositions.end()) {
            return false;
        }
        occupiedPositions.insert(destPos);
        
        // Check if edge is already used by another ant in this row
        Edge edge(startPos, destPos);
        if (usedEdges.find(edge) != usedEdges.end()) {
            return false;
        }
        usedEdges.insert(edge);
    }
    
    return true;
}

// Check if two row patterns are compatible (no edge conflicts between rows)
bool areRowsCompatible(int row1, int row2, int n, 
                      const vector<Position>& moves1, 
                      const vector<Position>& moves2) {
    set<Edge> edges1, edges2;
    
    // Collect edges from row1
    for (int col = 0; col < n; col++) {
        Position start1(row1, col);
        Position dest1 = moves1[col];
        edges1.insert(Edge(start1, dest1));
    }
    
    // Collect edges from row2 and check for conflicts
    for (int col = 0; col < n; col++) {
        Position start2(row2, col);
        Position dest2 = moves2[col];
        Edge edge2(start2, dest2);
        
        if (edges1.find(edge2) != edges1.end()) {
            return false;
        }
    }
    
    return true;
}

// Main row-by-row backtracking function
long long solveRowByRow(int n) {
    if (n == 1) return 0;
    
    // Pre-generate all valid movement patterns for each row
    vector<vector<vector<Position>>> validRowPatterns(n);
    
    cout << "Generating valid row patterns..." << endl;
    for (int row = 0; row < n; row++) {
        vector<vector<Position>> allRowMoves;
        generateRowMoves(row, n, allRowMoves);
        
        // Filter to keep only internally valid patterns
        for (const auto& pattern : allRowMoves) {
            if (isValidRowPattern(row, n, pattern)) {
                validRowPatterns[row].push_back(pattern);
            }
        }
        
        cout << "Row " << row << ": " << validRowPatterns[row].size() 
             << " valid patterns (out of " << allRowMoves.size() << ")" << endl;
    }
    
    // Now use backtracking to combine rows
    vector<int> chosenPatterns(n, -1);
    
    function<long long(int, set<Position>&, set<Edge>&)> backtrack = 
        [&](int currentRow, set<Position>& globalOccupied, set<Edge>& globalUsedEdges) -> long long {
        
        if (currentRow == n) {
            return 1; // All rows processed successfully
        }
        
        long long count = 0;
        
        for (int patternIdx = 0; patternIdx < validRowPatterns[currentRow].size(); patternIdx++) {
            const auto& pattern = validRowPatterns[currentRow][patternIdx];
            
            // Check if this pattern conflicts with already placed rows
            bool valid = true;
            vector<Position> newOccupied;
            vector<Edge> newEdges;
            
            for (int col = 0; col < n; col++) {
                Position startPos(currentRow, col);
                Position destPos = pattern[col];
                
                // Check position conflict
                if (globalOccupied.find(destPos) != globalOccupied.end()) {
                    valid = false;
                    break;
                }
                newOccupied.push_back(destPos);
                
                // Check edge conflict
                Edge edge(startPos, destPos);
                if (globalUsedEdges.find(edge) != globalUsedEdges.end()) {
                    valid = false;
                    break;
                }
                newEdges.push_back(edge);
            }
            
            if (valid) {
                // Apply the pattern
                for (const Position& pos : newOccupied) {
                    globalOccupied.insert(pos);
                }
                for (const Edge& edge : newEdges) {
                    globalUsedEdges.insert(edge);
                }
                
                // Recurse to next row
                count += backtrack(currentRow + 1, globalOccupied, globalUsedEdges);
                
                // Backtrack
                for (const Position& pos : newOccupied) {
                    globalOccupied.erase(pos);
                }
                for (const Edge& edge : newEdges) {
                    globalUsedEdges.erase(edge);
                }
            }
        }
        
        return count;
    };
    
    set<Position> globalOccupied;
    set<Edge> globalUsedEdges;
    
    cout << "Starting row-by-row backtracking..." << endl;
    return backtrack(0, globalOccupied, globalUsedEdges);
}

int main() {
    cout << "Row-by-row brute force for ant movement problem" << endl;
    
    for (int n = 2; n <= 8; n++) {
        cout << "\n=== Computing f(" << n << ") ===" << endl;
        
        auto start = high_resolution_clock::now();
        long long result = solveRowByRow(n);
        auto end = high_resolution_clock::now();
        
        auto duration = duration_cast<milliseconds>(end - start);
        cout << "f(" << n << ") = " << result << endl;
        cout << "Time taken: " << duration.count() << " ms" << endl;
        
        // Stop if it's taking too long
        if (duration.count() > 60000) { // More than 1 minute
            cout << "Stopping due to time limit" << endl;
            break;
        }
    }
    
    return 0;
} 