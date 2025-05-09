#include <iostream>
#include "Cluster.h"
#include "Utils.h"
#include <ctime>
#include <fstream>

std::vector<double>  prob_interation() {
    // This function generates a random number of iterations based on the given probabilities.
    double p ;
    std::vector<double> m;
    for (p = 0.587; p < 0.603; p += 0.001) {
        m.push_back(p);      
    }
    return m;
}



int main() {
    // srand(time(0));
    
    int k1 = 10000;
    int k2 = 10009; 
    // int iteratrions = 100; // number of iterations
    std::vector<double> m = prob_interation(); // generate the probabilities
    //std::vector<std::vector<double>> percolates(m.size(), std::vector<double>(3, 0.0));
    //std::ofstream percolation_file("data/percolation.txt");

    // if (!percolation_file.is_open()) {
    //     std::cerr << "Failed to open file for writing!" << std::endl;
    //     return 1;
    // }
    std::cout << "Generating rectangular lattice..." << std::endl;

    for (size_t i = 0; i < m.size(); i++) {
        // for (int j = 0; j < iteratrions; j++) {
            Cluster rect_cluster = Cluster::init_clustering(k1, k2,m[i] );
            rect_cluster.data_save(i+11); // save the grid and cluster size distribution to two separate txt files
        //     int percolating_index = rect_cluster.percolates();
        //     std::cout << "Percolation index: " << percolating_index << std::endl;

        //     if (percolating_index != 0) {
        //         std::cout << "shinigami loves apples" << std::endl;
        //         percolates[i][1] += 1;
        //         //percolates[i][2] += rect_cluster.directed_percolates(percolating_index);
        //         std::cout << "light use deathnote" << std::endl;
        //     }
        //     rect_cluster.labels = 0; // reset the labels for the next iteration
        //  }
        // std::cout << "apples are red" << std::endl;
        // percolates[i][0] = m[i];
        // percolates[i][1] /= iteratrions;
        // //percolates[i][2] /= iteratrions;
        // std ::cout << "so many apples" << std::endl;
        // percolation_file << percolates[i][0] << " " << percolates[i][1] << " " << percolates[i][2] << std::endl;
        // std::cout << "why i am not getting apples" << std::endl;
     }

   

    //percolation_file.close();
    //std::cout << "Percolation data saved to data/percolation.txt" << std::endl;

    return 0;
    
}
