#include <iostream>
#include "Cluster.h"
#include "Utils.h"
#include <ctime>

int main() {
    srand(time(0));
    double p = 0.6;
    int k; 
    for (k = 10; k < 11; k += 50) {
        vector<vector<int>> rectangular_lattice = generate_rectangular_lattice(k, k, p);
        clock_t start_rect = clock();
        Cluster rect_cluster(rectangular_lattice);
        rect_cluster.assign_labels();
        clock_t end_rect = clock();
        
        cout << "Rectangular lattice time taken: " 
             << (double)(end_rect - start_rect) / CLOCKS_PER_SEC << " seconds" << endl;
        rect_cluster.data_save(k);
        rect_cluster.get_grid(k);
        clock_t start_rect_percolation = clock();
        if (rect_cluster.percolates()) {
            cout << "The system percolates!" << endl;
        } else {
            cout << "The system does not percolate." << endl;
        }
        clock_t end_rect_percolation = clock();
        cout << "Percolation check time taken: " 
             << (double)(end_rect_percolation - start_rect_percolation) / CLOCKS_PER_SEC << " seconds" << endl;
    }
    system("pause");
    return 0;
    
}
