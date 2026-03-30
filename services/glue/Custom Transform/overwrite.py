def Overwrite(glueContext, dfc) -> DynamicFrameCollection:
    
    import pandas as pd
    from awsglue.dynamicframe import DynamicFrame
    
    # DynamicFrame → Pandas → Spark DataFrame
    df = dfc.select(list(dfc.keys())[0]).toDF()
    pandas_df = df.toPandas()
    
    import datetime
    partition_date = datetime.datetime.now().strftime('%Y-%m-%d')
    pandas_df['partition_date'] = partition_date
    
    spark_df = glueContext.spark_session.createDataFrame(pandas_df)
    
    # 書き込み（パーティション指定）
    spark_df.write.mode("overwrite")\
      .option("partitionOverwriteMode", "dynamic")\
      .partitionBy("partition_date")\
      .parquet('s3://sample-bucket/key/')
    

    # # 書き込み (csv, 一つのファイルに)
    # spark_df.coalesce(1).write \
    # .mode("overwrite") \
    # .option("header", "true") \
    # .csv('s3://sample-bucket/key/')
        
    # DynamicFrameに戻す（必要なら）
    dynamic_frame = DynamicFrame.fromDF(spark_df, glueContext, "dynamic_frame")
    return DynamicFrameCollection({"CustomTransform0": dynamic_frame}, glueContext)
    