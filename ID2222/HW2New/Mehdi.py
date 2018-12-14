import math
import itertools
import time

def parseData ():
	data = {}
	baskets = []
	for line in open ("T10I4D100K.dat", 'r'):
		temp = line.rstrip().split(" ")
		basket = []
		for item in temp:
			item = int(item)
			basket.append(item)
			key = tuple ([item])
			if key in data:
				data[key] += 1
			else: 
				data[key] = 1

		baskets.append(basket)
			
	s = int (0.01 * len (baskets))

	for k in list(data):
		if data[k] < s:
			del data[k]

	
	print ("Support threshold is 1%: " + str(s))

	return data, baskets, s

# data, baskets, s = parseData()


# Returns a set of unique singletons in L_k
def getNarrowedL1 (prevLset):
	items = set([])
	for key in prevLset:
		for val in key:
			items.add(val)

	return items

# Checks if all combinations (k-1-tuples) of a k-tuple exist i L_(k-1)
def checkCandidate (element, prevLset, k):
	combinations = itertools.combinations (list(element), k-1)
	for key in combinations:
		if key not in prevLset:
			return False
	return True



def getLset (prevLset, baskets, s, k):
	newLset = {}
	L1 = getNarrowedL1(prevLset.keys())


	for basket in baskets:
		#removed L1 elemments from basket
		#Get all items from basket that are in L1
		valid_basket = list(L1.intersection (basket))
		valid_basket.sort()
		print(valid_basket)

		# Get all candidates from the current basket
		candidates = list(itertools.combinations (valid_basket, k))

		for key in candidates:
			# Check if all k-1-tuples of the candidate exist in L_(k-1)
			if checkCandidate (key, prevLset, k):
				if key in newLset:
					newLset[key] += 1
				else:
					newLset[key] = 1

	# Prune the valid candidates
	for key in newLset.keys():
		if newLset[key] < s:
			del newLset[key]

	return newLset
# getLset(data, baskets, s, 2)






def AprioriAlgo ():
	# Retrieve L1, the baskets and the support threshold
	L_1, baskets, s = parseData ()

	resultSet = [(1,)]
	Lset = L_1
	k = 2
	# Fetch higher order pruned Lsets until	there exists no more
	while (len(Lset) > 0):
		resultSet.append (Lset)
		print("k: ",k)
		Lset = getLset (Lset, baskets, s, k)
		k += 1

	return resultSet

AprioriAlgo()
# #---  END OF ASSIGNEMENT 1 -- NOW LETS FIND ASSOCIATION RULES ----
#
# def getConfidence (itemSets, s1, s2):
# 	union = list (set(s1) | set(s2))
# 	print("left: ",s1)
# 	print("right: ", s2)
# 	print(union)
# 	union.sort()
# 	union = tuple(union)
# 	conf = float(itemSets[len(union)][union]) / itemSets[len(s1)][s1]
#
# 	return conf
#
# def getAssociation (itemSets, k, c, associations):
# 	counter = 1
# 	while counter < k:
# 		for key in itemSets[k]:
# 			items = list(key)
# 			left = set(itertools.combinations(list(items), counter))
# 			items = set(items)
# 			for _tuple in left:
# 				right = items.symmetric_difference(_tuple)
# 				conf = getConfidence (itemSets, _tuple, right)
# 				if conf > c:
# 					associations[tuple([tuple(_tuple), tuple(right)])] = conf
#
# 		counter += 1
#
#
# def generateAssociations (itemSets, c):
# 	associations = {}
# 	length = len(itemSets)
# 	for k in range(2, length):
# 		getAssociation(itemSets, k, c, associations)
#
# 	return associations
#
# def printAssociations (associations):
# 	print ("")
# 	print ("Association rules are: \n")
# 	for key in associations:
# 		left = key[0]
# 		right = key[1]
# 		conf = associations[key]
# 		print(str(left)+" -> "+str(right)+" | With Confidency of: "+str(conf))
#
# 	print ("")
#
# def main ():
# 	c = 0.5
# 	start = time.time()
# 	results = AprioriAlgo ()
# 	end= time.time()
# 	print("time: ", end-start)
#
# 	for i in range (1, len(results)):
# 		print (str(i) +"-tuples Frequency: " + str(len(results[i])))
#
# 		# for key in _dict.keys():
# 		# 	print "Key: " + str(key) + " - Value: " + str(_dict[key])
#
# 	associations = generateAssociations (results, c)
# 	# printAssociations (associations)
#
#
# if __name__ == "__main__":
# 	main ()
