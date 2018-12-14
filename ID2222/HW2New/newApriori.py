import pandas as pd
import numpy as np
import itertools as it
from tqdm import tqdm
import time


s = 1000


#returns list of set(baskets)
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

################Generate a characteristic Matrix of elements##############
### rows are basket nr
### columns are items
def char_matrix(baskets):
    rows= len(baskets)
    basket_unique = list(set([e for x in baskets for e in x]))
    col = len(basket_unique)
    mat = np.zeros((rows, col))
    for r in tqdm(range(rows)):
        for c in range(col):
            if basket_unique[c] in baskets[r]:
                mat[r][c] = 1

    return mat, basket_unique

char_m, elements_char_m = char_matrix(baskets)

''' input: characteristic matrix
            columns names of the characteristic matrix
    output: frequency of items
            items
'''
def single(char_m, elements):
    count = np.sum(char_m, axis=0)
    above_threshold = np.where(count > s)
    idxs = above_threshold[0]
    items = [elements[i] for i in idxs]
    # print(items)
    singles = count[np.where(count > s)]
    singles = list(zip(items, singles))
    return singles, items

singles,items = single(char_m, elements_char_m)

'''function removes infrequent items from characteristic matrix
    input: frequent single items
          characteristic matrix
          items (columns) of the characteristic matrix
   output: characteristic matrix with single items as columns
           single items
'''
def remove_infrequentItems_from_main(items, char_m, elements):
    idx = np.zeros((char_m.shape[0], len(items)))
    for i in tqdm(range(len(elements))):
        for j in range(len(items)):
            if elements[i] == items[j]:
                idx[:, j] = char_m[:, i]

    return idx, items

char_m, elements_char_m = remove_infrequentItems_from_main(items, char_m, elements_char_m)

# print(elements_char_m)

def comb_list(column, r):
    return list(it.combinations(column, r))


pair_items = comb_list(elements_char_m, 2)
pair_items = np.asarray(list(zip(*pair_items)))

def check_count_pair(pair_items, char_m, elements_char_m):
    count = []
    new_items = []
    # print(pair_items)
    for i in tqdm(range(pair_items.shape[1])):
        pair1 = char_m[:, elements_char_m.index(pair_items[0,i])]
        pair2 = char_m[:, elements_char_m.index(pair_items[1,i])]
        checking = np.count_nonzero(np.multiply(pair1, pair2))
        # new_items.append((pair_items[0, i], pair_items[1, i]))
        count.append((checking, pair1, pair2))
        # if checking > s:
        #     count.append(checking)
        #     new_items.append((pair_items[0,i],pair_items[1,i]))


    return new_items, count

start = time.time()
count, pairs = check_count_pair(pair_items, char_m, elements_char_m)
end = time.time()
print("time: ", end-start)
print("(pair1, pair2)")
print(pairs)
print("nr of pairs: ", len(pairs))

# char_m, elements_char_m = remove_infrequentItems_from_main(pairs, char_m, elements_char_m)
#
#
# print(list(zip(*elements_char_m)))
# triple_items = comb_list(zip(*elements_char_m), 3)
# # triple_items = np.asarray(list(zip(*triple_items)))
# print(comb_list(list(zip(*elements_char_m)), 3))