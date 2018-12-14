import numpy as np
import itertools as it
# from tqdm import tqdm
import time


s = 1000
c = 0.5

# read file returns list of set(baskets)
def read_main_file():
    content = []
    with open("T10I4D100K.dat", 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    new_content = []
    for i in range(len(content)):
        basket = [int(s) for s in content[i].split(" ")]
        new_content.append(set(basket))


    return new_content


baskets = read_main_file()

# check for single frequent items
def singles(baskets, s):
    dict_item = {}
    for basket in baskets:
        for item in basket:
            if item in dict_item:
                dict_item[item] +=1
            else:
                dict_item[item] = 1

    dict_singles = {key:dict_item[key] for key in dict_item.keys() if dict_item[key]>s}
    return dict_singles

single = singles(baskets, s)
print("single items: ", single)
print("frequent single itemsets: ", len(single))

def check(set_item, pair_single, k):
    count = 0
    for item in set_item:
        if item in pair_single:
            count +=1
    if count == k:
        return True
    else:
        return False


def pairs(baskets, single, s, k):
    single_items = set(single.keys())
    pair_single = set(single.keys())#set(list(it.combinations(single.keys(), k-1)))
    pair_dict = {}

    # removed infrequent items from baskets
    for basket in baskets:
        # new_baskets.append(basket.intersection(single_items))
        new_b = list(single_items.intersection(basket))
        new_b.sort()

        basket_comb = set(it.combinations(new_b, k))
        for set_item in basket_comb:
            if check(set_item, pair_single, k):
                # pair_dict[set_item] = 1
                if set_item in pair_dict:
                    pair_dict[set_item] +=1
                else:
                    pair_dict[set_item] =1

    dict_pair = {key:pair_dict[key] for key in pair_dict.keys() if pair_dict[key]>s}

    return dict_pair


pair_dict = pairs(baskets, single, s, 2)

print("pair items: ", pair_dict)
print("frequent pair itemsets: ", len(pair_dict))


def check_triple(item_set, pairs_flat, k):
    count = 0
    pairs = set(it.combinations(pairs_flat, k-1))

    pairs_triple = set(it.combinations(item_set, k-1))
    for item in pairs_triple:
        if item in pairs:
            count +=1
    if count ==k:
        return True
    else:
        return False


def triples(baskets, pair_dict, s, k):
    triple_dict = {}
    pairs_flat = [x for item in pair_dict.keys() for x in item]
    pairs_flat.sort()
    for basket in baskets:
        new_b = list(basket.intersection(pairs_flat))
        new_b.sort()
        new_b_comb = list(it.combinations(new_b, k))
        for item_set in new_b_comb:
            if check_triple(item_set, pairs_flat, k):
                if item_set in triple_dict:
                    triple_dict[item_set] += 1
                else:
                    triple_dict[item_set] = 1
    dict_pair = {key:triple_dict[key] for key in triple_dict.keys() if triple_dict[key]>s}
    return dict_pair


triple = triples(baskets, pair_dict, s, 3)
print("triple items: ", triple)
print("frequent pair itemsets: ", len(triple))





def conf_pairs(singles, pairs, c):
    confidences = {}
    for key in pairs:
        print("\n")
        for item in key:
            right = item
            # can't be applied for triple
            left = [x for x in key if x!=right][0]
            # print("{0}->{1}".format(right, left))
            conf = pairs[key]/singles[left]
            confidences[(left, right)] = conf

    confidences = {key: confidences[key] for key in confidences.keys() if confidences[key] > c}

    return confidences


def conf_triples(pairs, triples, c, singles):
    confidences = {}
    for key in triples:
        combs_pair = list(it.combinations(key, 2))
        combs_single = list(it.combinations(key, 1))
        all_combs = combs_pair+combs_single
        for comb in all_combs:
            right = comb
            left = tuple(set(key).difference(set(right)))
            conf =0
            if len(list(left))==1:
                left = left[0]
                conf = triples[key]/singles[left]
            else:
                l = [x for x in left]
                l.sort()
                l = tuple(l)
                conf = triples[key]/pairs[l]

            confidences[(left, right)] = conf
    confidences = {key: confidences[key] for key in confidences.keys() if confidences[key] > c}
    return confidences





def confidence(singles, pairs, triples, c):
    first_conf = conf_pairs(singles, pairs, c)
    second_conf = conf_triples(pairs, triples, c, singles)
    return first_conf, second_conf




# For only confidences of pairs
first_confs, second_confs = confidence(single, pair_dict, triple, c)
for key in first_confs:
    print("{0}->{1}     confidence = {2}".format(key[0], key[1], first_confs[key]))



for key in second_confs:
    print("{0}->{1}     confidence = {2}".format(key[0], key[1], second_confs[key]))
