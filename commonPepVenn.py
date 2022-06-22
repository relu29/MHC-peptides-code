import matplotlib.pyplot as plt
import argparse
import os
import glob
import pandas as pd
import numpy as np
from venn import venn

# Initialize the argument parser
argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='input directory', type=str, required=True)
argparser.add_argument('-o', '--output', help='output dir', type=str, required=True)
argparser.add_argument('-t', '--threshold', help='EL_Rank threshold', type=float, required=False, default = 2)

args = argparser.parse_args()

# Create list with sets for Venn diagram and load files into csv_files
path = os.getcwd()
csv_files = glob.glob(os.path.join(r"{}".format(args.input), "*.csv"))

# Create dictionary with filtered sets of peptides (using threshold value for EL_Rank)
set_dict = {}

for file in csv_files:
    read_file = pd.read_csv(file)
    new_df = read_file.loc[read_file['EL_Rank'] < args.threshold, 'Peptide']
    set_dict["{0}".format(os.path.basename(file).replace('.csv', ''))] = new_df

# Add each key name as group label and each set as values for the venn diagram
label_list = []

for key,value in set_dict.items():
    set_dict[key] = set(value.values)
    label_list.append(key)

# Set colorblind palette
cb_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']

# Plot the diagram
fig, ax = plt.subplots(1, figsize=(16,12))
venn(set_dict, ax=ax, cmap = cb_color_cycle)
plt.legend(label_list, ncol=len(label_list), loc = 9)
plt.show()
