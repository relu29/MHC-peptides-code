import requests, sys, json
import argparse
from pathlib import Path
import pandas as pd
import os
import time
import re

# Initialize argument parser
argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='input file', type=str, required=True)
argparser.add_argument('-o', '--output', help='output dir', type=str, required=True)
argparser.add_argument('-f', '--filename', help='output file name', type=str, required=True)

args = argparser.parse_args()

# Define function for obtaining accesion number list from raw PEAKS peptide dataset with at least Peptide and Accession columns
def transform_input(file):

    accession_list = []
    df = pd.read_csv(file)
    df = df[['Peptide', 'Accession']]

# Look for first accesiion number in Acession column
    for i in range(len(df)):
        r = re.search('[A-Z]\w*', str(df.iloc[i, 1]))
        result = r.group(0) if r else ""

# Exclude contamination peptides
        if result != 'CONTAM':
            accession_list.append(result)

    return accession_list

# Define function to get response from url
def get_url(url, **kwargs):
    response = requests.get(url, **kwargs)

    if not response.ok:
        print(response.text)
        response.raise_for_status()
        sys.exit()

    return response

# Function to retrieve protein names from UniProt using API and count ocurrances. Makes a dictionary
def get_protein_dict(list):

    accession_list = list
    web_api = 'https://rest.uniprot.org'
    protein_dict = {}

    for number in accession_list:

        try:
            r = get_url(f'{web_api}/uniprotkb/{number}?fields=protein_name')

            data = json.dumps(r.json(), indent = 2)
            try:
                json_object = json.loads(data)['proteinDescription']['recommendedName']['fullName']['value']

            except:
                json_object = json.loads(data)['proteinDescription']['submissionNames'][0]['fullName']['value']

            if json_object in protein_dict.keys():
                protein_dict[json_object] += 1

            else:
                protein_dict[json_object] = 1
        except:
            print(f'Accession number {number} not found')
            pass
        time.sleep(0.3)

    return protein_dict

# Function to build dataframe in form of csv file from dictionary. Incorporates all other functions
def create_final_df(input):
    accession_list = transform_input(input)
    result_dictionary = get_protein_dict(accession_list)

    df = pd.DataFrame.from_dict(result_dictionary, orient = 'index', columns = ['n_of_ocurrences'])
    df = df.reset_index()
    df = df.rename(columns = {df.columns[0]: 'protein'})


    # Save dataframes as csv_files
    os.makedirs(args.output, exist_ok=True)
    df.to_csv(r"{}".format(args.output + "/" + args.filename + ".csv"))

create_final_df(args.input)
