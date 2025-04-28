#include <iostream>
#include <vector>
#include <string>
#include <unordered_set>
#include <iomanip>
#include <thread>
#include <mutex>
#include <atomic>
#include <cmath>
#include <algorithm>
#include <functional>

using namespace std;

// Structure to represent a position in the 2D grid
struct Point {
    int x, y;
    
    Point(int _x = 0, int _y = 0) : x(_x), y(_y) {}
    
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

// Hash function for Point to use in unordered_set
struct PointHash {
    size_t operator()(const Point& p) const {
        // Combine x and y into a single hash
        return (static_cast<size_t>(p.x) << 16) | static_cast<size_t>(p.y & 0xFFFF);
    }
};

// Check if two positions are adjacent in the grid
inline bool areAdjacent(const Point& a, const Point& b) {
    return abs(a.x - b.x) + abs(a.y - b.y) == 1;
}

// Count H-H contacts in a given folding
// protein is represented as a bit mask: bit i is 1 if position i is 'H', 0 if 'P'
int countHHContacts(unsigned protein, const vector<Point>& folding, int length) {
    int contacts = 0;
    
    for (int i = 0; i < length; i++) {
        // Skip if not H
        if ((protein & (1U << i)) == 0) continue;
        
        for (int j = 0; j < length; j++) {
            // Skip if same position or not H
            if (i == j || (protein & (1U << j)) == 0) continue;
            
            if (areAdjacent(folding[i], folding[j])) {
                contacts++;
            }
        }
    }
    
    // Each contact is counted twice (from both ends), so divide by 2
    return contacts / 2;
}

// Directions for movement: right, down, left, up
const int dx[4] = {1, 0, -1, 0};
const int dy[4] = {0, 1, 0, -1};

// Find the maximum number of H-H contacts for a protein
int findMaxContacts(unsigned protein, int length) {
    if (length <= 1) return 0;
    
    vector<Point> currentFolding(length);
    unordered_set<Point, PointHash> occupied;
    
    int maxContacts = 0;
    
    // Backtracking function to explore all possible foldings
    function<void(int)> search = [&](int index) {
        // Base case: all positions are filled
        if (index == length) {
            int contacts = countHHContacts(protein, currentFolding, length);
            maxContacts = max(maxContacts, contacts);
            return;
        }
        
        // Try all four directions for the next position
        for (int dir = 0; dir < 4; dir++) {
            Point newPos(
                currentFolding[index-1].x + dx[dir], 
                currentFolding[index-1].y + dy[dir]
            );
            
            if (occupied.find(newPos) == occupied.end()) {
                // Place amino acid at new position
                currentFolding[index] = newPos;
                occupied.insert(newPos);
                
                // Recursively fill the rest
                search(index + 1);
                
                // Backtrack
                occupied.erase(newPos);
            }
        }
    };
    
    // Place the first amino acid at origin
    currentFolding[0] = {0, 0};
    occupied.insert(currentFolding[0]);
    
    // Try all four directions for the second amino acid
    for (int dir = 0; dir < 1; dir++) {
        Point secondPos(dx[dir], dy[dir]);
        
        currentFolding[1] = secondPos;
        occupied.insert(secondPos);
        
        search(2);
        
        occupied.erase(secondPos);
    }
    
    return maxContacts;
}

// Worker function for each thread
void workerThread(int threadId, int length, 
                 atomic<long long>& totalContacts, 
                 atomic<int>& processedCount,
                 mutex& outputMutex) {
    long long totalProteins = (1LL << length);  // 2^length
    
    // Each thread processes a portion of the proteins
    for (long long i = threadId; i < totalProteins; i += 8) {  // 4 threads
        // The integer i directly represents the protein
        unsigned protein = (unsigned)i;
        int contacts = findMaxContacts(protein, length);
        
        // Update shared counter
        totalContacts += contacts;
        int processed = ++processedCount;
        
        // Report progress occasionally
        if (processed % 100 == 0 || processed == totalProteins || processed <= 5) {
            lock_guard<mutex> lock(outputMutex);
            
            // Convert protein to string for display
            string proteinStr;
            for (int j = 0; j < length; j++) {
                proteinStr += ((protein >> j) & 1) ? 'H' : 'P';
            }
            
            cout << "Processed " << processed << " / " << totalProteins << " proteins ("
                 << fixed << setprecision(2) << (100.0 * processed / totalProteins) << "%)" << endl;
            
            // Show details for a few examples
            if (processed <= 5) {
                cout << "  Thread " << threadId << " - Protein: " << proteinStr 
                     << ", Max contacts: " << contacts << endl;
            }
        }
    }
}

// Calculate average number of H-H contacts for proteins of given length
double calculateAverageMultiThreaded(int length) {
    // Shared counters
    atomic<long long> totalContacts(0);
    atomic<int> processedCount(0);
    mutex outputMutex;
    
    // Create 4 worker threads
    vector<thread> threads;
    for (int i = 0; i < 8; i++) {
        threads.emplace_back(workerThread, i, length, 
                            ref(totalContacts), ref(processedCount), 
                            ref(outputMutex));
    }
    
    // Wait for all threads to complete
    for (auto& t : threads) {
        t.join();
    }
    
    return static_cast<double>(totalContacts) / (1LL << length);
}

int main() {
    // Calculate average for length 8 (for verification)
    cout << "Calculating average for length 8 using 4 threads..." << endl;
    double avg8 = calculateAverageMultiThreaded(8);
    cout << "Average H-H contacts for length 8: " << fixed << setprecision(10) << avg8 << endl;
    cout << "Expected: 3.3203125" << endl << endl;
    
    // Calculate for length 15
    cout << "Calculating average for length 15 using 4 threads..." << endl;
    double avg15 = calculateAverageMultiThreaded(15);
    cout << "Average H-H contacts for length 15: " << fixed << setprecision(20) << avg15 << endl;
    
    return 0;
}