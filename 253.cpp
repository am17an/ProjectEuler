#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <set>
#include <cmath>
#include <iomanip>
#include <thread>
#include <atomic>
#include <mutex>
#include <chrono>

class SegmentTracker {
private:
    std::set<std::pair<int, int>> segments; // Each segment represented as (start, end)
    
public:
    void addNumber(int num) {
        std::vector<std::pair<int, int>> toRemove;
        int newStart = num, newEnd = num;
        
        // Check which existing segments this number can connect to
        for (const auto& segment : segments) {
            if (segment.second == num - 1) { // num extends this segment to the right
                newStart = std::min(newStart, segment.first);
                toRemove.push_back(segment);
            } else if (segment.first == num + 1) { // num extends this segment to the left
                newEnd = std::max(newEnd, segment.second);
                toRemove.push_back(segment);
            }
        }
        
        // Remove the segments that we're merging
        for (const auto& segment : toRemove) {
            segments.erase(segment);
        }
        
        // Add the new merged segment
        segments.insert({newStart, newEnd});
    }
    
    int getSegmentCount() const {
        return segments.size();
    }
    
    void clear() {
        segments.clear();
    }
};

int simulateOnce(std::mt19937& gen) {
    std::vector<int> permutation(40);
    for (int i = 0; i < 40; ++i) {
        permutation[i] = i + 1;
    }
    
    std::shuffle(permutation.begin(), permutation.end(), gen);
    
    SegmentTracker tracker;
    int maxSegments = 0;
    
    for (int num : permutation) {
        tracker.addNumber(num);
        maxSegments = std::max(maxSegments, tracker.getSegmentCount());
    }
    
    return maxSegments;
}

// Thread worker function
void workerThread(int threadId, int simulationsPerBatch, 
                 std::atomic<long long>& totalRuns, 
                 std::atomic<long long>& totalSum, 
                 std::atomic<long long>& totalSumSquared,
                 std::atomic<bool>& shouldStop) {
    
    std::random_device rd;
    std::mt19937 gen(rd() + threadId); // Different seed per thread
    
    while (!shouldStop.load()) {
        long long localSum = 0;
        long long localSumSquared = 0;
        
        // Run a batch of simulations
        for (int i = 0; i < simulationsPerBatch; ++i) {
            int result = simulateOnce(gen);
            localSum += result;
            localSumSquared += static_cast<long long>(result) * result;
        }
        
        // Atomically update global counters
        totalRuns.fetch_add(simulationsPerBatch);
        totalSum.fetch_add(localSum);
        totalSumSquared.fetch_add(localSumSquared);
    }
}

int main() {
    const int NUM_THREADS = std::thread::hardware_concurrency();
    const int SIMULATIONS_PER_BATCH = 1000;
    const double TARGET_HALF_WIDTH = 1e-6;  // Target half-width of confidence interval (6 decimal places)
    const int MIN_RUNS = 10000;
    const int CHECK_INTERVAL = 100000; // Check convergence less frequently to reduce overhead
    
    std::cout << "Running multi-threaded Monte Carlo simulation for expected maximum segments..." << std::endl;
    std::cout << "Using " << NUM_THREADS << " threads" << std::endl;
    std::cout << "Target precision: ±" << TARGET_HALF_WIDTH << " (95% confidence interval)" << std::endl;
    std::cout << std::endl;
    
    std::atomic<long long> totalRuns{0};
    std::atomic<long long> totalSum{0};
    std::atomic<long long> totalSumSquared{0};
    std::atomic<bool> shouldStop{false};
    
    // Start worker threads
    std::vector<std::thread> threads;
    for (int i = 0; i < NUM_THREADS; ++i) {
        threads.emplace_back(workerThread, i, SIMULATIONS_PER_BATCH, 
                           std::ref(totalRuns), std::ref(totalSum), 
                           std::ref(totalSumSquared), std::ref(shouldStop));
    }
    
    // Main monitoring loop
    long long lastCheckRuns = 0;
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1)); // Check every second
        
        long long currentRuns = totalRuns.load();
        
        if (currentRuns >= lastCheckRuns + CHECK_INTERVAL || currentRuns >= MIN_RUNS) {
            double mean = static_cast<double>(totalSum.load()) / currentRuns;
            
            if (currentRuns >= MIN_RUNS) {
                // Calculate sample variance and standard error
                double variance = (static_cast<double>(totalSumSquared.load()) / currentRuns) - (mean * mean);
                double standardError = std::sqrt(variance / currentRuns);
                
                // 95% confidence interval half-width (using normal approximation)
                double halfWidth = 1.96 * standardError;
                
                if (halfWidth <= TARGET_HALF_WIDTH) {
                    shouldStop.store(true);
                    
                    // Wait for all threads to finish
                    for (auto& thread : threads) {
                        thread.join();
                    }
                    
                    // Final calculations with exact final counts
                    long long finalRuns = totalRuns.load();
                    double finalMean = static_cast<double>(totalSum.load()) / finalRuns;
                    double finalVariance = (static_cast<double>(totalSumSquared.load()) / finalRuns) - (finalMean * finalMean);
                    double finalStandardError = std::sqrt(finalVariance / finalRuns);
                    double finalHalfWidth = 1.96 * finalStandardError;
                    
                    std::cout << std::endl << "*** CONVERGED ***" << std::endl;
                    std::cout << "Converged after " << finalRuns << " runs." << std::endl;
                    std::cout << "95% Confidence interval: [" << std::fixed << std::setprecision(6) 
                             << (finalMean - finalHalfWidth) << ", " << (finalMean + finalHalfWidth) << "]" << std::endl;
                    std::cout << "Half-width: " << std::scientific << std::setprecision(2) << finalHalfWidth << std::endl;
                    std::cout << "Standard error: " << finalStandardError << std::endl;
                    std::cout << std::fixed << std::setprecision(6) 
                             << "Expected maximum segments: " << finalMean << " ± " << std::scientific << std::setprecision(2) << finalHalfWidth << std::endl;
                    break;
                }
                
                std::cout << "Runs: " << std::setw(10) << currentRuns 
                         << " | Mean: " << std::fixed << std::setprecision(6) << mean
                         << " | 95% CI: ±" << std::scientific << std::setprecision(2) << halfWidth 
                         << " | Rate: " << std::fixed << std::setprecision(0) << (currentRuns - lastCheckRuns) << " runs/sec" << std::endl;
            } else {
                std::cout << "Runs: " << std::setw(10) << currentRuns 
                         << " | Mean: " << std::fixed << std::setprecision(6) << mean
                         << " | (Building statistics...)" << std::endl;
            }
            
            lastCheckRuns = currentRuns;
        }
    }
    
    return 0;
}
