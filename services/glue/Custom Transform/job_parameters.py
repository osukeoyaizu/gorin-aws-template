# job parameter を取得して使用する

def GetJobParameter (glueContext, dfc) -> DynamicFrameCollection:
    
    import sys
    from awsglue.dynamicframe import DynamicFrame
    import datetime
    import pandas as pd
    
    # DynamicFrame → Pandas DataFrame
    df = dfc.select(list(dfc.keys())[0]).toDF()
    pandas_df = df.toPandas()
    
    # 今日の日付をデフォルト値に設定
    filter_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    # sys.argvから値を取得（なければデフォルト）
    if '--filter_date' in sys.argv:
        filter_date = sys.argv[sys.argv.index('--filter_date') + 1]
    
    # 日付を分割
    partition_0, partition_1, partition_2 = filter_date.split('-')
    
    # フィルタ処理
    pandas_df = pandas_df.loc[
        (pandas_df['partition_0'].astype(str) == partition_0) &
        (pandas_df['partition_1'].astype(str) == partition_1) &
        (pandas_df['partition_2'].astype(str) == partition_2)
    ]
    
    # Pandas → Spark → DynamicFrame
    spark_df = glueContext.spark_session.createDataFrame(pandas_df)
    dynamic_frame = DynamicFrame.fromDF(spark_df, glueContext, "dynamic_frame")
    
    return DynamicFrameCollection({"CustomTransform0": dynamic_frame}, glueContext)
    