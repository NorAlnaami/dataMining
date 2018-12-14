import pandas as pd
import numpy as np
import itertools as it
from tqdm import tqdm
import time


#returns list of sets(baskets)
def read_main_file():
    content = []
    with open("T10I4D100K.dat", 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    new_content = []
    for i in range(len(content)):
        new_content.append(set(content[i].split(" ")))

    return new_content


baskets = read_main_file()


def read_file():
    doc = open("T10I4D100K.dat", 'r').read().replace('\n', '')
    list_file = doc.split(" ")
    ones = np.ones((len(list_file)-1,1))
    list_file = list(zip(list_file, ones))
    return list_file


def comb_list(column, r):
    return list(it.combinations(column, r))


file = read_file()
s = 1000

main_df = pd.read_table("T10I4D100K.dat", sep='\n', names=['items'])
# C1
singles = pd.DataFrame(data=file, columns=['items', 'count']).groupby('items', as_index=False).sum()
# L1
singles = singles[(singles['count'] >= s)]

# removes all singles found from the main basket for the next search
def keep_singles_inMain(baskets, singles):
    keep = []
    for i in range(len(baskets)):
        keep_list = []
        for single in singles:
            if single in baskets[i]:
                keep_list.append(single)
        keep.append(set(keep_list))

    return keep
# baskets = keep_singles_inMain(baskets, singles['items'])

# C2
# checks frequency of item in all baskets
# returns frequency of item in baskets
def check_freq_item(baskets, element, r):
    count = 0
    # print(baskets[0])
    # print(element)
    for i in tqdm(range(len(baskets))):
        if baskets[i].issuperset(element):
            count += 1

    return count

# checks the frequency of each pair

def check_all_pairs(pairs, baskets, r):
    freq = []
    for element in tqdm(pairs):
        freq.append((element,check_freq_item(baskets, element, r)))
    return freq

pairs = np.asarray(comb_list(singles['items'], 2))

# fre = check_all_pairs(pairs, baskets, 2)
# print(fre)






################Generate a characteristic Matrix of elements##############
### rows are basket nr
### columns are items
def char_matrix(baskets):
    rows= len(baskets)
    basket_unique = list(set(list(it.chain(*baskets))))
    col = len(basket_unique)
    print("col: ", col)
    mat = np.zeros((rows, col))
    for r in tqdm(range(rows)):
        for c in range(col):
            if basket_unique[c] in baskets[r]:
                mat[r][c] = 1

    return mat, basket_unique
char_m, basket_unique = char_matrix(baskets)
# print(char_m.shape)

def search(char_m, basket_unique, pairs):
    df = pd.DataFrame(data=char_m, columns=basket_unique)
    counts = []
    everything = np.zeros((len(pairs), 3))
    start = time.time()
    # print(char_m[:, int(pairs[0][0])])
    print(np.count_nonzero(np.multiply(char_m[:, int(pairs[0][0])], char_m[:, int(pairs[0][1])])))
    # counts.append(df.groupby([pairs[0][0], pairs[0][1]]).size().to_frame('count').reset_index()['count'][3])
    end = time.time()
    time_takes = (end - start)*len(pairs)
    print(end - start)
    print(time_takes)
    i = 0
    for pair in tqdm(pairs):
        print(int(pair[0]))
        print(int(pair[1]))
        print(char_m.shape)
        v = np.multiply(char_m[:, int(pair[0])], char_m[:, int(pair[1])])
        val = np.count_nonzero(np.multiply(char_m[:, int(pair[0])], char_m[:, int(pair[1])]))
        counts.append(val)
        everything[i] = [val, pair[0], pair[1]]
        i += 1
        #counts.append(df.groupby([pair[0], pair[1]]).size().to_frame('count').reset_index()['count'][3])
        # if bigger > s:
        #      counts.append((pair, bigger))
    # df['new_count'] = counts
    # print(df)
    print(everything)
    return counts

search(char_m, basket_unique, pairs)