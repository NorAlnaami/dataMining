import HW1Framework
import jaccardS
import numpy as np
import random
import math


def minhash(DocPath, DocPath1, DocPath2, DocPath3, DocPath4):
    nrDocs = 5
    signature_nr = 200
    k = 10
    #prime nr slightly larger than nr of unique shingles of all docs
    c = 30211

    '''Testing Jaccard'''
    setA = HW1Framework.shinglingClass(DocPath, k)
    setB = HW1Framework.shinglingClass(DocPath1, k)
    setC = HW1Framework.shinglingClass(DocPath2, k)
    setD = HW1Framework.shinglingClass(DocPath3, k)
    setE = HW1Framework.shinglingClass(DocPath4, k)


    Element = setA|setB|setC|setD|setE

    charact_m = np.zeros((len(Element), nrDocs))
    lists_of_sets = np.asarray([list(setA), list(setB), list(setC), list(setD), list(setE)])
    Element = list(Element)
    # print("len: ",len(Element))

    def searchList(lists_of_sets, Element, charact_m):
        for col in range(len(lists_of_sets)):
            for row in range(len(Element)):
                if Element[row] in lists_of_sets[col]:
                    charact_m[row][col] = 1
        return charact_m


    charact_m = searchList(lists_of_sets, Element, charact_m)
    # print(charact_m)



    def init_permute_values(charact_m, signature_nr, c):
        primes = np.repeat(c, signature_nr)
        a_s = [random.randint(1, charact_m.shape[0]) for i in range(signature_nr)]
        b_s = [random.randint(1, charact_m.shape[0]) for i in range(signature_nr)]

        hashes = np.asarray([a_s, b_s, primes]).transpose()
        return hashes

    def hash_fun(a, b, prime, x):
        return ((a*x)+b)%prime

    hashes = np.asarray(init_permute_values(charact_m, signature_nr, c))
    # print(hashes)


    def compute_sig(charact_m, hashes, signature_nr):
        M = np.ones((signature_nr, charact_m.shape[1]))*math.inf
        permuts = np.zeros((signature_nr, charact_m.shape[0]))
        for row in range(charact_m.shape[0]):
            for i in range(hashes.shape[0]):
                permuts[i][row] = hash_fun(hashes[i][0], hashes[i][1], hashes[i][2], row)
            for col in range(charact_m.shape[1]):
                if charact_m[row][col]==1:
                    for i in range(hashes.shape[0]):
                        if permuts[i][row]< M[i][col]:
                            M[i][col]= permuts[i][row]
        # print(permuts)
        return M

    sig = compute_sig(charact_m, hashes, signature_nr)
    # print('minhash signatures for book example: ')
    # print(sig)

    return sig




DocPath = "OpinosisDataset1.0/topics/screen_garmin_nuvi_255W_gps.txt.data"
DocPath1 = "OpinosisDataset1.0/topics/screen_ipod_nano_8gb.txt.data"
DocPath2 = "OpinosisDataset1.0/topics/screen_netbook_1005ha.txt.data"
DocPath3 = "OpinosisDataset1.0/topics/video_ipod_nano_8gb.txt.data"
DocPath4 = "OpinosisDataset1.0/topics/voice_garmin_nuvi_255W_gps.txt.data"




sig = minhash(DocPath, DocPath1, DocPath2, DocPath3, DocPath4)
# print(sig)