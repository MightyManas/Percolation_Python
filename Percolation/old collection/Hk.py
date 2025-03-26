#import numpy as np
import numpy as np
from numba import njit  # (Note: not used in this snippet, but kept for consistency)
import time 


# Dictionary to store cluster instances (if needed)
grid_dict = {}

class cluster:
    labels = 0  # Class-level counter for new labels

    def __init__(self, grid):
        self.grid = grid
        self.size = grid.shape[0]   
        self.label = 0  # Default label
        self.parrent = {}  # Union-Find parent dictionary

    def find(self, x):
        """Find the root representative of a cluster using path compression."""
        # If x is not in the dictionary, return x (should not happen for assigned labels)
        if x not in self.parrent:
            return x
        if self.parrent[x] == x:
            return x
        else:
            # Path compression: update parent to the root representative
            self.parrent[x] = self.find(self.parrent[x])
            return self.parrent[x]
        
    def union(self, x, y):
        """Merge two clusters by linking their roots."""
        parent_x = self.find(x)
        parent_y = self.find(y)
        self.parrent[parent_x] = parent_y  # Merge: make parent's parent_y

    def assign_label(self):
        """Label clusters in the grid using a union-find approach"""
        for i in range(self.size):
            for j in range(self.size):
                # Skip if the cell is not occupied
                if self.grid[i, j] == 0:
                    continue
                else:
                    # Get left neighbor value if available; otherwise 0.
                    left_val = self.grid[i, j-1] if j > 0 else 0
                    # Only call find if left_val is non-zero
                    left = self.find(left_val) if (j > 0 and left_val != 0) else 0
                    
                    # Get top neighbor value if available; otherwise 0.
                    top_val = self.grid[i-1, j] if i > 0 else 0
                    # Only call find if top_val is non-zero
                    top = self.find(top_val) if (i > 0 and top_val != 0) else 0

                    if left == 0 and top == 0:  # New cluster
                        self.label = cluster.labels + 1
                        self.grid[i, j] = self.label
                        self.parrent[self.label] = self.label
                        cluster.labels += 1
                    elif left != 0 and top != 0:  # Merge clusters
                        # Choose the smaller label as the representative
                        if top > left:
                            self.grid[i, j] = left
                            self.label = left
                            self.union(top, left)
                            self.parrent[self.label] = left
                        else:  # top <= left
                            self.grid[i, j] = top
                            self.label = top
                            self.union(top, left)
                            self.parrent[self.label] = top
                    else:  # One neighbor is 0, so take the non-zero neighbor
                        val = max(left, top)
                        self.grid[i, j] = val
                        self.label = val
                        self.parrent[self.label] = val

# Grid size and probability
k = 10000
p = 0.6

# Generate grid with percolation probability: 
# Here, 1 indicates an occupied cell, 0 indicates an empty cell.
sheet = (np.random.rand(k, k) < p).astype(int)

time1 = time.time()
hok = cluster(sheet)
hok.assign_label()
print(hok.grid)
time2 = time.time()
print("Time taken: ", time2 - time1)