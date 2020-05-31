#include "common.h"
#include "graph_reader/graph.h"
#include <stdio.h>
#include <stdlib.h>
#include <cusparse_v2.h>
#include <cuda.h>
#include <iostream>
#include "cublas_v2.h"

/*
 * Generate random dense matrix A in column-major order, while rounding some
 * elements down to zero to ensure it is sparse.
 */
int generate_random_dense_matrix(int M, int N, float **outA)
{
    int i, j;
    double rMax = (double)RAND_MAX;
    float *A = (float *)malloc(sizeof(float) * M * N);
    int totalNnz = 0;

    for (j = 0; j < N; j++)
    {
        for (i = 0; i < M; i++)
        {
            int r = rand();
            float *curr = A + (j * M + i);

            if (r % 3 > 0)
            {
                *curr = 0.0f;
            }
            else
            {
                double dr = (double)r;
                *curr = (dr / rMax) * 100.0;
            }

            if (*curr != 0.0f)
            {
                totalNnz++;
            }
        }
    }
    
    // std::cout << "sparsity: " << (totalNnz * 1.0) / (M * N) << std::endl;
    *outA = A;
    return totalNnz;
}


__global__ void Relu(float *matrix, int noOfElements){
    
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if(i < noOfElements)
        if (matrix[i] > 0)
            matrix[i] = matrix[i];
        else
            matrix[i] = 0;
}


int main(int argc, char **argv)
{
    float *X;
    float *dC, *dC1;
    float *W_1, *W_2;
    float *dh, *dh1;

    float *dCsrValA;
    int *dCsrRowPtrA;
    int *dCsrColIndA;
    int totalANnz;

    float *CsrValA;
    int *CsrRowPtrA;
    int *CsrColIndA;
    
    float alpha = 1.0f;
    float beta_1 = 1.0f;
    float beta_2 = 1.0f;
    
    cusparseHandle_t handle = 0;
    cublasHandle_t handle_blas = 0;
    cusparseMatDescr_t Adescr = 0;
    
    // std::cout<<"Input: ./exe beg csr weight indim hiddendim outdim\n";
	if(argc != 8){
        std::cout<<"Wrong input\n"; 
        return -1;
    }
	
	const char *beg_file=argv[1];
	const char *csr_file=argv[2];
    const char *weight_file=argv[3];
    
    int N;
    int D = atoi(argv[4]);
    int K = atoi(argv[5]);
    int F = atoi(argv[6]);

    graph<long, long, int, int, int, float>
	*ginst = new graph<long, long, int, int, int, float>(beg_file, csr_file, weight_file);
    
    CsrRowPtrA = ginst->beg_pos;
    CsrColIndA = ginst->csr;
    CsrValA = ginst->weight;

    totalANnz = ginst -> edge_count;
    printf("nonZeros: %d\n", totalANnz);

    N = ginst-> vert_count;

    // Generate input
    // srand(9384);
    // generate_random_dense_matrix(N, D, &B);
    // B = (float *)malloc(sizeof(float) * N * D);
    // C = (float *)malloc(sizeof(float) * N * D);
    // memset(B, 0x01, sizeof(float) * N * D);

    // Create the cuSPARSE handle
    CHECK_CUSPARSE(cusparseCreate(&handle));
    // Create the cuBLAS handle
    CHECK_CUBLAS(cublasCreate(&handle_blas));

    // Allocate device memory for vectors and the dense form of the matrix A
    CHECK(cudaMalloc((void **)&X, sizeof(float) * N * D));

    // aggregration step param
    CHECK(cudaMalloc((void **)&dC, sizeof(float) * N * K));
    CHECK(cudaMalloc((void **)&dC1, sizeof(float) * N * F));

    // hidden parameters == scaled bias matrix (1 x K --> N x K)
    CHECK(cudaMalloc((void **)&dh, sizeof(float) * N * K));
    CHECK(cudaMalloc((void **)&dh1, sizeof(float) * N * F));

    // combination step param
    CHECK(cudaMalloc((void **)&W_1, sizeof(float) * D * K));
    CHECK(cudaMalloc((void **)&W_2, sizeof(float) * K * F));

    // Allocate device memory to store the sparse CSR representation of A
    CHECK(cudaMalloc((void **)&dCsrValA, sizeof(float) * totalANnz));
    CHECK(cudaMalloc((void **)&dCsrRowPtrA, sizeof(int) * (N + 1)));
    CHECK(cudaMalloc((void **)&dCsrColIndA, sizeof(int) * totalANnz));

    CHECK(cudaMemcpy(dCsrValA, CsrValA, sizeof(float) * totalANnz, cudaMemcpyHostToDevice));
    CHECK(cudaMemcpy(dCsrRowPtrA, CsrRowPtrA, sizeof(int) * (N + 1), cudaMemcpyHostToDevice));
    CHECK(cudaMemcpy(dCsrColIndA, CsrColIndA, sizeof(int) * totalANnz, cudaMemcpyHostToDevice));

    // Construct a descriptor of the matrix A
    CHECK_CUSPARSE(cusparseCreateMatDescr(&Adescr));
    CHECK_CUSPARSE(cusparseSetMatType(Adescr, CUSPARSE_MATRIX_TYPE_GENERAL));
    CHECK_CUSPARSE(cusparseSetMatIndexBase(Adescr, CUSPARSE_INDEX_BASE_ZERO)); // CUSPARSE_INDEX_BASE_ZERO

    float total_agg = 0;
    float total_update = 0;
    float total_update1 = 0;

    float milliseconds = 0;
    int iteration = atoi(argv[7]);

    for (int i = 0; i < iteration; i++)
    {
        // -------------------------------------------
        // Layer - 1 ---------------------------------
        // -------------------------------------------
        printf("iteration: %d\n", i);
        cudaEvent_t start, stop;

        //////////////////////////////////////////////////
        CHECK(cudaEventCreate(&start));
        CHECK(cudaEventCreate(&stop));
        CHECK(cudaEventRecord(start));

        // Layer1 = Update step dgemm (N x D dot D x K --> N x K)
        cublasSgemm(handle_blas, CUBLAS_OP_N, CUBLAS_OP_N, N, K, D, &alpha, X, N, W_1, D, &beta_2, dC, N);
        
        CHECK(cudaEventRecord(stop));
        CHECK(cudaEventSynchronize(stop));
        
        milliseconds = 0;
        CHECK(cudaEventElapsedTime(&milliseconds, start, stop));
        total_update += milliseconds;

        //////////////////////////////////////////////////
        CHECK(cudaEventCreate(&start));
        CHECK(cudaEventCreate(&stop));
        CHECK(cudaEventRecord(start));
        
        // Aggregration step spMM (dh = A.dC == N x N dot N x K --> N x K)
        // formula: alpha * A.dot(dC) + beta * dh  
        cusparseScsrmm(handle, CUSPARSE_OPERATION_NON_TRANSPOSE, N, K, N, totalANnz, &alpha, Adescr, dCsrValA, dCsrRowPtrA, dCsrColIndA, dC, N, &beta_1, dh, N);

        CHECK(cudaEventRecord(stop));
        CHECK(cudaEventSynchronize(stop));
        
        milliseconds = 0;
        CHECK(cudaEventElapsedTime(&milliseconds, start, stop));
        total_agg += milliseconds;

        //////////////////////////////////////////////////
        // dh = ReLU(dh)
        int noTrd = 1024;
        int noBlocks=(N * K)/1024 + 1;
        CHECK(cudaEventCreate(&start));
        CHECK(cudaEventCreate(&stop));
        CHECK(cudaEventRecord(start));

        Relu<<<noBlocks, noTrd >>>(dh, N * K);
        
        CHECK(cudaEventRecord(stop));
        CHECK(cudaEventSynchronize(stop));
        
        milliseconds = 0;
        CHECK(cudaEventElapsedTime(&milliseconds, start, stop));
        total_update1 += milliseconds;

        // -------------------------------------------
        // Layer - 2 ---------------------------------
        // -------------------------------------------
        CHECK(cudaEventCreate(&start));
        CHECK(cudaEventCreate(&stop));
        CHECK(cudaEventRecord(start));

        // Layer2 = Update step dgemm  
        // ((dh) N x K dot (W2) K x F --> (dC1) N x F)
        cublasSgemm(handle_blas, CUBLAS_OP_N, CUBLAS_OP_N, N, F, K, &alpha, dh, N, W_2, K, &beta_2, dC1, N);

        CHECK(cudaEventRecord(stop));
        CHECK(cudaEventSynchronize(stop));
        
        milliseconds = 0;
        CHECK(cudaEventElapsedTime(&milliseconds, start, stop));
        total_update += milliseconds;

        /////////////////////////////////////////////////
        CHECK(cudaEventCreate(&start));
        CHECK(cudaEventCreate(&stop));
        CHECK(cudaEventRecord(start));
        
        // Aggregration step spMM (A (N x N) dot dC (N x F) --> dh1 (N x F))
        // Formula: alpha * A.dot(dC1) + beta1 * dh1  
        cusparseScsrmm(handle, CUSPARSE_OPERATION_NON_TRANSPOSE, N, F, N, totalANnz, &alpha, Adescr, dCsrValA, dCsrRowPtrA, dCsrColIndA, dC1, N, &beta_1, dh1, N);

        CHECK(cudaEventRecord(stop));
        CHECK(cudaEventSynchronize(stop));

        milliseconds = 0;
        CHECK(cudaEventElapsedTime(&milliseconds, start, stop));
        total_agg += milliseconds;
    }

    // printf("Sparsity: %f %%\n", totalANnz * 1.0 / ((long)(N) * (long)(N)) * 100);
    float total = total_agg + total_update + total_update1;
    printf("Dim Reduction: %.3f %%\n", total_update/total * 100);
    printf("Aggre: %.3f %%\n", total_agg/total * 100);
    printf("Node Update: %.3f %%\n", total_update1/total * 100);
    printf("Time: %.3f ms\n", total);
    
    float total_ops = 2 * ((float)N * (float)D * (float)K + (float)N * (float)K * (float)F) + (float)totalANnz * (K + F);
    printf("Throughput: %.3f GFLOPS\n",  total_ops/(milliseconds / 1000.)/1e9);
    
    printf("\n\n\n\n");

    CHECK(cudaFree(X));
    CHECK(cudaFree(dC));
    CHECK(cudaFree(dCsrValA));
    CHECK(cudaFree(dCsrRowPtrA));
    CHECK(cudaFree(dCsrColIndA));

    CHECK_CUSPARSE(cusparseDestroyMatDescr(Adescr));
    CHECK_CUSPARSE(cusparseDestroy(handle));
    CHECK_CUBLAS(cublasDestroy(handle_blas));
    return 0;
}
