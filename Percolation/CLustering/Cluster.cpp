#include "Cluster.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <ctime>
#include "Utils.h"

int Cluster::labels = 0;

Cluster::Cluster(vector<vector<int>>& inputGrid) : grid(inputGrid) {}

int Cluster::H_find(int x) {
    if (parent.find(x) == parent.end()) return x;
    if (parent[x] == x) return x;
    return parent[x] = H_find(parent[x]);
}

void Cluster::union_sets(int x, int y) {
    int rootX = H_find(x);
    int rootY = H_find(y);
    if (rootX != rootY) {
        parent[rootX] = rootY;
        clusterSizes[rootY] += clusterSizes[rootX];
        clusterSizes.erase(rootX);
    }
}
void Cluster::grid_normaliser() {
    for (size_t i = 0; i < grid.size(); i++) {
        for (size_t j = 0; j < grid[i].size(); j++) {
            if (grid[i][j] == 0) continue;
            grid[i][j] = H_find(grid[i][j]);
        }

    }
}

void Cluster::assign_labels() {
    for (size_t i = 0; i < grid.size(); i++) {
        for (size_t j = 0; j < grid[i].size(); j++) {
            if (grid[i][j] == 0) continue;
            
            int left = (j > 0 && grid[i][j-1] != 0) ? H_find(grid[i][j-1]) : 0;
            int top = (i > 0 && grid[i-1][j] != 0) ? H_find(grid[i-1][j]) : 0;
            
            if (left == 0 && top == 0) {
                grid[i][j] = ++labels;
                parent[labels] = labels;
                clusterSizes[labels] = 1;
            } else if (left != 0 && top != 0) {
                if (left < top) {
                    grid[i][j] =  left;
                    union_sets(top, left);
                    
                }
                else {
                    grid[i][j] = top;
                    union_sets(left, top);
                    
                }
            }
            else {
                grid[i][j] = max(left, top);
                clusterSizes[grid[i][j]]++;
            }
        }
    } 
    grid_normaliser();
}

void Cluster::print_cluster_data() {
    cout << "Number of clusters: " << clusterSizes.size() << endl;
    for (const auto& [label, size] : clusterSizes) {
        cout << "Cluster " << label << ": Size = " << size << endl;
    }
}

void Cluster::data_save(int k) {
    std::ofstream file("data_" + std::to_string(k) + ".txt");
    file << "Number of clusters: " << clusterSizes.size() << endl;
    for (const auto& [label, size] : clusterSizes) {
        file << "Cluster " << label << ": Size = " << size << endl;
    }
    file.close();
    

}

int Cluster::vector_comparator(vector<int>& vector1, vector<int>& vector2) {
    unordered_set<int> set1(vector1.begin(), vector1.end());
    set1.erase(0); // Remove zero values
    for (size_t j = 0; j < vector2.size(); j++) {
        if (vector2[j] != 0 && set1.find(vector2[j]) != set1.end()) {
            cout << "Match Found: vector2[" << j << "] with value " << vector2[j] << endl;
            return 1;
        }
    }
    return 0;
}

bool Cluster::percolates() {
    return vector_comparator(grid[0], grid[grid.size() - 1]);
}

void Cluster::get_grid(int k) {
    std::cout << "Printing grid" << std::endl;
    std::ofstream grid_file("grid" + std::to_string(k) + ".txt");
    grid_file << grid;
    grid_file.close();
    
}