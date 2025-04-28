#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <string>
#include <map>
#include <unordered_map>
#include <cstdint>

// Fast 64-bit state representation class
class GameState {
public:
    // Constants for bit field sizes
    static constexpr size_t LARRY_BITS = 16;
    static constexpr size_t ROBIN_BITS = 16;
    static constexpr size_t SCORE_BITS = 8;
    
private:
    uint64_t value;

public:
    GameState() : value(0) {}
    
    GameState(int larry_memory_idx, int robin_memory_idx, int score, bool larry_winning) : value(0) {
        set_larry_memory(larry_memory_idx);
        set_robin_memory(robin_memory_idx);
        set_score(score);
        set_larry_winning(larry_winning);
    }
    
    void set_larry_memory(int idx) {
        // Clear the larry memory bits and set new value (16 bits)
        value = (value & ~0xFFFFULL) | (idx & 0xFFFFULL);
    }
    
    void set_robin_memory(int idx) {
        // Clear the robin memory bits and set new value (16 bits, shifted 16)
        value = (value & ~(0xFFFFULL << 16)) | ((static_cast<uint64_t>(idx) & 0xFFFFULL) << 16);
    }
    
    void set_score(int score) {
        // Clear the score bits and set new value (8 bits, shifted 32)
        value = (value & ~(0xFFULL << 32)) | ((static_cast<uint64_t>(score) & 0xFFULL) << 32);
    }
    
    void set_larry_winning(bool winning) {
        // Clear the winning bit and set new value (1 bit, shifted 40)
        value = (value & ~(1ULL << 40)) | (static_cast<uint64_t>(winning) << 40);
    }
    
    int get_larry_memory() const {
        return value & 0xFFFFULL;
    }
    
    int get_robin_memory() const {
        return (value >> 16) & 0xFFFFULL;
    }
    
    int get_score() const {
        return (value >> 32) & 0xFFULL;
    }
    
    bool get_larry_winning() const {
        return (value >> 40) & 1;
    }
    
    uint64_t get_value() const {
        return value;
    }
    
    bool operator<(const GameState& other) const {
        return value < other.value;
    }
    
    bool operator==(const GameState& other) const {
        return value == other.value;
    }
};

// Hash function for GameState to use in unordered_map
namespace std {
    template<>
    struct hash<GameState> {
        size_t operator()(const GameState& state) const {
            return hash<uint64_t>()(state.get_value());
        }
    };
}

std::vector<std::vector<int>> larry_transition_matrix;
std::vector<std::vector<int>> robin_transition_matrix;

std::vector<std::vector<int>> unique_arrangements; 
std::map<std::tuple<int, int, int, int, int>, int> unique_arrangements_map;

// Use unordered_map with GameState for better performance
std::unordered_map<GameState, double> dp;

void create_transition_matrix_larry() {
    // For each unique arrangement (state)
    larry_transition_matrix.resize(unique_arrangements.size(), std::vector<int>(10));
    for (size_t state = 0; state < unique_arrangements.size(); ++state) {
        const auto& current_arrangement = unique_arrangements[state];
        
        // For each possible number called (1-10)
        for (int num = 1; num <= 10; ++num) {
            std::vector<int> new_arrangement = current_arrangement;
            
            // Check if number is in current arrangement
            auto it = std::find(new_arrangement.begin(), new_arrangement.end(), num);
            
            if (it != new_arrangement.end()) {
                // If number exists, move it to front
                new_arrangement.erase(it);
                new_arrangement.insert(new_arrangement.begin(), num);
            } else {
                // If number doesn't exist, add to front and remove last
                new_arrangement.insert(new_arrangement.begin(), num);
                new_arrangement.pop_back();
            }
            
            // Find the index of the new arrangement
            auto tuple_key = std::make_tuple(new_arrangement[0], new_arrangement[1], new_arrangement[2], new_arrangement[3], new_arrangement[4]);
            larry_transition_matrix[state][num-1] = unique_arrangements_map[tuple_key];
            
        }
    }
}

void create_transition_matrix_robin() {
    // For each unique arrangement (state)
    robin_transition_matrix.resize(unique_arrangements.size(), std::vector<int>(10));
    for (size_t state = 0; state < unique_arrangements.size(); ++state) {
        const auto& current_arrangement = unique_arrangements[state];
        
        // For each possible number called (1-10)
        for (int num = 1; num <= 10; ++num) {
            std::vector<int> new_arrangement = current_arrangement;
            
            // Check if number is in current arrangement
            auto it = std::find(new_arrangement.begin(), new_arrangement.end(), num);
            
            if (it == new_arrangement.end()) {
                // If number doesn't exist, add to front and remove last
                new_arrangement.insert(new_arrangement.begin(), num);
                new_arrangement.pop_back();
            }
            
            // Find the index of the new arrangement
            auto tuple_key = std::make_tuple(new_arrangement[0], new_arrangement[1], new_arrangement[2], new_arrangement[3], new_arrangement[4]);
            robin_transition_matrix[state][num-1] = unique_arrangements_map[tuple_key];
            
            /*
            std::cout << "For number " << num << ": ";
            for (int n : current_arrangement) std::cout << n << " ";

            auto transition = unique_arrangements[robin_transition_matrix[state][num-1]];

            std::cout << "-->";
            for(int n: transition) std::cout << n << " ";
            std::cout << std::endl;
            */
        }
    }
}

bool in_memory(int memory, int number) {
    // memory is an index into unique_arrangements
    const auto& arrangement = unique_arrangements[memory];
    return std::find(arrangement.begin(), arrangement.end(), number) != arrangement.end();
}

int fix_larry_memory(int memory, int number) {
    // Use the pre-computed transition matrix
    return larry_transition_matrix[memory][number-1];
}

int fix_robin_memory(int memory, int number) {
    // Use the pre-computed transition matrix
    return robin_transition_matrix[memory][number-1];
}

double solve_bottom_up(int initial_larry_memory, int initial_robin_memory, bool larry_winning_initial) {
    // We'll use maps to store the probability for each state
    // Key: GameState
    // Value: probability of being in this state
    std::unordered_map<GameState, double> prev_round;
    std::unordered_map<GameState, double> curr_round;
    
    // Initialize with the starting state having 100% probability
    GameState initial_state(initial_larry_memory, initial_robin_memory, 0, larry_winning_initial);
    prev_round[initial_state] = 1.0;
    
    // For each round
    for (int round = 0; round < 50; round++) {
        // Clear current round data
        std::cout << "Doing round " << round << " (" << prev_round.size() << " states)" << std::endl;
        curr_round.clear();
        
        // For each state in the previous round
        for (const auto& state_prob : prev_round) {
            const GameState& state = state_prob.first;
            double probability = state_prob.second;
            
            int larry_memory = state.get_larry_memory();
            int robin_memory = state.get_robin_memory();
            int score = state.get_score();
            bool larry_winning = state.get_larry_winning();
            
            // For each possible number called
            for (int i = 1; i <= 10; i++) {
                int new_score = score;
                bool new_larry_winning = larry_winning;
                int new_larry_memory = larry_memory;
                int new_robin_memory = robin_memory;
                
                if (in_memory(larry_memory, i) && in_memory(robin_memory, i)) {
                    // Both remember - no score change
                    new_larry_memory = fix_larry_memory(larry_memory, i);
                } else if (in_memory(larry_memory, i)) {
                    if (larry_winning) {
                        new_score++;
                    } else {
                        new_score--;
                        if (new_score == 0) new_larry_winning = true;
                    }
                    new_larry_memory = fix_larry_memory(larry_memory, i);
                    new_robin_memory = fix_robin_memory(robin_memory, i);
                } else if (in_memory(robin_memory, i)) {
                    if (!larry_winning) {
                        new_score++;
                    } else {
                        new_score--;
                        if (new_score <= 0) {
                            new_larry_winning = false;
                            new_score = -1 * new_score;
                        }
                    }
                    new_larry_memory = fix_larry_memory(larry_memory, i);
                    new_robin_memory = fix_robin_memory(robin_memory, i);
                } else {
                    // Neither remembers - no score change
                    new_larry_memory = fix_larry_memory(larry_memory, i);
                    new_robin_memory = fix_robin_memory(robin_memory, i);
                }
                
                // Update the probability in the current round
                GameState new_state(new_larry_memory, new_robin_memory, new_score, new_larry_winning);
                curr_round[new_state] += probability * 0.1; // 10% chance for each number
            }
        }
        
        // Swap for next round
        prev_round = std::move(curr_round);
    }
    
    // Calculate the expected score
    double expected_score = 0.0;
    for (const auto& state_prob : prev_round) {
        const GameState& state = state_prob.first;
        double probability = state_prob.second;
        
        int larry_memory = state.get_larry_memory();
        int robin_memory = state.get_robin_memory();
        int score = state.get_score();
        
        expected_score += score * probability;
    }
    
    return expected_score;
}

void initialize() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::set<std::vector<int>> uniqueArrangements;
    
    // Generate arrangements with different numbers of zeros
    for (int zeros = 0; zeros <= 5; zeros++) {
        int non_zeros = 5 - zeros;
        
        // Create bitmask for selecting non-zero numbers
        std::vector<bool> bitmask(10, false);
        std::fill(bitmask.begin(), bitmask.begin() + non_zeros, true);
        
        // Iterate through all combinations of non-zero numbers
        do {
            // Extract the current non-zero number combination
            std::vector<int> combination;
            for (size_t i = 0; i < 10; ++i) {
                if (bitmask[i]) {
                    combination.push_back(numbers[i]);
                }
            }
            
            // Add zeros to the combination
            combination.resize(5, 0);
            
            // Generate all permutations
            do {
                std::vector<int> arrangement = combination;
                
                // Move all zeros to the back
                std::stable_partition(arrangement.begin(), arrangement.end(), 
                                     [](int n) { return n != 0; });
                
                uniqueArrangements.insert(arrangement);
                
            } while (std::next_permutation(combination.begin(), combination.end()));
            
        } while (std::prev_permutation(bitmask.begin(), bitmask.end()));
    }
    
    std::cout << "Total unique arrangements: " << uniqueArrangements.size() << std::endl;
    
    int count = 0;
    for(auto && s: uniqueArrangements) {
        unique_arrangements.emplace_back(s);
        // Convert vector to tuple for the map key
        auto tuple_key = std::make_tuple(s[0], s[1], s[2], s[3], s[4]);
        unique_arrangements_map[tuple_key] = count++;
    }

    // Initialize transition matrices with correct size
    larry_transition_matrix.resize(unique_arrangements.size(), std::vector<int>(10));
    robin_transition_matrix.resize(unique_arrangements.size(), std::vector<int>(10));
    
    create_transition_matrix_larry();
    create_transition_matrix_robin();
}

void debug_transition(const std::vector<int>& state, int number) {
    std::cout << "\nDebug transition for state: ";
    for (int num : state) std::cout << num << " ";
    std::cout << "and number: " << number << "\n";

    // Convert state to tuple for lookup
    auto tuple_key = std::make_tuple(state[0], state[1], state[2], state[3], state[4]);
    int state_idx = unique_arrangements_map.at(tuple_key);

    std::cout << state_idx << std::endl;

    // Get Larry's transition
    std::vector<int> larry_new = unique_arrangements[larry_transition_matrix[state_idx][number-1]];
    std::cout << "Larry's new state: ";
    for (int num : larry_new) std::cout << num << " ";
    std::cout << "\n";

    // Get Robin's transition
    std::vector<int> robin_new = unique_arrangements[robin_transition_matrix[state_idx][number-1]];
    std::cout << "Robin's new state: ";
    for (int num : robin_new) std::cout << num << " ";
    std::cout << "\n";
}

int main() {
    initialize();

    // Debug information first
    std::cout << "Total unique arrangements: " << unique_arrangements.size() << std::endl;
    
    // Print a few arrangements
    std::cout << "First few arrangements:" << std::endl;
    for(int i = 0; i < std::min(5, (int)unique_arrangements.size()); i++) {
        std::cout << "State " << i << ": ";
        for(int num : unique_arrangements[i]) {
            std::cout << num << " ";
        }
        std::cout << std::endl;
    }

    // Test transitions
    std::vector<int> initial_state = {1, 2, 5, 4, 3};
    debug_transition(initial_state, 5);

    // Run the simulation with bottom-up approach
    auto initial_key = std::make_tuple(0, 0, 0, 0, 0);
    int idx = unique_arrangements_map[initial_key];

    double expected_value = solve_bottom_up(idx, idx, true);
    std::cout << "Expected Value (Bottom-up): " << expected_value << std::endl;
    
    return 0;
}