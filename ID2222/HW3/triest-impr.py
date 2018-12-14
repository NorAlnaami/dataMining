import csv
from random import choices
import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

random.seed(3)
path = "contiguous-usa/out.contiguous-usa"
file = open(path)



# nr of max edges allowed
# M = 107
m = list(range(6,108, 10))
# print(m)
# estimation of global triangles
counter = np.zeros((len(m)))

# local triangles, destroyed if they have a value of 0
tau = {}

# Edge sample
S = set()

# time for the stream
t = 0

# S in dict
S_neight = {}

#TRIEST algorithm use a space of O(M) space



def read_stream(file):
    # stream given as list
    arr = []

    with file as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\n")
        headers = next(tsvreader)
        headers = next(tsvreader)
        for row in tsvreader:
            e = tuple(row[0].split())
            arr.append(e)
        return arr

data = read_stream(file)

def FlipBiasedCoin(val):
    coin = choices('HT', cum_weights=(val, 1), k=1)
    return coin

#finds all vertices (neighbours) to a given node
def neight(node):
    neights = set()
    for tuple_ in S:
        if tuple_[0]==node:
            neights.add(tuple_[1])
        elif tuple_[1]==node:
            neights.add(tuple_[0])

    return neights

def UpdateCounters(operation, candidate, M, i):
    neightbours = neight(candidate[0]).intersection(neight(candidate[1]))
    global counter
    global tau
    global t
    # global M
    # max{1,(t − 1)(t − 2)/(M(M − 1))}
    value = max(1.0, ((t-1)*(t-2))/(M*(M-1)))
    for e in neightbours:
        if operation == '+':
            counter[i] += value

            if e in tau.keys():
                tau[int(e)] += value
            else:
                tau[int(e)] = value



def SampleEdge(stream, t, M):
    if t<=M:
        return True
    elif FlipBiasedCoin(M/t) == ['H']:
        candidate = list(S)[random.randrange(M)]
        S.remove(candidate)
        return True
    return False


i = 0
for M in tqdm(m):
    for row in tqdm(data):
        t += 1
        UpdateCounters('+', row, M, i)
        if SampleEdge(row,t, M):
            S.add(row)
    S = set()
    tau = {}
    t = 0
    S_neight = {}
    i +=1

plt.plot(m, counter, 'g')
plt.xlabel('M')
plt.ylabel('Triangle count')
plt.title('Trièst-impr')
plt.show()
# print(counter)
