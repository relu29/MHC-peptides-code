import pandas as pd
import os
import argparse
import glob
from venn import venn
import matplotlib.pyplot as plt
import numpy as np
import sys

# Initialize the argument parser
argparser = argparse.ArgumentParser()
argparser.add_argument('-l', '--list', nargs='+', help='csv file list (paths)', type=str, required=True)
argparser.add_argument('-o', '--output', help='output dir', type=str, required=False)
argparser.add_argument('-n', '--name', help='Name of output jpg file', type=str, required=False, default = 2)

args = argparser.parse_args()

#Specify max number of input csv_files
if len(args.list) > 2:
    sys.exit('\nMax number of input files is 2')

path = os.getcwd()
# Create list with all csv files
csv_files = args.list

print(csv_files)
# Create dictionary containing files
file_dict = {}

for file in csv_files:
    read_file = pd.read_csv(file)
    file_dict["{0}".format(os.path.basename(file).replace('.csv', ''))] = read_file

# Create dataframe with common peptides
key_list = []
for key, value in file_dict.items():
    key_list.append(key)

df1 = pd.DataFrame(file_dict[key_list[0]]['Peptide'])
df2 = pd.DataFrame(file_dict[key_list[1]]['Peptide'])

# Make dataframe with unique and common peptides of input datafiles
df_all = df1.merge(df2.drop_duplicates(), on = ['Peptide'], how = 'outer', indicator = True)

data = {'Unique peptides {0}'.format(key_list[0]): df_all['Peptide'][df_all['_merge'] == 'left_only'],
'Unique peptides {0}'.format(key_list[1]): df_all['Peptide'][df_all['_merge'] == 'right_only'],
'Common peptides': df_all['Peptide'][df_all['_merge'] == 'both']}

df_pep_back = pd.DataFrame(data)
print(df_pep_back.head(5))

os.makedirs(args.output, exist_ok=True)
df_pep_back.to_csv(r"{}".format(args.output + "/" + args.name + ".csv"))

# Set colorblind palette
cb_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']

# Plot the diagram
set1 = set(df1['Peptide'])
set2 = set(df2['Peptide'])

set_dict = {'set1': set1, 'set2': set2}

fig, ax = plt.subplots(1, figsize=(16,12))
venn(set_dict, ax=ax, cmap = cb_color_cycle)
plt.legend(('{0}'.format(key_list[0]), '{0}'.format(key_list[1])), ncol=len(set_dict), loc = 9)


# Save figure in output directory
figure_path = os.path.join(args.output, '{0}.jpg'.format(args.name))
plt.savefig(figure_path)
