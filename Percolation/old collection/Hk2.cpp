#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <sstream>
#include <unordered_set>

using namespace std;

class Cluster {
public:
    static int labels;
    vector<vector<int>> grid;
    unordered_map<int, int> parent;
    unordered_map<int, int> clusterSizes;
    vector<int> Row1;
    vector<int> Row2;   

    Cluster(vector<vector<int>>& inputGrid) : grid(inputGrid) {}

    int find(int x) {
        if (parent.find(x) == parent.end()) return x;
        if (parent[x] == x) return x;
        return parent[x] = find(parent[x]);
    }

    void union_sets(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            parent[rootX] = rootY;
            clusterSizes[rootY] += clusterSizes[rootX];
            clusterSizes.erase(rootX);
        }
    }

    void assign_labels() {
        for (int i = 0; i < grid.size(); i++) {
            for (int j = 0; j < grid[i].size(); j++) {
                if (grid[i][j] == 0) continue;
                
                int left = (j > 0 && grid[i][j-1] != 0) ? find(grid[i][j-1]) : 0;
                int top = (i > 0 && grid[i-1][j] != 0) ? find(grid[i-1][j]) : 0;
                
                if (left == 0 && top == 0) {
                    grid[i][j] = ++labels;
                    parent[labels] = labels;
                    clusterSizes[labels] = 1;
                } else if (left != 0 && top != 0) {
                    if (left < top) {
                        grid[i][j] = left;
                        union_sets(top, left);
                    } else {
                        grid[i][j] = top;
                        union_sets(left, top);
                    }
                } else {
                    grid[i][j] = max(left, top);
                    clusterSizes[grid[i][j]]++;
                }
            }
        }
    }

    void print_cluster_data() {
        cout << "Number of clusters: " << clusterSizes.size() << endl;
        cout << "Cluster sizes: ";
        for (const auto& [label, size] : clusterSizes) {
            cout << size << " ";
        }
        cout << endl;
    }

    void data_save(int k) {
        std::string filename = "data_" + std::to_string(k) + ".txt";
        ofstream file(filename);
        file << "Number of clusters: " << clusterSizes.size() << endl;
        file << "Cluster sizes: ";
        for (const auto& [label, size] : clusterSizes) {
            file << size << " ";
        }
        file << endl;
        file.close();
    }


    int vector_comparator(vector<int>& vector1, vector<int>& vector2) {
        
    
    // Use a set to store non-zero values for faster lookup
    unordered_set<int> set1;
    for (int val : vector1) {
        if (val != 0) {
            set1.insert(val);
        }
    }

    // Compare and print matches, avoiding zeros
    for (size_t j = 0; j < vector2.size(); j++) {
        if (vector2[j] != 0 && set1.find(vector2[j]) != set1.end()) {
            cout << "Match Found: vector2[" << j << "] with value " << vector2[j] << endl;
        }
    }

    return 0;
    }

    bool percolates() {
        

        vector<int> grid_0 = grid[0];
        vector<int> grid_n = grid[grid.size() - 1];
        return vector_comparator(grid_0, grid_n);

    }



};

int Cluster::labels = 0;

vector<vector<int>> generate_rectangular_lattice(int rows, int cols, double p) {
    vector<vector<int>> grid(rows, vector<int>(cols, 0));
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            grid[i][j] = (rand() / (double)RAND_MAX < p) ? 1 : 0;
        }
    }
    return grid;

}

ostream& operator<<(ostream& os, const vector<vector<int>>& vec) {
    for (const auto& row : vec) {
        for (int val : row) {
            os << val << " ";
        }
        os << "\n";
    }
    return os;
}





int main() {
    srand(time(0));
    double p = 0.6;
    int k; //dim of the lattice 
    for (k = 5000; k < 5002; k += 50)
    {   
        vector<vector<int>> rectangular_lattice = generate_rectangular_lattice(k, k, p);
        clock_t start_rect = clock();
        Cluster rect_cluster(rectangular_lattice);
        rect_cluster.assign_labels();
        clock_t end_rect = clock();
        cout << "Rectangular lattice time taken: " << (double)(end_rect - start_rect) / CLOCKS_PER_SEC << " seconds" << endl;
        //rect_cluster.print_cluster_data();
        rect_cluster.data_save(k);
        //std::cout << rect_cluster.grid << std::endl;

        rect_cluster.percolates();
    };
    
    return 0;
}
