import numpy as np

# Dictionary to store cluster instances
sheet_dict = {}

class Cluster:
    clusters = []  # Stores lists of labels representing each cluster
    label_map = {}  # Maps label to its cluster index

    def __init__(self, i, j):
        self.i = i
        self.j = j  
        self.label = f"A{i}{j}"  # Default label
        self.cluster_index = None  # Index in Cluster.clusters

        self.assign_label()
        
    def assign_label(self):
        """Assigns a label based on left and top neighbors, handling boundary cases."""
        left_label, left_index = self.get_left_label()
        top_label, top_index = self.get_top_label()
        
        if top_label:
            self.label = top_label
            self.cluster_index = top_index
            Cluster.clusters[top_index].append(self.label)

            if left_label and left_index != top_index:
                # Merge left cluster into the top cluster
                Cluster.clusters[top_index].extend(Cluster.clusters[left_index])
                Cluster.clusters[left_index] = []
                Cluster.label_map[left_label] = top_index
        
        elif left_label:
            self.label = left_label
            self.cluster_index = left_index
            Cluster.clusters[left_index].append(self.label)
        
        else:
            # Create a new cluster
            self.cluster_index = len(Cluster.clusters)
            Cluster.clusters.append([self.label])

        # Track label's cluster index
        Cluster.label_map[self.label] = self.cluster_index

    def get_left_label(self):
        """Returns the label and cluster index of the left neighbor if it exists in the cluster."""
        if self.j > 0 and (self.i, self.j - 1) in sheet_dict:
            left_cluster = sheet_dict[(self.i, self.j - 1)]
            return left_cluster.label, left_cluster.cluster_index
        return None, None

    def get_top_label(self):
        """Returns the label and cluster index of the top neighbor if it exists in the cluster."""
        if self.i > 0 and (self.i - 1, self.j) in sheet_dict:
            top_cluster = sheet_dict[(self.i - 1, self.j)]
            return top_cluster.label, top_cluster.cluster_index
        return None, None

    @staticmethod
    def get_sorted_clusters():
        """Returns sorted clusters by size (largest first), excluding empty clusters."""
        return sorted([cluster for cluster in Cluster.clusters if cluster], key=len, reverse=True)

# Grid size and probability
k = 10
p = 0.8

# Generate sheet with percolation probability
sheet = np.ones((k, k))
num_zeros = int(k**2 * p)
sheet.flat[:num_zeros] = 0  # Set first num_zeros elements to 0
np.random.shuffle(sheet.flat)  # Shuffle in place

# Populate clusters, handling boundary cases
for i in range(k):
    for j in range(k):
        if sheet[i, j] == 1:
            sheet_dict[(i, j)] = Cluster(i, j)

# Print results
sorted_clusters = Cluster.get_sorted_clusters()
print(sheet)
print("\nSorted Clusters (by size):")
for cluster in sorted_clusters:
    print(f"Size: {len(cluster)}, Labels: {cluster}")
