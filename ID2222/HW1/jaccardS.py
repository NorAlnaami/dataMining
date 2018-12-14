import HW1Framework




'''A set is a collection which is unordered and unindexed. In Python sets are written with curly brackets.
    example: thisset = {"apple", "banana", "cherry"}
'''
def jaccard(setA, setB):
    intersection = len(setA.intersection(setB))
    union = len(setA.union(setB))
    return intersection/union

# DocPath = "OpinosisDataset1.0/topics/screen_garmin_nuvi_255W_gps.txt.data"
# DocPath1 = "OpinosisDataset1.0/topics/screen_ipod_nano_8gb.txt.data"
# DocPath2 = "OpinosisDataset1.0/topics/screen_netbook_1005ha.txt.data"
# DocPath3 = "OpinosisDataset1.0/topics/video_ipod_nano_8gb.txt.data"
# DocPath4 = "OpinosisDataset1.0/topics/voice_garmin_nuvi_255W_gps.txt.data"
#
# k = 10
#
# setA = HW1Framework.shinglingClass(DocPath, k)
# setB = HW1Framework.shinglingClass(DocPath1, k)
# setC = HW1Framework.shinglingClass(DocPath2, k)
# setD = HW1Framework.shinglingClass(DocPath3, k)
# setE = HW1Framework.shinglingClass(DocPath4, k)
#
# print("Jaccard similarity between doc0 and doc1: ")
# print(jaccard(setA, setB))
# print("Jaccard similarity between doc0 and doc2: ")
# print(jaccard(setA, setC))
# print("Jaccard similarity between doc0 and doc3: ")
# print(jaccard(setA, setD))
# print("Jaccard similarity between doc0 and doc4: ")
# print(jaccard(setA, setE))
#
#
# print("Jaccard similarity between doc1 and doc2: ")
# print(jaccard(setB, setC))
# print("Jaccard similarity between doc1 and doc3: ")
# print(jaccard(setB, setD))
# print("Jaccard similarity between doc1 and doc4: ")
# print(jaccard(setB, setE))
#
#
#
# print("Jaccard similarity between doc2 and doc3: ")
# print(jaccard(setC, setD))
# print("Jaccard similarity between doc2 and doc4: ")
# print(jaccard(setC, setE))
#
# print("Jaccard similarity between doc3 and doc4: ")
# print(jaccard(setD, setE))
