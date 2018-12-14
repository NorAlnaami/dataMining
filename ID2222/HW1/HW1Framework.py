from pyspark.ml.feature import StopWordsRemover
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import string
import os
from pyspark.ml.feature import NGram
from pyspark.ml.feature import FeatureHasher
from pyspark.ml.feature import CountVectorizer
import numpy as np
import hashlib


os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/local/bin/python3"
os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3"

#starting a spark session
spark = SparkSession \
    .builder \
    .appName("shingling") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# k = 10
# DocPath = "dataset-CalheirosMoroRita-2017.csv"

def shinglingClass(DocPath,k):

    ''' method load the external data
        input: file path
        output: data frame'''
    def load_Data(path):
        # df = spark.read \
        #     .option("inferSchema", "true") \
        #     .option("header", "true") \
        #     .load(path, format="csv", sep= "\n")

        df = spark.read.text(path)
        df = df.withColumnRenamed("value", "Review")

        doc = open(path, 'r')
        doc_str = doc.read().replace("\n", '')
        doc_str = [doc_str.lower()]
        df =spark.createDataFrame(doc_str, StringType())
        df = df.withColumnRenamed("value", "Review")
        return df

    df = load_Data(DocPath)
    # df.show(truncate= False)


    ''' method removing punctuation
        input: list (element of scheme)
        output: list with removed punctuation'''
    def remove_punct(line):
        # line = [''.join(c for c in line if c not in string.punctuation) ]#for s in line]
        # line = [s.strip() for s in line]
        new = ""
        for s in line:
            for c in s:
                if c not in string.punctuation:
                    new += c
        line = new
        line = line.strip()
        # line = line.replace(" ", "")
        # line = " ".join(line)

        return line


    ''' calling spark user defined function '''
    fun_removePunct = spark.udf.register("removePunct",remove_punct,StringType())
    tokenized = df.withColumn("Review_punct", fun_removePunct(df.Review))


    ''' method tokenizes the data meaning it put each word of sentence as an element of a list
        input: data frame
        output: tokenized rows'''
    def tokenizer(doc):
        tkn = Tokenizer().setInputCol("Review_punct").setOutputCol("Review_Tokenized")
        tokenized = tkn.transform(doc.select("Review_punct"))
        return tokenized


    tokenized = tokenizer(tokenized)



    ''' method removes stop words form the text given a tokenized data
        input: tokenized schema
        output: schema with removed stopwords'''
    def clean(tokenized):
        englishStopWords = StopWordsRemover.loadDefaultStopWords("english")
        stop_words = StopWordsRemover(outputCol="stopword_removed") \
            .setStopWords(englishStopWords) \
            .setInputCol("Review_Tokenized")
        SW_Re = stop_words.transform(tokenized)

        return SW_Re


    SW_Re = clean(tokenized)
    # SW_Re.show(truncate = False)


    def char_rep(line):
        line = [s.replace(" ", "") for s in line]
        line = ["".join(c for c in s) for s in line]

        line = "".join(line)
        new =""

        for c in line:
            c += " "
            new += c
        line = new

        return line

    fun_char = spark.udf.register("characters", char_rep, StringType())
    chars_represented = SW_Re.withColumn("charDest", fun_char(SW_Re.stopword_removed))


    def tokenizer(doc):
        tkn = Tokenizer().setInputCol("charDest").setOutputCol("final_tokenization")
        tokenized = tkn.transform(doc.select("charDest"))
        return tokenized


    SW_Re = tokenizer(chars_represented)
    # SW_Re.show(truncate=False)


    ''' dropping unncessary columns'''
    final_data = SW_Re.drop("charDest")
    final_data = final_data.withColumnRenamed("final_tokenization", "Review")
    # final_data.show(truncate=False)

    nGram = NGram(n=k, inputCol="Review", outputCol="shingles")
    nGramTransform = nGram.transform(final_data)

    def char_space(line):
        line = [s.replace(" ", "") for s in line]

        return line

    fun_spaces = spark.udf.register("spaces", char_space, StringType())
    chars_spaces = nGramTransform.withColumn("finalShingles", fun_spaces(nGramTransform.shingles))
    # chars_spaces.show(truncate = False)


    def tokenizer(doc):
        tkn = Tokenizer().setInputCol("finalShingles").setOutputCol("final_shingles")
        tokenized = tkn.transform(doc.select("finalShingles"))
        return tokenized

    chars_spaces = tokenizer(chars_spaces)
    # chars_spaces.show(truncate = False)


    cv = CountVectorizer()\
        .setInputCol("final_shingles")\
        .setOutputCol("hashed_shingles")\
        .setVocabSize(500)\

    fittedCvModel = cv.fit(chars_spaces)
    fittedCv = fittedCvModel.transform(chars_spaces)
    # fittedCv.show(truncate=False)

    shingles_list = chars_spaces.select("finalShingles").rdd.flatMap(lambda x: x).collect()


    def hashing(shingles_list):
        new = ""
        for e in shingles_list:
            for S in e:
                if S != ']' and S != '[' and S != ' ':
                    new += S
                if S == ']':
                    new += ","

        shingles_list = new.split(sep=',')
        shingles_set = set(shingles_list)
        shingles_set.discard('')

        hashed_set = {hash(x) for x in shingles_set}
        return shingles_list, hashed_set

    shingles_list , hashing_set = hashing(shingles_list)


    return hashing_set


''' Testing shingles'''
# DocPath = "OpinosisDataset1.0/topics/battery-life_ipod_nano_8gb.txt.data"
# k = 10
# shingles_list, shingles = shinglingClass(DocPath,k)
# new = ""
# for e in shingles_list:
#     for S in e:
#         if S != ']' and S != '[' and S != ' ':
#             new += S
#         if S==']':
#             new += ","
#
# shingles_list = new.split(sep=',')
# shingles_set = set(shingles_list)
# shingles_set.discard('')
#
# # hashing = hashlib.md5()
# hashed_set = {hash(x) for x in shingles_set}


# shingles_list = list(shingles_set)

# def hashShingles(shingles_list):
#     unique_shingles = np.unique(np.asarray(shingles_list))
#     # Hashed set
#     shingle_set = {}
#     hashed_set = dict(enumerate(unique_shingles))
#     hashed_set = {v: k for k, v in hashed_set.items()}
#     print(hashed_set)
#     for elem in shingles_list:
#         if elem in hashed_set:
#             shingle_set[hashed_set.get(elem)] = elem
#     print(shingle_set)



# hashShingles(shingles_list)
