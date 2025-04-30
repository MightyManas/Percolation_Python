#include "Cluster.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <ctime>
#include "Utils.h"
#include <queue>

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
    unordered_map<int, int>::iterator it;
    vector<int> keys;

    for (it = clusterSizes.begin(); it != clusterSizes.end(); ++it) {
    keys.push_back(it->first);
    }
    sort(keys.begin(), keys.end());
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
                clusterSizes[grid[i][j]]++;
            }
            else {
                grid[i][j] = max(left, top);
                clusterSizes[grid[i][j]]++;
            }
        }
    } 
}



void Cluster::data_save(int k) {
    std::ofstream file("data/data_" + std::to_string(k) + ".txt");
    file << "Number of clusters: " << clusterSizes.size() << endl;
    for (const auto& [label, size] : clusterSizes) {
        file << "Cluster " << label << ": Size = " << size << endl;
    }
    file.close();
    //get_grid(k); // save the grid to a file

}





int Cluster::vector_comparator(vector<int>& vector1, vector<int>& vector2) {
    unordered_set<int> set1(vector1.begin(), vector1.end());
    set1.erase(0); // Remove zero values
    for (size_t j = 0; j < vector2.size(); j++) {
        if (vector2[j] != 0 && set1.find(vector2[j]) != set1.end()) {
            cout << "Match Found: vector2[" << j << "] with value " << vector2[j] << endl;
            return vector2[j]; // Return the matching value
        }
    }
    return 0;
}

int Cluster::percolates() {
    return vector_comparator(grid[0], grid[grid.size() - 1]);
}

void Cluster::get_grid(int k) {
    std::cout << "Printing grid" << std::endl;
    std::ofstream grid_file("data/grid" + std::to_string(k) + ".txt");
    grid_file << grid;
    grid_file.close();
    
}



void Cluster::calculate_correlation(double p) {
    std::string file_correlation = "data/correlation_length_" + std::to_string(p) + ".txt";
    std::ofstream correlation_file(file_correlation);

    std::string file_diameter = "data/diameter_" + std::to_string(p) + ".txt";
    std::ofstream diameter(file_diameter);
    double delta_r = 0.4; 
    double likelihood = 0;
    int likelihood_count = 0;
    int max_diameter = 1;
    unordered_map<int, int> cluster_diameter_map  = clusterSizes; 
    std::for_each(cluster_diameter_map.begin(),cluster_diameter_map.end(), [](auto& pair) { 
        pair.second = 0;
    });  

    int max_rad = static_cast<int>(std::sqrt(grid.size()*grid.size() +  grid[0].size()* grid[0].size()));

    for (int rad = 1; rad < max_rad; rad++) { // loop through radius
        int count = 0;
        int count_all = 0;

        for (size_t i = 0; i < grid.size(); i++) { // loop through rows
            for (size_t j = 0; j < grid[i].size(); j++) { // loop through columns
                if (grid[i][j] != 0) {
                    for (int di = -rad; di <= rad; di++) { //loop for x coordinate in the disk
                        for (int dj = -rad; dj <= rad; dj++) { //loop for y coordinate in the disk
                            double dist = std::sqrt(di * di + dj * dj);
                            if (dist <= rad + delta_r && dist > rad - delta_r) {
                                count_all++;
                                int x = static_cast<int>(i) + di;
                                int y = static_cast<int>(j) + dj;

                                if (x >= 0 && x < static_cast<int>(grid.size()) && 
                                    y >= 0 && y < static_cast<int>(grid[x].size())) {
                                    if (grid[x][y] == grid[i][j]) {
                                        count++;
                                    }
                                }
                            }

                        }
                    }
                }
                
                if (count_all != 0) {
                    likelihood += static_cast<double>(count) / count_all;
                    likelihood_count++;
                }

                
                if (count != 0) {
                    max_diameter = rad;
                    cluster_diameter_map.at(grid[i][j]) =  std::max(max_diameter, cluster_diameter_map[grid[i][j]]);
                }
                count = 0;
                count_all = 0;
            }
        }

        if (likelihood_count != 0) {
            correlation_file << rad << " " << likelihood / likelihood_count << std::endl;
        }
    }
    for (const auto& [label, dia] : cluster_diameter_map) {
        diameter << label << " " << dia << std::endl;
    }
    
    correlation_file.close();
    diameter.close();
} 


Cluster Cluster::init_clustering(int k1, int k2, double p) {
    // This function initializes the clustering process.
    vector<vector<int>> rectangular_lattice = generate_rectangular_lattice(k1, k2, p);
    clock_t start_rect = clock();
    
    Cluster rect_cluster(rectangular_lattice);
    rect_cluster.assign_labels();
    rect_cluster.grid_normaliser();
    clock_t end_rect = clock();
    
    std::cout << "Rectangular lattice time taken: " << (double)(end_rect - start_rect) / CLOCKS_PER_SEC << " seconds" << std::endl;

    return rect_cluster;
}


double Cluster::fractal_dimension() {
    // This function calculates the fractal dimension of the cluster.
    double fractal_dim = 0.0;
    // Implement the calculation here
    return fractal_dim;
}


std::vector<std::pair<int, int>> Cluster::connected_children(int x, int y) {
    std::vector<std::pair<int, int>> result;
    if (grid[x][y] == 0) return result;

    int target_label = grid[x][y];
    std::vector<std::vector<bool>> visited(grid.size(), std::vector<bool>(grid[0].size(), false));
    std::queue<std::pair<int, int>> q;

    q.emplace(x, y);
    visited[x][y] = true;

    while (!q.empty()) {
        auto [cx, cy] = q.front();
        q.pop();

        // Check if this node is in the row below the original node
        if (cx == x + 1) {
            result.emplace_back(cx, cy);
            // Do NOT continue exploring down from here — this is a "child"
            continue;
        }

        // Explore 4-neighbor connectivity (you can generalize)
        const std::vector<std::pair<int, int>> directions = {
            {1, 0}, {-1, 0}, {0, 1}, {0, -1}
        };

        for (const auto& [dx, dy] : directions) {
            int nx = cx + dx, ny = cy + dy;
            if (nx >= 0 && nx < grid.size() && ny >= 0 && ny < grid[0].size()) {
                if (!visited[nx][ny] && grid[nx][ny] == target_label) {
                    visited[nx][ny] = true;
                    q.emplace(nx, ny);
                }
            }
        }
    }

    return result;
}




int Cluster::directed_percolates(int percolating_index) {
    // This function checks if the grid percolates for directed percolation.

    std::vector<std::pair<int,int>> parent_nodes ;
    std::vector<std::pair<int,int>> direct_children ;
    direct_children.push_back(std::make_pair(1,1));
    size_t i = 0;
    std::cout << "the directed apple is red" << std::endl;  
    while(i < grid.size() && direct_children.size() != 0) {
        std::cout << "the while apple has begun" << std::endl;
        for (size_t j = 0; j < grid[i].size(); j++  ) {
            //std::cout << "the for apple has begun" << std::endl;
            if (grid[i][j] == 0) continue;
            if (grid[i][j] == percolating_index) {
                parent_nodes.push_back(std::make_pair(i,j));
            } 
        }
        for (size_t k = 0; k < parent_nodes.size(); k++) {
            //std::cout << "the parent apple is eating up" << std::endl;
            int x = parent_nodes[k].first;
            int y = parent_nodes[k].second;
            if (x > 0 && grid[x-1][y-1] == percolating_index) {
                direct_children.clear();
                direct_children.push_back(std::make_pair(x-1,y-1));
                std::vector<std::pair<int, int>> children = connected_children(x, y);
                direct_children.insert(direct_children.end(), children.begin(), children.end());
            }
          
    }
        parent_nodes.clear();
        parent_nodes = direct_children;
    
        i++;
    }
    if (direct_children.size() != 0) {
        std::cout << "The grid percolates in the direction of the children" << std::endl;
        return 1; // return 1 if the grid percolates in the direction of the children
    } else {
        std::cout << "nope" << std::endl;
        return 0; // return 0 if the grid does not percolate in the direction of the children
    }

    
}
