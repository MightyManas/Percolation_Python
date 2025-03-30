#ifndef CLUSTER_H
#define CLUSTER_H

#include <cmath>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
using namespace std;

class Cluster {


    private : // helper functions
    // private member variables

    static int labels;
    vector<vector<int>> grid;
    unordered_map<int, int> parent;
    unordered_map<int, int> clusterSizes;

    // private member functions
    int H_find(int x);
    void union_sets(int x, int y);
    void assign_labels(); // assign labels to the clusters in the grid
    void grid_normaliser(); // normalise the grid to have the same labels for the same clusters
    int vector_comparator(vector<int>& vector1, vector<int>& vector2); // compare two vectors to check if they hav0e the same cluster label
    void get_grid(int k); // save the grid to a file


    public: // these are under development functions


    Cluster(vector<vector<int>>& inputGrid);
    double fractal_dimension(); // calculate the fractal dimension of the cluster
   
    
    void radial_distribution(int k); // radius of curvature of the clusters
    void directed_percolates(int percolating_index); // check if the grid percolates for directed percolation
    
    public : // these are the function to be used in main.cpp
    
    static Cluster init_clustering(int k1, int k2, double p); // function to initialise the grid with random values and assign labels to the clusters
    void calculate_correlation(double p); // to plot the correlation as function of r, dist between the two points
    void data_save(int k); // save the grid and cluster size distribution to two seperate txt files
    bool percolates(); // check if the grid percolates for open boundary conditions

};

#endif
