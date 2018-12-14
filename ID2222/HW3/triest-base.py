import csv
from random import choices
import random
import numpy as np
import matplotlib.pyplot as plt
path = "contiguous-usa/out.contiguous-usa"
file = open(path)



# nr of max edges allowed
# M = 90
m = list(range(6,108, 5))

# estimation of global triangles
# counter = 0
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

def UpdateCounters(operation, candidate,i):
    neightbours = neight(candidate[0]).intersection(neight(candidate[1]))
    global counter
    global tau
    for e in neightbours:
        if operation == '+':
            counter[i] += 1
            if e in tau.keys():
                tau[int(e)] += 1
            else:
                tau[int(e)] = 1
        elif operation == '-':
            counter[i] -= 1
            if e in tau.keys():
                tau[int(e)] -= 1
            else:
                tau[int(e)] = 0


def SampleEdge(stream, t, M, i):
    if t<=M:
        return True
    elif FlipBiasedCoin(M/t) == ['H']:
        candidate = list(S)[random.randrange(M)]
        S.remove(candidate)
        UpdateCounters('-', candidate, i)
        return True
    return False

i = 0
for M in m:
    for row in data:
        t += 1
        if SampleEdge(row,t, M, i):
            S.add(row)
            UpdateCounters('+', row, i)

    S = set()
    tau = {}
    t = 0
    S_neight = {}
    i +=1


plt.plot(m, counter, 'r')
plt.title('Trièst-base')
plt.xlabel('M')
plt.ylabel("Triangle count")
plt.show()
print(counter)
