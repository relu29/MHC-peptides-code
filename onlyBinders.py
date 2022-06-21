import pandas as pd
import argparse
import re
import os
import glob

# Initialize the argument parser
argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='input directory with files', type=str, required=True)
argparser.add_argument('-o', '--output', help='output directory', type=str, required=True)

args = argparser.parse_args()

# Use glob to get all csv files in directory
path = os.getcwd()
csv_files = glob.glob(os.path.join(r"{}".format(args.input), "*.csv"))

# Loop over csv file list and read them
dfdict = {}
for file in csv_files:

    # Append files to dictionary with names
    dfdict["{0}".format(os.path.basename(file)).replace('.csv', '_binders')] = pd.read_csv(file)

# Create df with only peptide and EL_Rank columns for all alleles, only binding peptides
for key in dfdict.keys():
    df = dfdict[key]
    dframe = df.loc[df['EL_Rank'] < 2.001, ['Peptide', 'EL_Rank']]
    dframe = dframe.reset_index(drop = True)
    print(dframe.head(5))

    #save dataframes as csv_files
    os.makedirs(args.output, exist_ok=True)
    dframe.to_csv(r"{}".format(args.output + "/" + key + ".csv"))
