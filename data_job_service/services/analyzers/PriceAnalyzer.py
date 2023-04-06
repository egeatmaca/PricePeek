from pyspark.sql import SparkSession, DataFrame
import os

class PriceAnalyzer:
    def analyze(self, df: DataFrame) -> None:
        df.printSchema()
        df.writeStream.format("console").start().awaitTermination()
        print("Finished analyzing")

    def consume_product_infos(self, topic_name: str, kafka_broker: str, spark_master) -> None:
        topic_name = topic_name.replace(' ', '_')

        spark = (
            SparkSession.builder.appName("PriceAnalyzer")
            .master(spark_master)
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
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
        