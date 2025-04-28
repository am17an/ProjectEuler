#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <map>
#include <set>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <numeric>

// Forward declaration for hash function
class SymbolicState;
namespace std {
    template<> struct hash<SymbolicState>;
}

// Class to represent a symbolic state of the memory game
class SymbolicState {
public:
    // Vectors to represent ordered memory (newest element first)
    std::vector<char> larry_memory;
    std::vector<char> robin_memory;
    // Score (positive means Larry is ahead, negative means Robin is ahead)
    int score;
    // Who has the serve (true for Larry, false for Robin)
    bool larry_serving;

    SymbolicState(const std::vector<char>& larry_mem, const std::vector<char>& robin_mem,
                  int score_val, bool larry_serv)
        : larry_memory(larry_mem), robin_memory(robin_mem), score(score_val), larry_serving(larry_serv) {}

    // Equality operator for use in maps
    bool operator==(const SymbolicState& other) const {
        return larry_memory == other.larry_memory &&
               robin_memory == other.robin_memory &&
               score == other.score &&
               larry_serving == other.larry_serving;
    }

    // String representation for debugging
    std::string toString() const {
        std::string larry_mem = "";
        for (size_t i = 0; i < larry_memory.size(); ++i) {
            if (i > 0) larry_mem += ",";
            larry_mem += larry_memory[i];
        }
        if (larry_mem.empty()) larry_mem = "∅";

        std::string robin_mem = "";
        for (size_t i = 0; i < robin_memory.size(); ++i) {
            if (i > 0) robin_mem += ",";
            robin_mem += robin_memory[i];
        }
        if (robin_mem.empty()) robin_mem = "∅";

        std::string serving = larry_serving ? "L" : "R";
        return "(" + larry_mem + "|" + robin_mem + "|" + std::to_string(score) + "|" + serving + ")";
    }
};

// Hash function for SymbolicState to use in unordered_map
namespace std {
    template<>
    struct hash<SymbolicState> {
        size_t operator()(const SymbolicState& state) const {
            // Combine hashes of all components
            size_t hash_val = 0;

            // Hash larry_memory
            for (char c : state.larry_memory) {
                hash_val = hash_val * 31 + std::hash<char>()(c);
            }

            // Hash robin_memory
            for (char c : state.robin_memory) {
                hash_val = hash_val * 31 + std::hash<char>()(c);
            }

            // Hash score and larry_serving
            hash_val = hash_val * 31 + std::hash<int>()(state.score);
            hash_val = hash_val * 31 + std::hash<bool>()(state.larry_serving);

            return hash_val;
        }
    };
}

class SymbolicSolver {
private:
    int memory_size;
    int total_symbols;
    std::vector<char> symbols;
    double probability_threshold;

public:
    SymbolicSolver(int mem_size = 5, int tot_symbols = 10)
        : memory_size(mem_size), total_symbols(tot_symbols), probability_threshold(1e-40) {
        // Initialize symbols (a, b, c, ...)
        symbols.resize(total_symbols);
        for (int i = 0; i < total_symbols; ++i) {
            symbols[i] = 'a' + i;
        }
    }

    // Update Larry's memory according to his rule
    std::vector<char> update_larry_memory(const std::vector<char>& memory, char symbol) {
        std::vector<char> memory_list = memory;

        // If symbol is in memory, move it to the front
        auto it = std::find(memory_list.begin(), memory_list.end(), symbol);
        if (it != memory_list.end()) {
            memory_list.erase(it);
            memory_list.insert(memory_list.begin(), symbol);
        } else {
            // Add to front, remove last if needed
            memory_list.insert(memory_list.begin(), symbol);
            if (memory_list.size() > static_cast<size_t>(memory_size)) {
                memory_list.pop_back();
            }
        }

        return memory_list;
    }

    // Update Robin's memory according to her rule
    std::vector<char> update_robin_memory(const std::vector<char>& memory, char symbol) {
        // If symbol is in memory, do nothing
        if (std::find(memory.begin(), memory.end(), symbol) != memory.end()) {
            return memory;
        } else {
            // Add to front, remove last if needed
            std::vector<char> memory_list = memory;
            memory_list.insert(memory_list.begin(), symbol);
            if (memory_list.size() > static_cast<size_t>(memory_size)) {
                memory_list.pop_back();
            }
            return memory_list;
        }
    }

    // Compute the next state after a symbol is called
    SymbolicState get_next_state(const SymbolicState& state, char symbol) {
        bool larry_remembers = std::find(state.larry_memory.begin(), state.larry_memory.end(), symbol) != state.larry_memory.end();
        bool robin_remembers = std::find(state.robin_memory.begin(), state.robin_memory.end(), symbol) != state.robin_memory.end();

        // Calculate new score and serving status
        int new_score = state.score;
        bool new_larry_serving = state.larry_serving;

        if (larry_remembers && robin_remembers) {
            // Both remember - no score change
        } else if (larry_remembers) {
            // Only Larry remembers
            if (state.larry_serving) {
                new_score += 1;
            } else {
                new_score -= 1;
                if (new_score == 0) {
                    new_larry_serving = true;
                }
            }
        } else if (robin_remembers) {
            // Only Robin remembers
            if (!state.larry_serving) {
                new_score += 1;
            } else {
                new_score -= 1;
                if (new_score <= 0) {
                    new_larry_serving = false;
                    new_score = std::abs(new_score);  // Convert to positive
                }
            }
        }

        // Update memories
        std::vector<char> new_larry_memory = update_larry_memory(state.larry_memory, symbol);
        std::vector<char> new_robin_memory = update_robin_memory(state.robin_memory, symbol);

        return SymbolicState(new_larry_memory, new_robin_memory, new_score, new_larry_serving);
    }

    // Solve using dynamic programming approach
    std::pair<double, std::unordered_map<SymbolicState, double>> solve_dp(int n_rounds) {
        std::cout << "Solving with dynamic programming for " << n_rounds << " rounds..." << std::endl;
        auto start_time = std::chrono::high_resolution_clock::now();

        // Start with empty memories
        SymbolicState initial_state(std::vector<char>(), std::vector<char>(), 0, true);

        // Dictionary to store probabilities of each state
        std::unordered_map<SymbolicState, double> prev_round;
        prev_round[initial_state] = 1.0;

        // For each round
        for (int round_num = 0; round_num < n_rounds; ++round_num) {
            std::cout << "Round " << round_num << ": " << prev_round.size() << " states" << std::endl;
            std::unordered_map<SymbolicState, double> curr_round;
            int pruned_states = 0;
            int processed_states = 0;

            // For each state in previous round
            for (const auto& [state, probability] : prev_round) {
                // Skip low probability states
                if (probability < probability_threshold) {
                    pruned_states++;
                    continue;
                }

                processed_states++;

                // Categorize symbols by their presence in memory
                std::set<char> larry_memory_set(state.larry_memory.begin(), state.larry_memory.end());
                std::set<char> robin_memory_set(state.robin_memory.begin(), state.robin_memory.end());

                // Find symbols in both memories
                std::set<char> both_remember;
                std::set_intersection(
                    larry_memory_set.begin(), larry_memory_set.end(),
                    robin_memory_set.begin(), robin_memory_set.end(),
                    std::inserter(both_remember, both_remember.begin())
                );

                // Find symbols only in Larry's memory
                std::set<char> larry_only;
                std::set_difference(
                    larry_memory_set.begin(), larry_memory_set.end(),
                    robin_memory_set.begin(), robin_memory_set.end(),
                    std::inserter(larry_only, larry_only.begin())
                );

                // Find symbols only in Robin's memory
                std::set<char> robin_only;
                std::set_difference(
                    robin_memory_set.begin(), robin_memory_set.end(),
                    larry_memory_set.begin(), larry_memory_set.end(),
                    std::inserter(robin_only, robin_only.begin())
                );

                // Calculate number of symbols in neither memory
                int total_remembered = both_remember.size() + larry_only.size() + robin_only.size();
                int neither_count = total_symbols - total_remembered;

                // Case 1: Both players remember (each symbol leads to a different state for Larry)
                if (!both_remember.empty()) {
                    for (char symbol : both_remember) {
                        SymbolicState next_state = get_next_state(state, symbol);
                        // Probability = 1 / total_symbols for each symbol
                        double new_prob = probability * (1.0 / total_symbols);
                        if (new_prob >= probability_threshold) {
                            curr_round[next_state] += new_prob;
                        }
                    }
                }

                // Case 2: Only Larry remembers (each symbol leads to a different state for Larry)
                if (!larry_only.empty()) {
                    for (char symbol : larry_only) {
                        SymbolicState next_state = get_next_state(state, symbol);
                        // Probability = 1 / total_symbols for each symbol
                        double new_prob = probability * (1.0 / total_symbols);
                        if (new_prob >= probability_threshold) {
                            curr_round[next_state] += new_prob;
                        }
                    }
                }

                // Case 3: Only Robin remembers
                if (!robin_only.empty()) {
                    // Use the first symbol alphabetically for deterministic behavior
                    char symbol = *robin_only.begin();
                    SymbolicState next_state = get_next_state(state, symbol);
                    // Probability = (number only in Robin's memory) / total_symbols
                    double new_prob = probability * (static_cast<double>(robin_only.size()) / total_symbols);
                    if (new_prob >= probability_threshold) {
                        curr_round[next_state] += new_prob;
                    }
                }

                // Case 4: Neither remembers
                if (neither_count > 0) {
                    // Use a representative new symbol (one that's not in either memory)
                    std::set<char> used_symbols;
                    std::set_union(
                        larry_memory_set.begin(), larry_memory_set.end(),
                        robin_memory_set.begin(), robin_memory_set.end(),
                        std::inserter(used_symbols, used_symbols.begin())
                    );

                    std::set<char> available_symbols;
                    for (char symbol : symbols) {
                        if (used_symbols.find(symbol) == used_symbols.end()) {
                            available_symbols.insert(symbol);
                        }
                    }

                    if (!available_symbols.empty()) {
                        // Use the first symbol alphabetically for deterministic behavior
                        char symbol = *available_symbols.begin();
                        SymbolicState next_state = get_next_state(state, symbol);
                        // Probability = (number in neither memory) / total_symbols
                        double new_prob = probability * (static_cast<double>(neither_count) / total_symbols);
                        if (new_prob >= probability_threshold) {
                            curr_round[next_state] += new_prob;
                        }
                    }
                }
            }

            std::cout << "  Processed " << processed_states << " states, pruned " << pruned_states << " low-probability states" << std::endl;
            prev_round = curr_round;
        }

        // Calculate expected score
        double expected_score = 0.0;
        for (const auto& [state, probability] : prev_round) {
            expected_score += state.score * probability;
        }

        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end_time - start_time;
        std::cout << "DP solution completed in " << elapsed.count() << " seconds" << std::endl;

        return {expected_score, prev_round};
    }

    // Print statistics about the states
    void print_state_statistics(const std::unordered_map<SymbolicState, double>& states_dict) {
        std::map<int, int> score_counts;
        std::map<int, int> larry_memory_sizes;
        std::map<int, int> robin_memory_sizes;
        std::map<int, double> score_probability;
        double total_probability = 0.0;

        for (const auto& [state, prob] : states_dict) {
            score_counts[state.score]++;
            larry_memory_sizes[state.larry_memory.size()]++;
            robin_memory_sizes[state.robin_memory.size()]++;
            score_probability[state.score] += prob;
            total_probability += prob;
        }

        std::cout << "\nState Statistics:" << std::endl;
        std::cout << "Total states: " << states_dict.size() << std::endl;
        std::cout << "Total probability: " << total_probability << std::endl;

        std::cout << "\nScore distribution:" << std::endl;
        for (const auto& [score, count] : score_counts) {
            std::cout << "  Score " << score << ": " << count << " states, probability: "
                      << score_probability[score] << std::endl;
        }

        // Calculate expected score
        double expected_score = 0.0;
        for (const auto& [score, prob] : score_probability) {
            expected_score += score * prob;
        }
        std::cout << "\nExpected score: " << expected_score << std::endl;

        std::cout << "\nLarry memory size distribution:" << std::endl;
        for (const auto& [size, count] : larry_memory_sizes) {
            std::cout << "  Size " << size << ": " << count << " states" << std::endl;
        }

        std::cout << "\nRobin memory size distribution:" << std::endl;
        for (const auto& [size, count] : robin_memory_sizes) {
            std::cout << "  Size " << size << ": " << count << " states" << std::endl;
        }
    }

    // Print details of the highest probability states
    void analyze_high_probability_states(const std::unordered_map<SymbolicState, double>& states_dict, int top_n = 10) {
        // Convert to vector for sorting
        std::vector<std::pair<SymbolicState, double>> sorted_states(states_dict.begin(), states_dict.end());

        // Sort by probability (descending)
        std::sort(sorted_states.begin(), sorted_states.end(),
                 [](const auto& a, const auto& b) { return a.second > b.second; });

        int num_to_show = std::min(top_n, static_cast<int>(sorted_states.size()));
        std::cout << "\nTop " << num_to_show << " highest probability states:" << std::endl;
        double total_prob_shown = 0.0;

        for (int i = 0; i < num_to_show; ++i) {
            const auto& [state, prob] = sorted_states[i];
            std::cout << "  " << (i+1) << ". " << state.toString() << " - Probability: " << prob << std::endl;
            total_prob_shown += prob;

            // Analyze this state
            std::set<char> larry_set(state.larry_memory.begin(), state.larry_memory.end());
            std::set<char> robin_set(state.robin_memory.begin(), state.robin_memory.end());

            std::set<char> both;
            std::set_intersection(
                larry_set.begin(), larry_set.end(),
                robin_set.begin(), robin_set.end(),
                std::inserter(both, both.begin())
            );

            std::set<char> larry_only;
            std::set_difference(
                larry_set.begin(), larry_set.end(),
                robin_set.begin(), robin_set.end(),
                std::inserter(larry_only, larry_only.begin())
            );

            std::set<char> robin_only;
            std::set_difference(
                robin_set.begin(), robin_set.end(),
                larry_set.begin(), larry_set.end(),
                std::inserter(robin_only, robin_only.begin())
            );

            std::set<char> union_set;
            std::set_union(
                larry_set.begin(), larry_set.end(),
                robin_set.begin(), robin_set.end(),
                std::inserter(union_set, union_set.begin())
            );
            int neither = total_symbols - union_set.size();

            std::cout << "    Both remember: " << both.size() << " symbols" << std::endl;
            std::cout << "    Larry only: " << larry_only.size() << " symbols" << std::endl;
            std::cout << "    Robin only: " << robin_only.size() << " symbols" << std::endl;
            std::cout << "    Neither: " << neither << " symbols" << std::endl;
        }

        std::cout << "\nTotal probability of top " << num_to_show << " states: " << total_prob_shown << std::endl;
    }
};

// Main execution
int main() {
    // Create a solver with memory size 5 and 10 symbols
    SymbolicSolver solver(5, 10);
    int rounds = 25;

    auto start_time = std::chrono::high_resolution_clock::now();
    auto [expected_score, final_states] = solver.solve_dp(rounds);
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    printf("Expected: %.8f\n", expected_score);
    std::cout << "Total computation time: " << elapsed.count() << " seconds" << std::endl;

    // Print state statistics
//    solver.print_state_statistics(final_states);

    // Analyze high probability states
//    solver.analyze_high_probability_states(final_states);

    return 0;
}
