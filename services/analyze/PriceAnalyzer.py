from pyspark.sql import SparkSession
import os

class PriceAnalyzer:
    def analyze(self, topic_name: str) -> None:
        spark = (
            SparkSession.builder.appName("PriceAnalyzer")
            .master("local[*]")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", os.environ.get('KAFKA_BOOTSTRAP_SERVER'))
            .option("subscribe", topic_name)
            .option("startingOffsets", "latest")
            .load()
        )

        df.printSchema()
        df.show()


        # TODO: Implement
        pass