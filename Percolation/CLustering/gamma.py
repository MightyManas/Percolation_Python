import numpy as np
import os
from graphing import graphing_tool as gt

def power_law(p, a, gamma, p_c):
    """Power law model for fitting |p - p_c|^(-gamma), with a safeguard for divide-by-zero."""
    epsilon = 1e-10  # Small constant to avoid division by zero
    return a * np.abs(p - p_c + epsilon)**(-gamma)

def parse_cluster_file(filepath):
    """Extract cluster sizes from a file"""
    sizes = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if 'Size = ' not in line:
                    continue
                try:
                    # Extract the cluster size value
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

def get_y_values(sizes, p_c):
    """Calculate S = ∑ s² n(s) / p_c"""
    unique, counts = np.unique(sizes, return_counts=True)
    
    # Calculate S using the formula: ∑ s² n(s) / p_c
    S_values = np.sum((unique**2) * counts) / p_c
    return S_values

def analyze_distribution_for_probabilities(sizes, p_c):
    """Analyze and fit the distribution for varying probabilities"""
    if sizes is None or len(sizes) == 0:
        print("No valid cluster sizes found")
        return
    
    # Get y values for each probability
    S_values = get_y_values(sizes, p_c)
    
    # Generate 12 distinct probability values
    probabilities = np.linspace(0.585, 0.585 + 0.001 * 11, 12)  # From 0.585 to 0.595
    
    # Prepare y-data and p-values for fitting
    y_data = []
    p_data = []
    
    for p in probabilities:
        y_data.append(S_values)
        p_data.append(p)
    
    # Convert to numpy arrays
    y_data = np.array(y_data)
    p_data = np.array(p_data)
    
    # Filter out invalid values (infinity or NaN)
    valid_mask = np.isfinite(y_data) & np.isfinite(p_data)
    y_data = y_data[valid_mask]
    p_data = p_data[valid_mask]
    
    if len(p_data) == 0 or len(y_data) == 0:
        print("No valid data available for fitting")
        return
    
    # Error bars for p and S
    dx = 0.001  # Error for probabilities (could be adjusted based on data)
    dy = 0.1    # Error for S (could be adjusted based on data)
    
    # Fit the model using graphing tool
    gt(power_law,
       xdata=p_data,  # Probability data
       ydata=y_data,  # Corresponding y values (S)
       p0=[1, 2, p_c],  # Initial guesses (a, gamma, p_c)
       dx=dx,  # Error on p values
       dy=dy,  # Error on S values
       title=f'S vs p (p_c = {p_c})',
       xlabel='Probability (p)',
       ylabel='S (sum of s² n(s) / p_c)')

# Main function to read data and perform analysis for a given probability
if __name__ == "__main__":
    # Set working directory
    os.chdir(r"S:\programing_files\Sem\Percolation\data")
    
    # Set input file path (update this to the correct file)
    INPUT_FILE = "data_7.txt"
    print(f"Processing {INPUT_FILE} from {os.getcwd()}...")
    
    # Read the cluster sizes from the file
    cluster_sizes = parse_cluster_file(INPUT_FILE)
    
    # Set critical probability value (p_c)
    p_c = 0.585  # You can change this to another value if needed
    
    # If cluster sizes are valid, analyze and fit the data
    if cluster_sizes is not None:
        print(f"Analyzing {len(cluster_sizes)} clusters")
        print("Size stats - Min:", np.min(cluster_sizes), 
              "Max:", np.max(cluster_sizes),
              "Mean:", np.mean(cluster_sizes))
        
        # Perform analysis and fitting for probabilities ranging from 0.585 to 0.595
        analyze_distribution_for_probabilities(cluster_sizes, p_c)
    else:
        print("Failed to process the input file")
