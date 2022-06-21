import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup, SoupStrainer
import urllib3
import time

#load peptide csv as pandas dataframe
csvf = str(input('Write CSV File\n'))
data = pd.read_csv(csvf)
print(data['Leading razor protein'].dtypes)

#number of razor_proteins
razor_proteins = data['Leading razor protein'].head(10)
print('Number of proteins: ')
print(len(razor_proteins))


#function to get species name from uniprot
def beauty(urlf):
    http = urllib3.PoolManager()

    url = urlf
    response = http.request('GET', url)

    onlyFirstEm = SoupStrainer("div", {'id': 'content-organism'})

    soup = BeautifulSoup(response.data, 'html.parser', parse_only = onlyFirstEm)
    species_box = soup.find('em')
    name = species_box.text
    return name

#generate url list with proteins for uniprot
def generate_url_list(series):
    url_list = list()
    for i in series:
        urln = 'https://www.uniprot.org/uniprot/{}'.format(i)
        url_list.append(urln)
    return url_list

#generate pandas series containing all species names
def get_species(url_list):
    species = list()
    for url in url_list:
        try:
            ret_sp = beauty(url)
            species.append(ret_sp)
            time.sleep(1)
        except:
            species.append(np.nan)
            time.sleep(1)
    return species

#creates dataframe with counts per species and plots in the form of piechart
def pieplot(speseries):
    plt.figure()
    df2 = speseries.value_counts().rename_axis('Species').reset_index(name = 'Counts')
    values = df2['Counts']
    labels = df2['Species']
    plt.pie(values, labels = labels, autopct = '%1.1f%%')
    plt.axis('Equal')
    plt.title('Species of origin of peptides')
    plt.show()
    print(df2.head(10))


#main function incorporating all others
def main(peptide_list):
    urllist = generate_url_list(peptide_list)
    print('\nSpecies list:')
    species_df = pd.DataFrame({'Species': get_species(urllist)})
    pieplot(species_df)


main(razor_proteins)
