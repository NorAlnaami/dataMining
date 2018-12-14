import pandas as pd
import numpy as np
import itertools as it

def read_file():
    doc = open("T10I4D100K.dat", 'r').read().replace('\n', '')
    list_file = doc.split(" ")
    ones = np.ones((len(list_file)-1,1))
    list_file = list(zip(list_file, ones))
    return list_file

def comb_list(df ,column, r):
    return list(it.combinations(df[column], r))

file = read_file()
s = 1000

main_df = pd.read_table("T10I4D100K.dat", sep='\n', names=['items'])
# C1
singles = pd.DataFrame(data=file, columns=['items', 'count']).groupby('items', as_index=False).sum()
# L1
singles = singles[(singles['count'] >= s)]




def read_file2():
    doc = open("T10I4D100K.dat", 'r').read().replace('\n', '')
    list_file = doc.split(" ")
    print(len(set(list_file)))
    # list_file = list(it.combinations(list_file, 2))
    #list_file = np.asarray(list_file).reshape((len(list_file), 1))
    #print(list_file.shape)
    print(list_file)
    ones = np.ones((len(list_file)-1, 1))
    list_file = list(zip(list_file, ones))
    return list_file


pairs = pd.DataFrame(data=read_file2(), columns=['items', 'count'])
# print(pairs)

# C2
# print(comb_list(singles, 'items', 2))
# print(singles)
# a = [1,2,3]
# b = [1,2,3]
# c = list(it.combinations(a,2))
# print(c)
