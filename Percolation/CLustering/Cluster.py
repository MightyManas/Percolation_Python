import numpy as np
import os
from graphing import graphing_tool as gt

def exponential_decay(x, a, b, xi):
    """Safe evaluation with numerical guards"""
    with np.errstate(all='ignore'):
        return a + x*(-b) - (np.exp(x)/xi)

def parse_cluster_file(filepath):
    """Bulletproof parser for your exact file format"""
    sizes = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if 'Size = ' not in line:
                    continue
                try:
                    # Extract the exact numeric part after 'Size = '
                    size_str = line.split('Size = ')[1].strip().split()[0]
                    size = int(float(size_str))
                    if size > 0:  # Only positive sizes
                        sizes.append(size)
                except (ValueError, IndexError):
                    continue
        return np.array(sizes, dtype=np.int64)
    except Exception as e:
        print(f"Error reading {filepath}: {str(e)}")
        return None

def analyze_distribution(sizes, p_value=None):
    """Numerically stable analysis"""
    if sizes is None or len(sizes) == 0:
        print("No valid cluster sizes found")
        return
    
    # Create distribution with safeguards
    unique, counts = np.unique(sizes, return_counts=True)
    
    # Apply multiple safety filters
    valid_mask = (unique > 0) & (counts > 0)
    unique = unique[valid_mask]
    counts = counts[valid_mask]
    
    # Safe log transform
    with np.errstate(all='ignore'):
        log_sizes = np.log(unique)
        log_counts = np.log(counts)
    
    # Remove infinite/NaN values
    finite_mask = np.isfinite(log_sizes) & np.isfinite(log_counts)
    
    if not np.any(finite_mask):
        print("No finite values available for fitting")
        return
    
    # Use your graphing tool
    gt(exponential_decay,
       xdata=log_sizes[finite_mask],
       ydata=log_counts[finite_mask],
       p0=[1, 4/3, 0.55],
       dx = 1 / (unique * np.log(10)), # Error on log(s)
       dy = 1 / (counts * np.log(10)),  # Error on log(P(s))
       title=f'Cluster Size Distribution (p = {p_value})' if p_value else 'Cluster Size Distribution',
       xlabel='log(Cluster Size)',
       ylabel='log(Count)')

if __name__ == "__main__":
    # Set working directory - using raw string for Windows paths
    os.chdir(r"S:\programing_files\Sem\Percolation\data")
    
    INPUT_FILE = "data_7.txt"
    print(f"Processing {INPUT_FILE} from {os.getcwd()}...")
    
    # Debug: List files in directory
    print("Files in directory:", os.listdir())
    
    cluster_sizes = parse_cluster_file(INPUT_FILE)
    # Filter cluster sizes: 10 <= size <= 5000
    cluster_sizes = cluster_sizes[(cluster_sizes >= 20 ) & (cluster_sizes <= np.exp(7.5))]

    if cluster_sizes is not None:
        print(f"Analyzing {len(cluster_sizes)} clusters")
        print("Size stats - Min:", np.min(cluster_sizes), 
              "Max:", np.max(cluster_sizes),
              "Mean:", np.mean(cluster_sizes))
        
        analyze_distribution(cluster_sizes, p_value=0.585 + 0.001 * 7)
    else:
        print("Failed to process the input file")