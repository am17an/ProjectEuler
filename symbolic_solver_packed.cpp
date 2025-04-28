#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <vector>
#include <numeric>
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <functional> // for std::hash
#include <absl/container/flat_hash_map.h>
#ifdef _MSC_VER
#include <intrin.h> // For __popcnt on MSVC
// Define __builtin_ctz for MSVC if needed (using _BitScanForward)
unsigned long _BitScanForward(unsigned long* Index, unsigned long Mask);
inline int __builtin_ctz(uint32_t x) {
    unsigned long index;
    if (_BitScanForward(&index, x)) return index;
    return 32; // Undefined if x is 0
}
#else
#include <x86intrin.h> // For __builtin_popcount, __builtin_ctz on GCC/Clang
#endif


// --- Configuration ---
const int MEMORY_SIZE = 5;
const int TOTAL_SYMBOLS = 10; // 'a' through 'j'
const char PLACEHOLDER = '\0'; // Represents an empty slot

// --- Precomputation Data Structures ---
std::vector<std::vector<char>> unique_arrangements;
std::vector<uint32_t> arrangement_masks; // Parallel vector for masks
std::map<std::vector<char>, int> arrangement_to_index;
std::vector<std::vector<int>> larry_transitions;
std::vector<std::vector<int>> robin_transitions;
std::vector<int> canonical_map; // Map arrangement index to its canonical index

// --- State Packing ---
// Layout:
// Bits 0-15:  Larry's memory index (up to 65536 states)
// Bits 16-31: Robin's memory index (up to 65536 states)
// Bits 32-39: Score (8 bits, range -128 to 127, stored as 0-255)
// Total: 40 bits


const int SCORE_OFFSET = 128; // Offset for 8-bit score range [-128, 127] -> [0, 255]

uint64_t pack_state(int larry_idx, int robin_idx, int score) {
    uint64_t state = 0;
    state |= (static_cast<uint64_t>(larry_idx) & 0xFFFF);
    state |= (static_cast<uint64_t>(robin_idx) & 0xFFFF) << 16;
    // Offset score to be non-negative for packing (0 to 255)
    state |= (static_cast<uint64_t>(score + SCORE_OFFSET) & 0xFF) << 32;
    return state;
}

void unpack_state(uint64_t state, int& larry_idx, int& robin_idx, int& score) {
    larry_idx = state & 0xFFFF;
    robin_idx = (state >> 16) & 0xFFFF;
    // Unpack score and remove offset
    score = ((state >> 32) & 0xFF) - SCORE_OFFSET;
}

// --- Helper Functions ---
int symbol_to_index(char symbol) {
    if (symbol == PLACEHOLDER) return -1;
    return symbol - 'a';
}

char index_to_symbol(int idx) {
     if (idx < 0 || idx >= TOTAL_SYMBOLS) return PLACEHOLDER;
    return 'a' + idx;
}

// Check if a symbol is in a memory arrangement using precomputed mask
bool in_memory(int arrangement_idx, char symbol) {
    if (arrangement_idx < 0 || static_cast<size_t>(arrangement_idx) >= arrangement_masks.size()) return false;
    int sym_idx = symbol_to_index(symbol);
    if (sym_idx < 0) return false;
    // Check the corresponding bit in the precomputed mask
    return (arrangement_masks[arrangement_idx] >> sym_idx) & 1;
}

// Calculate bitmask for an arrangement
uint32_t calculate_mask(const std::vector<char>& arrangement) {
    uint32_t mask = 0;
    for (char c : arrangement) {
        int idx = symbol_to_index(c);
        if (idx >= 0) {
            mask |= (1u << idx);
        }
    }
    return mask;
}

// Count set bits (popcount)
inline int countSetBits(uint32_t n) {
#ifdef _MSC_VER
    return __popcnt(n);
#else
    return __builtin_popcount(n);
#endif
}

// Helper to convert arrangement to string for printing
std::string arrangement_to_string(const std::vector<char>& arr) {
    std::string s = "(";
    bool first = true;
    for (char c : arr) {
        if (!first) s += ",";
        s += (c == PLACEHOLDER ? '_' : c);
        first = false;
    }
    s += ")";
    return s;
}

// --- Precomputation Functions ---

// Generate unique arrangements, map them, and store masks
void generate_unique_arrangements() {
    std::vector<char> symbols(TOTAL_SYMBOLS);
    std::iota(symbols.begin(), symbols.end(), 'a');
    std::set<std::vector<char>> unique_set;

    // Generate combinations of symbols (k symbols out of TOTAL_SYMBOLS)
    for (int k = 0; k <= MEMORY_SIZE; ++k) { // k = number of non-placeholder symbols
        std::vector<bool> v(TOTAL_SYMBOLS);
        std::fill(v.begin() + TOTAL_SYMBOLS - k, v.end(), true); // Select k elements

        do {
            std::vector<char> current_selection_symbols;
            for (int i = 0; i < TOTAL_SYMBOLS; ++i) {
                if (v[i]) {
                    current_selection_symbols.push_back(symbols[i]);
                }
            }

            // Generate permutations of the selected k symbols
            std::sort(current_selection_symbols.begin(), current_selection_symbols.end());
            do {
                 std::vector<char> arrangement(MEMORY_SIZE, PLACEHOLDER);
                 for(int i = 0; i < k; ++i) {
                     arrangement[i] = current_selection_symbols[i];
                 }
                 unique_set.insert(arrangement);
            } while (std::next_permutation(current_selection_symbols.begin(), current_selection_symbols.end()));

        } while (std::next_permutation(v.begin(), v.end()));
    }

    // Populate the vector, map, and mask vector
    unique_arrangements.assign(unique_set.begin(), unique_set.end());
    arrangement_masks.resize(unique_arrangements.size());
    for (int i = 0; i < static_cast<int>(unique_arrangements.size()); ++i) {
        arrangement_to_index[unique_arrangements[i]] = i;
        arrangement_masks[i] = calculate_mask(unique_arrangements[i]); // Calculate and store mask
    }
    std::cout << "Generated " << unique_arrangements.size() << " unique memory arrangements." << std::endl;
}


// Corrected Apply Larry's update rule
std::vector<char> apply_larry_update(const std::vector<char>& arrangement, char symbol) {
    std::vector<char> memory_list;
    // Copy non-placeholder elements
    for(char c : arrangement) {
        if (c != PLACEHOLDER) {
            memory_list.push_back(c);
        }
    }

    auto it = std::find(memory_list.begin(), memory_list.end(), symbol);
    if (it != memory_list.end()) {
        // Found: remove and insert at front
        memory_list.erase(it);
        memory_list.insert(memory_list.begin(), symbol);
    } else {
        // Not found: insert at front, remove last if needed
        memory_list.insert(memory_list.begin(), symbol);
        if (memory_list.size() > MEMORY_SIZE) {
            memory_list.pop_back(); // Remove the actual last element
        }
    }
    // Pad with placeholders
    while (memory_list.size() < MEMORY_SIZE) {
        memory_list.push_back(PLACEHOLDER);
    }
    return memory_list;
}

// Corrected Apply Robin's update rule
std::vector<char> apply_robin_update(const std::vector<char>& arrangement, char symbol) {
     std::vector<char> memory_list;
     bool found = false;
     // Copy non-placeholder elements and check if symbol exists
    for(char c : arrangement) {
        if (c != PLACEHOLDER) {
            memory_list.push_back(c);
            if (c == symbol) {
                found = true;
            }
        }
    }

    if (found) {
        // Found: return original arrangement (padded correctly)
        std::vector<char> result = memory_list;
         while (result.size() < MEMORY_SIZE) {
            result.push_back(PLACEHOLDER);
        }
        return result;
    } else {
        // Not found: insert at front, remove last if needed
        memory_list.insert(memory_list.begin(), symbol);
        if (memory_list.size() > MEMORY_SIZE) {
            memory_list.pop_back(); // Remove the actual last element
        }
        // Pad with placeholders
        while (memory_list.size() < MEMORY_SIZE) {
            memory_list.push_back(PLACEHOLDER);
        }
        return memory_list;
    }
}


// Create transition matrices
void create_transition_matrices() {
    int num_states = unique_arrangements.size();
    if (num_states == 0) {
        std::cerr << "Error: No unique arrangements generated." << std::endl;
        return;
    }
    larry_transitions.resize(num_states, std::vector<int>(TOTAL_SYMBOLS));
    robin_transitions.resize(num_states, std::vector<int>(TOTAL_SYMBOLS));

    for (int i = 0; i < num_states; ++i) {
        const auto& current_arrangement = unique_arrangements[i];
        for (int j = 0; j < TOTAL_SYMBOLS; ++j) {
            char symbol_called = index_to_symbol(j);

            // Larry's transition
            std::vector<char> next_larry_arrangement = apply_larry_update(current_arrangement, symbol_called);
             if (arrangement_to_index.count(next_larry_arrangement)) {
                larry_transitions[i][j] = arrangement_to_index.at(next_larry_arrangement);
             } else {
                 std::cerr << "Error: Larry generated an unknown state for state " << i << " symbol " << symbol_called << std::endl;
                 larry_transitions[i][j] = i; // Fallback
             }

            // Robin's transition
            std::vector<char> next_robin_arrangement = apply_robin_update(current_arrangement, symbol_called);
             if (arrangement_to_index.count(next_robin_arrangement)) {
                 robin_transitions[i][j] = arrangement_to_index.at(next_robin_arrangement);
             } else {
                 std::cerr << "Error: Robin generated an unknown state for state " << i << " symbol " << symbol_called << std::endl;
                 robin_transitions[i][j] = i; // Fallback
             }
        }
    }
     std::cout << "Generated transition matrices." << std::endl;
}

// --- Canonicalization Precomputation ---

// Helper to find the canonical index for a given arrangement index
int find_canonical_index(int arrangement_idx,
                         const std::vector<std::vector<char>>& unique_arrangements,
                         const std::map<std::vector<char>, int>& arrangement_to_index) {
    if (arrangement_idx < 0 || static_cast<size_t>(arrangement_idx) >= unique_arrangements.size()) {
        std::cerr << "Error: Invalid arrangement index in find_canonical_index: " << arrangement_idx << std::endl;
        return arrangement_idx; // Fallback
    }
    const auto& current_arrangement = unique_arrangements[arrangement_idx];

    // Find unique non-placeholder symbols present
    std::set<char> present_symbols_set;
    for (char c : current_arrangement) {
        if (c != PLACEHOLDER) {
            present_symbols_set.insert(c);
        }
    }

    // If no symbols present (empty memory), it's already canonical
    if (present_symbols_set.empty()) {
        return arrangement_idx;
    }

    std::vector<char> present_symbols(present_symbols_set.begin(), present_symbols_set.end()); // Sorted

    // Create the renaming map to canonical symbols ('a', 'b', ...)
    std::map<char, char> renaming_map;
    for (size_t i = 0; i < present_symbols.size(); ++i) {
        renaming_map[present_symbols[i]] = 'a' + i;
    }

    // Apply the renaming to the original arrangement
    std::vector<char> canonical_arrangement = current_arrangement; // Copy structure
    for (size_t i = 0; i < canonical_arrangement.size(); ++i) {
        if (canonical_arrangement[i] != PLACEHOLDER) {
            canonical_arrangement[i] = renaming_map[canonical_arrangement[i]];
        }
    }

    // Find the index of this canonical arrangement
    auto it = arrangement_to_index.find(canonical_arrangement);
    if (it != arrangement_to_index.end()) {
        return it->second;
    } else {
        // This should not happen if generation was correct
        std::cerr << "Error: Canonical arrangement not found in map for original index " << arrangement_idx << ". Arrangement: ";
        for(char c : canonical_arrangement) std::cerr << (c == PLACEHOLDER ? '_' : c);
        std::cerr << std::endl;
        return arrangement_idx; // Fallback
    }
}

// Precompute the canonical map for all arrangements
void create_canonical_map() {
    int num_arrangements = unique_arrangements.size();
    if (num_arrangements == 0) {
        std::cerr << "Error: Cannot create canonical map before generating arrangements." << std::endl;
        return;
    }
    canonical_map.resize(num_arrangements);
    for (int i = 0; i < num_arrangements; ++i) {
        canonical_map[i] = find_canonical_index(i, unique_arrangements, arrangement_to_index);
    }
    std::cout << "Generated canonical map for L==R isomorphism." << std::endl;

    // --- Debug Print for Canonical Map ---
    std::cout << "Canonical Map Examples:" << std::endl;
    int print_count = 0;
    std::vector<int> specific_indices_to_print = {100, 500, 1000, 5000, 10000}; // Example indices
    int specific_idx_ptr = 0;
    for (int i = 0; i < num_arrangements; ++i) {
        bool should_print = false;
        if (print_count < 5) { // Print first 5
            should_print = true;
            print_count++;
        } else {
            // Check if it's one of the specific indices we want to see
            while (specific_idx_ptr < specific_indices_to_print.size() && specific_indices_to_print[specific_idx_ptr] < i) {
                specific_idx_ptr++;
            }
            if (specific_idx_ptr < specific_indices_to_print.size() && specific_indices_to_print[specific_idx_ptr] == i) {
                 should_print = true;
                 specific_idx_ptr++;
            }
        }

        if (should_print) {
             int canonical_idx = canonical_map[i];
             std::cout << "  Orig Idx " << i << ": " << arrangement_to_string(unique_arrangements[i])
                       << " -> Canon Idx " << canonical_idx << ": " << arrangement_to_string(unique_arrangements[canonical_idx]) << std::endl;
        }
    }
    // --- End Debug Print ---
}


// --- DP Solver ---
double solve_dp_packed(int n_rounds) {
    std::cout << "Solving with packed state DP for " << n_rounds << " rounds..." << std::endl;
    std::cout << "Using symbol renaming canonicalization" << std::endl;
    auto start_time = std::chrono::high_resolution_clock::now();

    // Find index of the initial empty state
    std::vector<char> initial_mem(MEMORY_SIZE, PLACEHOLDER);
     if (!arrangement_to_index.count(initial_mem)) {
         std::cerr << "Error: Initial empty memory state not found in precomputed arrangements." << std::endl;
         return -1.0; 
     }
    int initial_idx = arrangement_to_index.at(initial_mem);

    uint64_t initial_state_key = pack_state(initial_idx, initial_idx, 0);

    absl::flat_hash_map<uint64_t, double> prev_round;
    prev_round[initial_state_key] = 1.0;

    double probability_threshold = 1e-30; // Keep this very small

    for (int round_num = 0; round_num < n_rounds; ++round_num) {
        std::cout << "Round " << round_num << ": " << prev_round.size() << " states" << std::endl;
        absl::flat_hash_map<uint64_t, double> curr_round;
        int processed_states = 0;

        for (const auto& pair : prev_round) {
            uint64_t current_state_key = pair.first;
            double probability = pair.second;

            // Skip processing states below threshold
            if (probability < probability_threshold) {
                continue;
            }
            processed_states++;

            int larry_mem_idx, robin_mem_idx, score;
            unpack_state(current_state_key, larry_mem_idx, robin_mem_idx, score);

            //int canonical_idx = arrangement_to_index.at({'a', 'b', 'c', 'd', 'e'});

            // Get masks for current memory arrangements
            uint32_t larry_mask = arrangement_masks[larry_mem_idx];
            uint32_t robin_mask = arrangement_masks[robin_mem_idx];

            // Calculate category masks
            uint32_t both_mask = larry_mask & robin_mask;
            uint32_t larry_only_mask = larry_mask & ~robin_mask;
            uint32_t robin_only_mask = robin_mask & ~larry_mask;
            uint32_t all_symbols_mask = (1u << TOTAL_SYMBOLS) - 1;
            uint32_t neither_mask = ~(larry_mask | robin_mask) & all_symbols_mask;

            // --- Process Categories ---

            // Case 1: Both players remember (iterate through symbols in mask)
            uint32_t temp_both_mask = both_mask;
            while (temp_both_mask != 0) {
                int i = __builtin_ctz(temp_both_mask); // Find index of first set bit
                // Score doesn't change
                int next_score = score;
                // Get next memory indices
                int next_l_idx = larry_transitions[larry_mem_idx][i];
                int next_r_idx = robin_transitions[robin_mem_idx][i];

                // Apply canonicalization if next L==R
                uint64_t next_state_key;
                //if (next_l_idx == next_r_idx && __builtin_popcount(arrangement_masks[next_l_idx]) == 5) {
                //    next_state_key = pack_state(canonical_idx, canonical_idx, next_score, next_larry_serving);
                //} else {
                    next_state_key = pack_state(next_l_idx, next_r_idx, next_score);
                //}
                curr_round[next_state_key] += probability * (1.0 / TOTAL_SYMBOLS);
                temp_both_mask &= ~(1u << i); // Clear the processed bit
            }

            // Case 2: Only Larry remembers (iterate through symbols in mask)
            uint32_t temp_larry_only_mask = larry_only_mask;
             while (temp_larry_only_mask != 0) {
                int i = __builtin_ctz(temp_larry_only_mask);
                // Apply score rules
                int next_score = score+1;
                next_score = std::clamp(next_score, -128, 127);
                // Get next memory indices
                int next_l_idx = larry_transitions[larry_mem_idx][i];
                int next_r_idx = robin_transitions[robin_mem_idx][i];

                // Apply canonicalization if next L==R
                uint64_t next_state_key;
                //if (next_l_idx == next_r_idx && __builtin_popcount(arrangement_masks[next_l_idx]) == 5) {
                //    next_state_key = pack_state(canonical_idx, canonical_idx, next_score, next_larry_serving);
                //} else {
                    next_state_key = pack_state(next_l_idx, next_r_idx, next_score);
                //}
                curr_round[next_state_key] += probability * (1.0 / TOTAL_SYMBOLS);
                temp_larry_only_mask &= ~(1u << i);
            }

            uint32_t temp_robin_only_mask = robin_only_mask;
            // Case 3: Only Robin remembers (use one representative symbol)
            while (temp_robin_only_mask != 0) {
                int i = __builtin_ctz(temp_robin_only_mask); // Index of first symbol in category
                 // Apply score rules
                int next_score = score - 1;
                // Get next memory indices
                int next_l_idx = larry_transitions[larry_mem_idx][i];
                int next_r_idx = robin_transitions[robin_mem_idx][i];

                // Apply canonicalization if next L==R
                uint64_t next_state_key;
                //if (next_l_idx == next_r_idx && __builtin_popcount(arrangement_masks[next_l_idx]) == 5) {
                    //next_state_key = pack_state(canonical_idx, canonical_idx, next_score, next_larry_serving);
                //} else {
                    next_state_key = pack_state(next_l_idx, next_r_idx, next_score);
                //}
                int category_count = countSetBits(robin_only_mask);
                //curr_round[next_state_key] += probability * (static_cast<double>(category_count) / TOTAL_SYMBOLS);
                curr_round[next_state_key] += probability * (1.0 / TOTAL_SYMBOLS);
                temp_robin_only_mask &= ~(1u << i);
            }

            // Case 4: Neither remembers (use one representative symbol)
            if (neither_mask != 0) {
                 int i = __builtin_ctz(neither_mask); // Index of first symbol in category
                // Score doesn't change
                int next_score = score;
                 // Get next memory indices
                int next_l_idx = larry_transitions[larry_mem_idx][i];
                int next_r_idx = robin_transitions[robin_mem_idx][i];

                // Apply canonicalization if next L==R
                uint64_t next_state_key;
                //if (next_l_idx == next_r_idx && __builtin_popcount(arrangement_masks[next_l_idx]) == 5) {
                //    next_state_key = pack_state(canonical_idx, canonical_idx, next_score, next_larry_serving);
                //} else {
                    next_state_key = pack_state(next_l_idx, next_r_idx, next_score); 
                //}
                int category_count = countSetBits(neither_mask);
                curr_round[next_state_key] += probability * (static_cast<double>(category_count) / TOTAL_SYMBOLS);
            }
        }

        // Pruning after accumulating probabilities for the round
        /*
        for(const auto& pair : curr_round) {
            if (pair.second >= probability_threshold) {
                next_prev_round[pair.first] = pair.second;
            } else {
                actual_pruned_count++; // Count states pruned *after* accumulation
            }
        }
        */

        prev_round = std::move(curr_round); // Use move for efficiency
    }

    double expected_score = 0.0;
    double total_prob = 0.0;
    for (const auto& pair : prev_round) {
        int larry_mem_idx, robin_mem_idx, score;
        unpack_state(pair.first, larry_mem_idx, robin_mem_idx, score);
        expected_score += std::abs(score) * pair.second;
        total_prob += pair.second;
    }
     std::cout << "Final total probability: " << total_prob << std::endl;


    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;
    std::cout << "Packed DP solution completed in " << elapsed.count() << " seconds" << std::endl;

    return expected_score;
}


// --- Main Execution ---
int main() {
    auto precompute_start = std::chrono::high_resolution_clock::now();
    generate_unique_arrangements();
    create_transition_matrices();
    create_canonical_map(); // Add call to precompute canonical map
    auto precompute_end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> precompute_elapsed = precompute_end - precompute_start;
    std::cout << "Precomputation completed in " << precompute_elapsed.count() << " seconds." << std::endl;


    int rounds = 50; // Set rounds for verification
    auto expected_score = solve_dp_packed(rounds);

    // Verification
    double target_score = 0.24854740;
    printf("Expected Score (Packed, %d rounds): %.8f\n", rounds, expected_score);

    return 0;
}
