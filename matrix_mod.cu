#include <iostream>
#include <vector> // Using vector for easier host-side matrix handling
#include <cuda_runtime.h>
#include <stdexcept> // For error handling

// Define constants based on the problem
const int N = 2000;
const int32_t MOD = 20092010;
const int64_t K = 1000000000000000000LL; // k = 10^18

// --- CUDA Error Handling Macro ---
#define CUDA_CHECK(call)                                                  \
do {                                                                      \
    cudaError_t err = call;                                               \
    if (err != cudaSuccess) {                                             \
        fprintf(stderr, "CUDA Error at %s:%d - %s\n", __FILE__, __LINE__, \
                cudaGetErrorString(err));                                 \
        throw std::runtime_error(cudaGetErrorString(err));                \
    }                                                                     \
} while (0)

// --- GPU Matrix Multiplication Kernel (Unchanged) ---
__global__ void matmul_mod(const int64_t* A, const int64_t* B, int64_t* C) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        int64_t val = 0;
        for (int k = 0; k < N; ++k) {
            // Fetch a and b, ensuring they are already mod MOD if matrices A, B contain results from previous steps
            // Note: If initial A, B elements could be >> MOD or negative, applying initial modulo is crucial.
            // Here, intermediate results are always kept modulo MOD.
            int64_t a_val = A[row * N + k];
            int64_t b_val = B[k * N + col];

            // Intermediate product (a_val * b_val) must fit in int64_t.
            // max(a_val*b_val) ~ (MOD-1)*(MOD-1) ~ 4e14, which fits in int64_t (max ~9e18)
            int64_t product = (a_val * b_val) % MOD;

            // Accumulate value
            val = (val + product) % MOD;
        }
        // Ensure result is positive
        C[row * N + col] = (val + MOD) % MOD;
    }
}

// --- GPU Matrix Multiplication Function (Error handling added) ---
void gpu_matrix_multiply(int64_t* d_A, int64_t* d_B, int64_t* d_C) {
    dim3 threadsPerBlock(16, 16);
    // Calculate blocks needed, ensuring coverage
    dim3 numBlocks((N + threadsPerBlock.x - 1) / threadsPerBlock.x,
                   (N + threadsPerBlock.y - 1) / threadsPerBlock.y);

    matmul_mod<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C);

    // Check for kernel launch errors immediately
    CUDA_CHECK(cudaGetLastError());
    // Synchronize device to ensure computation is complete and check errors
    CUDA_CHECK(cudaDeviceSynchronize());
}

// --- GPU Matrix Exponentiation (Corrected Initialization) ---
// Computes (h_matrix ^ exp) mod MOD and stores result back in h_matrix
void matrix_expo_gpu(int64_t* h_matrix, int64_t exp) {
    if (exp == 0) {
        // If exp is 0, result is Identity matrix
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                h_matrix[i * N + j] = (i == j) ? 1 : 0;
            }
        }
        return;
    }
    if (exp == 1) {
        // If exp is 1, result is the matrix itself (modulo MOD)
        // Ensure initial matrix is mod MOD if necessary (depends on how it was created)
         for(size_t i = 0; i < (size_t)N * N; ++i) {
             h_matrix[i] = (h_matrix[i] % MOD + MOD) % MOD;
         }
        return;
    }


    int64_t *d_matrix = nullptr, *d_temp = nullptr, *d_result = nullptr, *d_identity = nullptr;
    size_t matrix_size_bytes = sizeof(int64_t) * N * N;

    try {
        // 1. Prepare Identity Matrix on Device
        std::vector<int64_t> h_identity(N * N, 0);
        for (int i = 0; i < N; ++i) {
            h_identity[i * N + i] = 1;
        }
        CUDA_CHECK(cudaMalloc(&d_identity, matrix_size_bytes));
        CUDA_CHECK(cudaMemcpy(d_identity, h_identity.data(), matrix_size_bytes, cudaMemcpyHostToDevice));
        // Host vector h_identity goes out of scope or clear it if needed std::vector<int64_t>().swap(h_identity);

        // 2. Allocate device memory for matrices
        CUDA_CHECK(cudaMalloc(&d_matrix, matrix_size_bytes));
        CUDA_CHECK(cudaMalloc(&d_temp, matrix_size_bytes));
        CUDA_CHECK(cudaMalloc(&d_result, matrix_size_bytes));

        // 3. Copy input matrix (base) to d_matrix
        CUDA_CHECK(cudaMemcpy(d_matrix, h_matrix, matrix_size_bytes, cudaMemcpyHostToDevice));
        // Ensure base matrix elements are mod MOD
        // This could be a kernel or done during copy, for simplicity we assume gpu_matrix_multiply handles it

        // 4. Initialize result matrix (d_result) to Identity
        CUDA_CHECK(cudaMemcpy(d_result, d_identity, matrix_size_bytes, cudaMemcpyDeviceToDevice));

        // 5. Perform exponentiation by squaring
        while (exp > 0) {
             std::cout << "Exponent remaining: " << exp << std::endl; // Progress indicator
            if (exp % 2 == 1) {
                // result = result * matrix_power (d_result = d_result * d_matrix)
                gpu_matrix_multiply(d_result, d_matrix, d_temp);
                std::swap(d_result, d_temp); // d_result now holds the product
            }
            // matrix_power = matrix_power * matrix_power (d_matrix = d_matrix * d_matrix)
            gpu_matrix_multiply(d_matrix, d_matrix, d_temp);
            std::swap(d_matrix, d_temp); // d_matrix now holds the square
            exp /= 2;
        }

        // 6. Copy final result back from d_result to host h_matrix
        CUDA_CHECK(cudaMemcpy(h_matrix, d_result, matrix_size_bytes, cudaMemcpyDeviceToHost));

    } catch (const std::exception& e) {
        std::cerr << "An error occurred: " << e.what() << std::endl;
        // Cleanup allocated memory even if error occurred
        if (d_matrix) cudaFree(d_matrix);
        if (d_temp) cudaFree(d_temp);
        if (d_result) cudaFree(d_result);
        if (d_identity) cudaFree(d_identity);
        throw; // Re-throw exception
    }

    // 7. Free all allocated device memory
    CUDA_CHECK(cudaFree(d_matrix));
    CUDA_CHECK(cudaFree(d_temp));
    CUDA_CHECK(cudaFree(d_result));
    CUDA_CHECK(cudaFree(d_identity));
}


int main() {
    // Use std::vector for easier host matrix management
    std::vector<int64_t> h_matrix(N * N, 0);

    // --- Initialize the CORRECT Transition Matrix T ---
    // T[0][1998] = 1, T[0][1999] = 1
    h_matrix[0 * N + 1998] = 1;
    h_matrix[0 * N + 1999] = 1;
    // T[i][i-1] = 1 for i = 1 to N-1
    for (int i = 1; i < N; ++i) {
        h_matrix[i * N + (i - 1)] = 1;
    }

    // --- Set the CORRECT Exponent ---
    // We need T^(k - (N-1)) = T^(k - 1999)
    int64_t exponent = K - (N - 1); // k - 1999
     std::cout << "Target Exponent: " << exponent << std::endl;


    // --- Perform Matrix Exponentiation ---
    try {
        matrix_expo_gpu(h_matrix.data(), exponent); // Pass pointer to vector data

        // --- Calculate the final answer g_k ---
        // g_k = sum of the first row of the resulting matrix M = T^p
        int64_t ans = 0;
        for (int i = 0; i < N; ++i) {
            ans = (ans + h_matrix[0 * N + i]) % MOD;
        }
        // Ensure final answer is positive
        ans = (ans + MOD) % MOD;

        std::cout << "Calculated g_k mod M = " << ans << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Matrix exponentiation failed." << std::endl;
        return 1; // Indicate failure
    }

    return 0; // Indicate success
}