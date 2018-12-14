import minHashing
import numpy as np
import CompareSignatures

# Divide the signature matrix into b bands, each band having r rows

signature = minHashing.sig
n = signature.shape[0]
b = 10
r = int(n/b)
print("n: ", n)
print("b: ", b)
print("r: ", r)
print("signature: ", signature)

def initBand(b,r, signature):
    bands = []
    counter = 0
    row = r
    for band in range(b):

        sig_rows = signature[counter:r]
        bands.append(sig_rows)
        counter = r
        r +=row
    return bands


bands = initBand(b, r, signature)

# For each band, hash its portion of each column to a hash table with k buckets
#Candidate column pairs are those that hash to the same bucket for at least 1 band


def check_each_band(band, b, all_buckets):
    # all_buckets = {}
    for col in range(band.shape[1]):
        for other_col in range(col+1, band.shape[1]):
            if CompareSignatures.similarity(band[:, col], band[:, other_col]) >= 0.07:
                if (col, other_col) not in all_buckets:
                    all_buckets[(col, other_col)] = CompareSignatures.similarity(band[:, col], band[:, other_col])
    return all_buckets

def go_through_bands(bands):
    all_buckets = {}
    for b in range(len(bands)):
        all_buckets = check_each_band(bands[b], b, all_buckets)
    return all_buckets

bucket_final = go_through_bands(bands)
print("Two pair of documents in tuple and the value is band number where the candidate pairs were found: ")
print(bucket_final)

#Tune b and r to catch most similar pairs but few non similar pairs


