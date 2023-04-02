from pyspark.sql import SparkSession, DataFrame
import os

class PriceAnalyzer:
    def analyze(self, df: DataFrame) -> None:
        df.printSchema()
        df.show()

    def consume_product_infos(self, topic_name: str, kafka_broker: str, spark_master) -> None:
        spark = (
            SparkSession.builder.appName("PriceAnalyzer")
            .master(spark_master)
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", kafka_broker)
            .option("subscribe", topic_name)
            .option("startingOffsets", "latest")
            .load()
        )

        self.analyze(df)
        