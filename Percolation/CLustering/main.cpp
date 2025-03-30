#include <iostream>
#include "Cluster.h"
#include "Utils.h"
#include <ctime>

std::vector<double>  prob_interation() {
    // This function generates a random number of iterations based on the given probabilities.
    double p ;
    std::vector<double> m;
    for (p = 0.05; p < 1; p += 0.05) {
        m.push_back(p);      
    }
    return m;
}



int main() {
    srand(time(0));
    
    int k1 = 1000;
    int k2 = 1000; 
    std::vector<double> m = prob_interation(); // generate the probabilities
    for (size_t i = 0; i < m.size(); i++) {
        Cluster rect_cluster = Cluster::init_clustering(k1, k2, m[i]);
        rect_cluster.data_save(k1);
        rect_cluster.calculate_correlation(m[i]); // calculate the correlation length for the given k1 and k2

    

    }
    return 0;
    
}
