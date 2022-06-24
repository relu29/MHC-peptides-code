import pandas as pd
import argparse
import re
import os
import glob
import ntpath

# Initialize the argument parser
argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='input directory', type=str, required=True)
argparser.add_argument('-o', '--output', help='output dir', type=str, required=True)

args = argparser.parse_args()

# Use glob to get all csv files in directory
path = os.getcwd()

csv_files = []
for path in os.listdir(args.input):
  full_path = os.path.join(args.input, path)
  if os.path.isfile(full_path):
    csv_files.append(full_path)

# Loop over csv file list and read them
dfdict = {}
for file in csv_files:

    # Append files to dictionary with names
    dfdict["{0}".format(os.path.basename(file)).replace('.csv', '_binders')] = pd.read_csv(file, delimiter = '\t', header = 1)

# Create df with only peptide and EL_Rank columns for all alleles, only binding peptides
for key in dfdict.keys():
    df = dfdict[key]
    dframe = df.loc[df['EL_Rank'] < 2.001, ['Peptide', 'EL_Rank']]
    dframe = dframe.reset_index(drop = True)
    dframe = dframe.drop_duplicates()
    
    print(dframe.head(5))

    #save dataframes as csv_files
    os.makedirs(args.output, exist_ok=True)
    dframe.to_csv(r"{}".format(args.output + "/" + key + ".csv"))
