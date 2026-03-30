def DynamodbWrite (glueContext, dfc) -> DynamicFrameCollection:
    import pandas as pd
    import datetime
    from awsglue.dynamicframe import DynamicFrame
    
    # DynamicFrame → Pandas → Spark DataFrame
    df = dfc.select(list(dfc.keys())[0]).toDF()
    pandas_df = df.toPandas()
    
    # Pandas で列（updated_at）を追加（ISO 8601 文字列）
    pandas_df["updated_at"] = datetime.datetime.now().isoformat()
    
    # Pandas -> Spark DataFrame に戻す
    spark_df = glueContext.spark_session.createDataFrame(pandas_df)
    
    # Spark DataFrame -> DynamicFrame に変換（DynamoDB シンクは DynamicFrame を受け付ける）
    dynamic_frame = DynamicFrame.fromDF(spark_df, glueContext, "dynamic_frame")
    
    # DynamoDB に書き込み（DynamicFrame を渡す）
    glueContext.write_dynamic_frame_from_options(
        frame=dynamic_frame,
        connection_type="dynamodb",
        connection_options={
            "dynamodb.output.tableName": "DailyInventory",
            "dynamodb.throughput.write.percent": "1.0"
        }
    )
    
    # Glue Studio の規約：DynamicFrameCollection を返す（第2引数 glueContext は必須）
    return DynamicFrameCollection({"CustomTransform0": dynamic_frame}, glueContext)
    