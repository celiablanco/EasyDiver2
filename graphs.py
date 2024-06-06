#!/usr/bin/env python3

"""
graphs.py plots a histogram for sequence length, a scatterplot comparing enrichment values, and a line chart showing
total and unique AA counts over time.
"""
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
import sys

def remove_outliers(x_values, y_values, zscore_threshold=3):
    """
   This function removes outliers from the given x and y values based on the provided z-score threshold.
    Used to graph scatterplot.
   Parameters:
   x_values (list): A list of x-values from which outliers are to be removed.
   y_values (list): A list of y-values from which outliers are to be removed.
   zscore_threshold (int): The z-score threshold to identify an outlier. Default is 3.

   Returns:
   x_values_filtered (numpy array): The filtered x-values after removing outliers.
   y_values_filtered (numpy array): The filtered y-values after removing outliers.
    """
    # Calculate Z-scores for x and y
    x_zscores = np.abs((x_values - np.mean(x_values)) / np.std(x_values))
    y_zscores = np.abs((y_values - np.mean(y_values)) / np.std(y_values))

    # Create a mask to filter outlier points
    outlier_mask = (x_zscores <= zscore_threshold) & (y_zscores <= zscore_threshold)

    # Apply the mask to keep only non-outlier points
    x_values_filtered = np.array(x_values)[outlier_mask]
    y_values_filtered = np.array(y_values)[outlier_mask]

    return x_values_filtered, y_values_filtered

def generate_graphs():
    file_path = sys.argv[1]
    graph = sys.argv[2]
    
    # Check if figures directory exists
    figures = os.path.join(file_path, "figures")
    if not os.path.exists(figures):
        os.makedirs(figures)
    
    # Set seaborn style
    sns.set_theme(style="darkgrid")

    # Scatterplot
    if graph == "1":
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        # Set res file dir
        res_dir = f"{file_path}/modified_counts/"

        # Initialize lists to store the values
        e_out_values = []
        e_neg_values = []

        # If res files don't exist, exit
        res_files = os.listdir(res_dir)
        if not res_files:
            return

        # Open and read the file
        for res_file in res_files:
            with open(f"{res_dir}/{res_file}", 'r') as file:
                lines = file.readlines()

            # Extracting relevant data from the lines
            start_index = 7
            for line in lines[start_index:]:
                columns = line.split(',')
                if '-' in (columns[-3], columns[-4], columns[-5], columns[-6]):
                    continue
                try:
                    # Calculate e_out and e_neg values
                    e_out = float(re.sub(r'[^\d.]', '', columns[-6]))
                    e_neg = float(re.sub(r'[^\d.]', '', columns[-4]))

                    # Append to respective lists
                    e_out_values.append(e_out)
                    e_neg_values.append(e_neg)
                except ValueError as ve:
                    print(f"Skipping line due to value error: {line}")
                    continue

            # Remove outliers
            x_filtered, y_filtered = remove_outliers(e_neg_values, e_out_values)

            # Perform linear regression
            slope, intercept = np.polyfit(x_filtered, y_filtered, 1)
            fit_line = np.poly1d([slope, intercept])

            # Create scatter plot
            plt.figure(figsize=(10, 6))
            plt.scatter(x_filtered, y_filtered, s=10)
            plt.plot(x_filtered, fit_line(x_filtered), color='blue', linestyle='dotted', linewidth=1)

            # Plot the regression line
            plt.plot(x_filtered, fit_line(x_filtered), color='blue', linestyle='dotted', linewidth=1, label=f'Regression Line (slope = {slope:.2f})')

            # Plot the diagonal line y = x
            plt.plot(x_filtered, x_filtered, color='red', linestyle='-', linewidth=1, label='y = x')

            # Adding labels and title
            plt.xlabel('e_neg')
            plt.ylabel('e_out')
            plt.title('e_neg vs e_out Scatter Plot')

            # Add legend
            plt.legend()
            
            # Save the plot as an image
            output_file = os.path.join(f"{file_path}/figures", f"{os.path.splitext(res_file)[0]}.png")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            plt.savefig(output_file, dpi=500)
            plt.close()

    # Histogram
    elif graph == "2":
        histos = os.path.join(file_path, "histos")
        files = [file for file in os.listdir(histos) if file.endswith(".txt")] # Find data for histos

        for file in files:
            filename = os.path.join(histos, file)
            lines = None
            with open(filename, 'r') as f:
                lines = f.readlines()

            lengths = []
            reads_counts = []
            start = lines.index("Len  Reads  %Reads\n") + 1 # Start line for data

            for line in lines[start:]:
                values = line.split()
                length = int(values[0])
                reads_count = int(values[1])
                lengths.append(length)
                reads_counts.append(reads_count)
            plt.figure(figsize=(12, 8))

            # Plotting the histogram without log scale
            color = "blue" if 'aa' in filename else "green"
            plt.bar(lengths, reads_counts, color=color)
            plt.xlabel('Length')
            plt.ylabel('Reads Count')
            plt.title('Read Length Histogram for ' + file)

            plt.tight_layout()  # Adjust spacing between subplots

            plt.savefig(f"{figures}/" + file[:file.rfind(".")] + ".png", dpi=500)
            plt.close()
            
    # Line graph
    elif graph == "3":
        file_path += "/log.txt"

        # Lists to store the data
        sample_names = []
        unique_aa = {}
        total_aa = {}
        max_round = -1
        # Read the text file and extract the data
        with open(file_path, 'r') as file:
            lines = file.readlines()
            start = False  # Initialize a flag to identify the start of relevant data
            for line in lines:
                if line.startswith("sample"):
                    start = True
                    continue
                elif start:
                    total_aa_ind = -1
                    line_data = line.split()  # Split the line into individual data points
                    if line_data[-1][-1] == '%':
                        total_aa_ind -= 1 # Solves formatting issues if recovered_aa(%) decides to print

                    sample_name = line_data[0]
                    sample_name_substr = sample_name.split("-")[1]

                    sample_names.append(sample_name)  # Store the first data point (sample name)
                    max_round = max(max_round, int(sample_name.split("-")[0]))

                    # Extract unique AA count and handle percentage if present
                    unique_aa_count = line_data[total_aa_ind - 1]
                    if unique_aa_count.endswith('%'):
                        unique_aa_count = unique_aa_count.rstrip('%')
                    unique_aa_count = int(float(unique_aa_count))

                    # Extract total AA count and handle percentage if present
                    total_aa_count = line_data[total_aa_ind]
                    if total_aa_count.endswith('%'):
                        total_aa_count = total_aa_count.rstrip('%')
                    total_aa_count = int(float(total_aa_count))

                    # Append unique amino acid (AA) counts to a dictionary, using the AA type as the key
                    unique_aa.setdefault(sample_name_substr, []).append(unique_aa_count)
                    
                    # Append total AA counts to a dictionary, using the AA type as the key
                    total_aa.setdefault(sample_name_substr, []).append(total_aa_count)

        print("Unique amino acid (AA) counts throughout rounds: " + str(unique_aa))
        print("Total amino acid (AA) counts throughout rounds: " + str(total_aa))
        # Create a figure for plotting
        plt.figure(figsize=(10, 6))

        # Iterate through different AA types
        for key in unique_aa.keys():
            if key == "neg":
                color = "red"
            elif key == "in":
                color = "orange"
            else:
                color = "green"
                
            label_u = "Unique AA " + key
            label_t = "Total AA " + key
            # Plot the unique AA counts and label with the AA type
            plt.plot(unique_aa[key], marker="o", label=label_u, color=color)
            # Plot the total AA counts and label with the AA type
            plt.plot(total_aa[key], marker="o", label=label_t, color="dark" + color)

        # Add labels and title to the plot
        plt.xlabel('Round')
        plt.ylabel('Count')
        plt.title('Unique and Total Amino Acid Counts Throughout Experiment')

        # Add a legend to distinguish unique and total counts for each AA type
        plt.legend()
        # Customize x-axis labels to show round numbers
        plt.xticks(range(0, max_round), [f'#{i}' for i in range(1, max_round + 1)], rotation=45)
        # Adjust layout for better appearance
        plt.tight_layout()

        # Save the plot as an image with high resolution (DPI: 500)
        plt.savefig(f"{figures}/Selection Counts Reads.png", dpi=500)
        
if __name__ == '__main__':
    generate_graphs() 
