#ifndef CLUSTER_H
#define CLUSTER_H

#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
using namespace std;

class Cluster {
public:
    static int labels;
    vector<vector<int>> grid;
    unordered_map<int, int> parent;
    unordered_map<int, int> clusterSizes;

    Cluster(vector<vector<int>>& inputGrid);
    int H_find(int x);
    void union_sets(int x, int y);
    void assign_labels();
    void print_cluster_data();
    void data_save(int k);
    int vector_comparator(vector<int>& vector1, vector<int>& vector2);
    bool percolates();
    void get_grid(int k);
    void grid_normaliser();
};

#endif
