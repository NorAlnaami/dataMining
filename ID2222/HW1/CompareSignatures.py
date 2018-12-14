import minHashing
import numpy as np


def similarity(vec1, vec2):
    diff = vec1 - vec2
    diff = len(diff) - np.count_nonzero(diff)
    return diff/len(vec1)


def eachDoc(sig):
    allSim = []
    comparedDocs = {}
    for doc in range(sig.shape[1]):
        for secDoc in range(doc+1 ,sig.shape[1]):
            a = (doc, secDoc)
            comparedDocs[a] = similarity(sig[:,doc], sig[:, secDoc])
            allSim.append(similarity(sig[:,doc], sig[:, secDoc]))
    return allSim, comparedDocs

# sig = minHashing.sig
# allSim, cmpDocs = eachDoc(sig)
# # print(allSim)
# print(cmpDocs)