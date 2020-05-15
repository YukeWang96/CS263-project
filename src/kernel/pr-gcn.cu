#include "cublas_v2.h"
#include "./pr.hpp"

// #define RUN_TOY

#ifdef RUN_TOY
	#define USE_RAND
	#define PROF_DETAIL
#endif
// #define DEBUG

int main(int argc, char** argv)
{
	Timer t, t1;
	float duration;

	ArgumentParser arguments(argc, argv, false, true, true);
	if (!arguments.hasInput || !arguments.hasEmbeding){
		std::cout << "Usage! ./exe graph_adj graph_embedding" << std::endl;
	}
	Graph graph(arguments.input, arguments.embedFilePath, false);
	
#ifdef PROF_DETAIL
	t.Start();
	graph.ReadGraph();
	duration = t.Finish();
	std::cout << "=> Read Graph (edge) takes: " << duration << "(ms)" << std::endl;
	t.Start();

	#ifdef load_ebd_from_file
		graph.ReadEmbedding();
	#else
	
	#endif
	duration = t.Finish();
	std::cout << "=> Read Graph (embeddinig) takes: " << duration << "(ms)" << std::endl;
#else
	graph.ReadGraph();
	#ifdef load_ebd_from_file
		graph.ReadEmbedding();
	#else
#endif 
#endif

	std::cout << "---------------" << std::endl;
#ifdef DEBUG
	//validate the embedding reading
	// for(int i = 0; i < 10; i++){
	// 	Embedding ebd = graph.pt_embeds[i];
	// 	std::cout << "pid[" << i  << "]= (";
	// 	// std::cout << "dim: " << ebd.embed.size() << std::endl;
	// 	for(int d  = 0; d < ebd.embed.size(); d++)
	// 		std::cout << ebd.embed[d] << " ";
	// 	std::cout << ")" <<std::endl;
	// }
#endif

#ifdef PROF_DETAIL
	t.Start();
	VirtualGraph vGraph(graph);
	vGraph.MakeUGraph();
	duration = t.Finish();
	std::cout << "=> Make Virtual Graph takes: " << duration << "(ms)" << std::endl;
#else
	VirtualGraph vGraph(graph);
	vGraph.MakeUGraph();
	// return 0;
#endif
	uint num_nodes = graph.num_nodes;
	uint num_edges = graph.num_edges;

#ifdef load_ebd_from_file
	uint ebd_dim = graph.pt_embeds[0].embed.size();  // get the size of node embedding
#else
	uint ebd_dim = arguments.ebdSize;
#endif
	// printf("ebd_dim, %d\n", ebd_dim);

	uint hidden_dim = arguments.hidden;
	uint output_dim = arguments.no_Class;

	if(arguments.hasDeviceID)
		cudaSetDevice(arguments.deviceID);	

	cudaFree(0);

	float *embed1, *embed2;
	embed1  = new float[num_nodes * ebd_dim];
	embed2  = new float[num_nodes * ebd_dim];
	
	float *weight1, *weight2;
	weight1 = new float[ebd_dim * hidden_dim];
	weight2 = new float[hidden_dim * output_dim];

	// float *hidden, *output;
	// hidden = new float[num_nodes * hidden_dim];
	// output = new float[num_nodes * output_dim];


#ifdef load_ebd_from_file
#pragma omp parallel for
	for(int i = 0; i < num_nodes; i++)
	{
		Embedding curr_pt = graph.pt_embeds[i];
		for(int d  = 0; d < ebd_dim; d++){
			embed1[i * ebd_dim + d] = 0;
			embed2[i * ebd_dim + d] = curr_pt.embed[d];
		}
	}
#else

#ifdef USE_RAND
#pragma omp parallel for
	for(int i = 0; i < num_nodes; i++)
	{
		for(int d  = 0; d < ebd_dim; d++){
			embed1[i * ebd_dim + d] = 0.0f;
			embed2[i * ebd_dim + d] = 1.0f; //static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/dataRange));
		}
	}

#pragma omp parallel for
	for(int i = 0; i < ebd_dim; i++)
		for(int d  = 0; d < hidden_dim; d++)
			weight1[i * hidden_dim + d] = 1.0f; // static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/dataRange));

#pragma omp parallel for
	for(int i = 0; i < hidden_dim; i++)
		for(int d  = 0; d < output_dim; d++)
			weight2[i * output_dim + d] = 1.0f; //static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/dataRange));
#endif

#endif

	unsigned int *d_nodePointer;
	unsigned int *d_edgeList;
	PartPointer *d_partNodePointer; 
	float *d_embed1;
	float *d_embed1_test;

	float *d_embed2;
	float *d_hidden;
	float *d_embed3;
	float *d_output;
	float *d_weight1, *d_weight2;

	// layer-1 param
	gpuErrorcheck(cudaMalloc(&d_nodePointer, num_nodes * sizeof(unsigned int)));
	gpuErrorcheck(cudaMalloc(&d_edgeList, (num_edges + num_nodes) * sizeof(unsigned int)));
	gpuErrorcheck(cudaMalloc(&d_embed1, num_nodes * ebd_dim * sizeof(float)));
	gpuErrorcheck(cudaMemcpy(d_embed1, embed2, num_nodes * ebd_dim * sizeof(float), cudaMemcpyHostToDevice));
	gpuErrorcheck(cudaMalloc(&d_embed1_test, num_nodes * ebd_dim * sizeof(float)));

	gpuErrorcheck(cudaMalloc(&d_hidden, num_nodes * hidden_dim * sizeof(float)));
	gpuErrorcheck(cudaMalloc(&d_embed2, num_nodes * hidden_dim * sizeof(float)));
	gpuErrorcheck(cudaMalloc(&d_weight1, ebd_dim * hidden_dim * sizeof(float)));
	gpuErrorcheck(cudaMemcpy(d_weight1, weight1, ebd_dim * hidden_dim * sizeof(float), cudaMemcpyHostToDevice));

	// layer-2 param
	gpuErrorcheck(cudaMalloc(&d_embed3, num_nodes * output_dim * sizeof(float)));
	gpuErrorcheck(cudaMalloc(&d_output, num_nodes * output_dim * sizeof(float)));
	gpuErrorcheck(cudaMalloc(&d_weight2, hidden_dim * output_dim * sizeof(float)));

	gpuErrorcheck(cudaMemcpy(d_weight2, weight2, hidden_dim * output_dim * sizeof(float), cudaMemcpyHostToDevice));

	// graph and virtual graph
	gpuErrorcheck(cudaMalloc(&d_partNodePointer, vGraph.numParts * sizeof(PartPointer)));

	gpuErrorcheck(cudaMemcpy(d_nodePointer, vGraph.nodePointer, num_nodes * sizeof(unsigned int), cudaMemcpyHostToDevice));
	gpuErrorcheck(cudaMemcpy(d_edgeList, vGraph.edgeList, (num_edges + num_nodes) * sizeof(unsigned int), cudaMemcpyHostToDevice));
	gpuErrorcheck(cudaMemcpy(d_partNodePointer, vGraph.partNodePointer, vGraph.numParts * sizeof(PartPointer), cudaMemcpyHostToDevice));

	// for(int i = 0; i < vGraph.numParts; i++){
	// 	std::cout << "part: " << i << "local part: " << vGraph.partNodePointer[i].part \
	// 	<< " node: " << vGraph.partNodePointer[i].node << std::endl;
	// }

	divide_node_by_block(vGraph);

	t1.Start();
	cublasHandle_t handle_blas = 0;
	float alpha = 1.0f;
	float beta_1 = 1.0f;

	// std::cout << "vGraph.numParts: " << vGraph.numParts << std::endl;
	// for (unsigned int i = 0; i < vGraph.numParts; i++){
	// 	std::cout << "GID: " << i << " TNID: " << vGraph.partNodePointer[i].node << " LID: " << vGraph.partNodePointer[i].part << std::endl;
	// }

	// for (unsigned int i = 0; i < vGraph.numParts; i++){
	// 	std::cout << "GID: " << i << " TNID: " << vGraph.partNodePointer[i].node \
	// 			  << " LSAddr: " << vGraph.partNodePointer[i].node_shared_addr << std::endl;
		
	// 	if ((i + 1)%thread_per_block == 0)
	// 		std::cout << "============================" << std::endl;

	// layer-1
#ifdef PROF_DETAIL

#ifdef RUN_TOY
	kernel<<< (vGraph.numParts * MAX_WK)/thread_per_block + 1 , thread_per_block >>>(vGraph.numParts, 
																						d_nodePointer,
																						ebd_dim,
																						num_nodes,
																						d_partNodePointer,
																						d_edgeList,
																						d_embed1_test,
																						d_embed1
																						);

	gpuErrorcheck( cudaDeviceSynchronize() );
	gpuErrorcheck(cudaMemcpy(embed1, d_embed1_test, num_nodes * ebd_dim * sizeof(float), cudaMemcpyDeviceToHost));
	for(int i = 0; i < num_nodes; i++)
	{
		for(int d  = 0; d < ebd_dim; d++){
			printf("%.3f ", embed1[i * ebd_dim + d]);
			// embed2[i * ebd_dim + d] = 1; //static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/dataRange));
		}
		std::cout << std::endl;
	}		
#else
	t.Start();
	cublasSgemm(handle_blas, CUBLAS_OP_N, CUBLAS_OP_N, num_nodes, hidden_dim, ebd_dim, &alpha, d_embed1, num_nodes, d_weight1, ebd_dim, &beta_1, d_hidden, num_nodes);
	gpuErrorcheck( cudaDeviceSynchronize() );
	duration = t.Finish();
	std::cout << "=> Layer-1 Dimension Reduction: " << duration << "(ms)" << std::endl;
	t.Start();
	kernel<<< (vGraph.numParts * MAX_WK)/thread_per_block + 1 , thread_per_block >>>(vGraph.numParts, 
																			d_nodePointer,
																			hidden_dim,
																			num_nodes,
																			d_partNodePointer,
																			d_edgeList,
																			d_embed2,
																			d_hidden
																			);
	duration = t.Finish();
	std::cout << "=> Layer-1 Aggregration: " << duration << "(ms)" << std::endl;
#endif

#else
	cublasSgemm(handle_blas, CUBLAS_OP_N, CUBLAS_OP_N, num_nodes, hidden_dim, ebd_dim, &alpha, d_embed1, num_nodes, d_weight1, ebd_dim, &beta_1, d_hidden, num_nodes);

	kernel<<< (vGraph.numParts * MAX_WK)/thread_per_block + 1 , thread_per_block >>>(vGraph.numParts, 
																					d_nodePointer,
																					hidden_dim,
																					num_nodes,
																					d_partNodePointer,
																					d_edgeList,
																					d_embed2,
																					d_hidden
																					);
#endif

#ifndef RUN_TOY
	clearLabel<<< num_nodes * ebd_dim/thread_per_block + 1 , thread_per_block >>>( d_hidden,
																				   d_embed2,
																				   hidden_dim, 
																				   num_nodes
																					);
	Relu<<<num_nodes * hidden_dim/thread_per_block, thread_per_block >>>(d_hidden, num_nodes * hidden_dim);

	// layer-2
#ifdef PROF_DETAIL
	t.Start();
	cublasSgemm(handle_blas, CUBLAS_OP_N, CUBLAS_OP_N, num_nodes, output_dim, hidden_dim, &alpha, d_hidden, num_nodes, d_weight2, hidden_dim, &beta_1, d_embed3, num_nodes);
	duration = t.Finish();
	gpuErrorcheck( cudaDeviceSynchronize() );	
	std::cout << "=> Layer-2 Dimension Reduction: " << duration << "(ms)" << std::endl;
	t.Start();
	kernel<<< (vGraph.numParts * MAX_WK) /thread_per_block + 1 , thread_per_block >>>(vGraph.numParts, 
																			d_nodePointer, 
																			output_dim,
																			num_nodes,
																			d_partNodePointer,
																			d_edgeList,
																			d_output,
																			d_embed3);
	duration = t.Finish();
	gpuErrorcheck( cudaDeviceSynchronize() );	
	std::cout << "=> Layer-2 Aggregration: " << duration << "(ms)" << std::endl;
#else
	cublasSgemm(handle_blas, CUBLAS_OP_N, CUBLAS_OP_N, num_nodes, output_dim, hidden_dim, &alpha, d_hidden, num_nodes, d_weight2, hidden_dim, &beta_1, d_embed3, num_nodes);
	kernel<<< (vGraph.numParts * MAX_WK)/thread_per_block + 1 , thread_per_block >>>(vGraph.numParts, 
																			d_nodePointer, 
																			output_dim,
																			num_nodes,
																			d_partNodePointer,
																			d_edgeList,
																			d_output,
																			d_embed3);
#endif
	clearLabel<<< num_nodes * hidden_dim/thread_per_block + 1 , thread_per_block >>>(d_output,
																					d_embed3,
																					output_dim, 
																					num_nodes);
	gpuErrorcheck( cudaPeekAtLastError() );
	gpuErrorcheck( cudaDeviceSynchronize() );	
	cudaDeviceSynchronize();

	float runtime = t1.Finish();
	cout << "**GCN " << runtime << " (ms).\n\n\n";
#endif

	gpuErrorcheck(cudaFree(d_nodePointer));
	gpuErrorcheck(cudaFree(d_edgeList));
	gpuErrorcheck(cudaFree(d_partNodePointer));
}
