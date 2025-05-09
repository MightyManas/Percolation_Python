import numpy as np
import os
from graphing import graphing_tool as gt

def parse_cluster_file(filepath):
    """Extract cluster sizes from a file"""
    sizes = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if 'Size = ' not in line:
                    continue
                try:
                    size_str = line.split('Size = ')[1].strip().split()[0]
                    size = int(float(size_str))
                    if size > 0:
                        sizes.append(size)
                except (ValueError, IndexError):
                    continue
        return np.array(sizes, dtype=np.int64)
    except Exception as e:
        print(f"Error reading {filepath}: {str(e)}")
        return None

def compute_average_cluster_size(sizes):
    """Compute average cluster size S = sum(s^2 * n(s)) / sum(s * n(s))"""
    if sizes is None or len(sizes) == 0:
        return None
    unique, counts = np.unique(sizes, return_counts=True)
    numerator = np.sum((unique**2) * counts)
    denominator = np.sum(unique * counts)
    if denominator == 0:
        return None
    return numerator / denominator


def power_law(p, a, gamma, p_c):
    """Fit function: a * |p - p_c|^{-gamma}"""
    epsilon = 1e-10  # to avoid division by zero
    return a * np.abs(p - p_c + epsilon) ** (-gamma)


def analyze_S_vs_p(data_folder="data/", file_template="data_{i}.txt",
                   p_start=0.587, p_step=0.001, first_file=12, last_file=28):

    S_values = []
    p_values = []

    for i in range(first_file, last_file + 1):
        # Debug: file existence
        filename = os.path.join(data_folder, file_template.format(i=i))
        p = p_start + p_step * (i - first_file)



        sizes = parse_cluster_file(filename)
        if sizes is None:
            print("  → parse_cluster_file returned None\n")
            continue

        print(f"  Parsed sizes before filtering: {len(sizes)}")
        filtered = sizes[(sizes >= 0) & (sizes <= np.inf)]
        print(f"  Sizes after [10–5000] filter:   {len(filtered)}")

        S = compute_average_cluster_size(filtered)
        if S is not None:
            p_values.append(p)
            S_values.append(S)
            print(f"  → p = {p:.3f}, S = {S:.3f}")
        else:
            print("  → Skipped (no valid S)\n")

    if not S_values:
        print("\nNo valid data for plotting. Please check file existence and contents.")
        return

    gt(power_law,
       xdata=p_values,
       ydata=S_values,
       p0=[1, 43/18, 0.590],
       dx=0.0,
       dy=0.1,
       title='Average Cluster Size S vs Probability p',
       xlabel='Probability (p)',
       ylabel='Average Cluster Size S')



if __name__ == "__main__":
    analyze_S_vs_p()
