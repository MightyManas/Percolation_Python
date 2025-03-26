#ifndef UTILS_H
#define UTILS_H

#include <vector>
#include <iostream>
#include <ostream>
using namespace std;

vector<vector<int>> generate_rectangular_lattice(int rows, int cols, double p);
ostream& operator<<(ostream& os, const vector<vector<int>>& vec);
#endif
