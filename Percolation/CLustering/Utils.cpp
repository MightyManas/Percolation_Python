#include "Utils.h"
#include <cstdlib>
#include <ostream>
#include <iostream>

vector<vector<int>> generate_rectangular_lattice(int rows, int cols, double p) {
    vector<vector<int>> grid(rows, vector<int>(cols, 0));
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            grid[i][j] = (rand() / (double)RAND_MAX < p) ? 1 : 0;
        }
    }
    cout << grid;
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
