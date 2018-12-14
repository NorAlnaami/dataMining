from pyspark.sql import SparkSession
from pyspark import SparkContext,SparkConf
import os
from pyspark.sql.types import StringType


sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))


os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/local/bin/python3"
os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3"

# file= open("T10I4D100K.dat", 'r').read().replace("\n", "")


spark = SparkSession.builder.master("local").appName("a priori")\
.config("spark.some.config.option", "some-value")\
.getOrCreate()

df = spark.read.text("T10I4D100K.dat")

print(df.filter(df.value.contains("945")).count())
df.show()


# 1% of the data
# s =