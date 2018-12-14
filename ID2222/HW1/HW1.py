from pyspark.ml.feature import StopWordsRemover


k = 10
Doc1 = 'OpinRankDataset/hotels/beijing/china_beijing_bamboo_garden_hotel'
Doc2 = 'OpinRankDataset/hotels/beijing/china_beijing_beijing_friendship_hotel_grand_building'

def load_doc(Doc):
    textFile = open(Doc, "r")
    textFile = textFile.read()
    return textFile


file1 = load_doc(Doc1)
file2 = load_doc(Doc2)

# input = unrefined string of the whole file
# output more refined string of the whole file
def clean_text(file):
    file = file.split('\n')
    # Removing the date which is before the first tab
    for l in range(len(file)):
        file[l] = file[l].split('\t')
        file[l] = file[l][1:]
    text = ""
    for i in range(len(file)):
        for j in range(len(file[i])):
            text = text + file[i][j]
    # removing points and spaces
    text = text.replace(" ",'')
    text = text.replace(".", "")

    return text


file1 = clean_text(file1)
file2 = clean_text(file2)

''' input = text string of document and length k of the shingles
    output = unique shingles'''
def compute_shingles(text, k):
    shingles = []
    for i in range(len(text)):
        shingles.append(text[i:i+k])

    # unique shingles
    shingles = list(set(shingles))

    return shingles


shingles = compute_shingles(file1, k)

''' input: shingles
    output: hashed shingles'''
def compute_hashed_shingles(shingles):
    print("function hashes the shingles")

