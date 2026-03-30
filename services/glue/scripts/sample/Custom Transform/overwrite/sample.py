import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame

# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    import pandas as pd
    from awsglue.dynamicframe import DynamicFrame

    # DynamicFrame → Pandas → Spark DataFrame
    df = dfc.select(list(dfc.keys())[0]).toDF()
    pandas_df = df.toPandas()

    # カラム順を揃える
    pandas_df = pandas_df.reindex(columns=[
        "category_id", "item_iditem_id", "category_name", "item_name", "partition_date"
    ])

    spark_df = glueContext.spark_session.createDataFrame(pandas_df)

    # 書き込み（パーティション指定）
    df.write.mode("overwrite")\
      .option("partitionOverwriteMode", "dynamic")\
      .partitionBy("partition_date")\
      .parquet('s3://oyaizu-datalake/sample/')
        
    # DynamicFrameに戻す（必要なら）
    dynamic_frame = DynamicFrame.fromDF(spark_df, glueContext, "dynamic_frame")
    return DynamicFrameCollection({"CustomTransform0": dynamic_frame}, glueContext)
def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node AWS Glue Data Catalog_m_category
AWSGlueDataCatalog_m_category_node1762740097207 = glueContext.create_dynamic_frame.from_catalog(database="oyaizu", table_name="master_m_category", transformation_ctx="AWSGlueDataCatalog_m_category_node1762740097207")

# Script generated for node AWS Glue Data Catalog_m_item
AWSGlueDataCatalog_m_item_node1762739797247 = glueContext.create_dynamic_frame.from_catalog(database="oyaizu", table_name="master_m_item", transformation_ctx="AWSGlueDataCatalog_m_item_node1762739797247")

# Script generated for node SQL Query
SqlQuery0 = '''
select * from table1 as A
inner join table2 as B on A.category_id = B.category_id
'''
SQLQuery_node1762739847726 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"table1":AWSGlueDataCatalog_m_item_node1762739797247, "table2":AWSGlueDataCatalog_m_category_node1762740097207}, transformation_ctx = "SQLQuery_node1762739847726")

# Script generated for node Change Schema
ChangeSchema_node1762740009628 = ApplyMapping.apply(frame=SQLQuery_node1762739847726, mappings=[("category_id", "string", "category_id", "long"), ("item_id", "string", "item_id", "long"), ("item_name", "string", "item_name", "string"), ("partition_date", "string", "partition_date", "string"), ("category_name", "string", "category_name", "string")], transformation_ctx="ChangeSchema_node1762740009628")

# Script generated for node Custom Transform
CustomTransform_node1762743231358 = MyTransform(glueContext, DynamicFrameCollection({"ChangeSchema_node1762740009628": ChangeSchema_node1762740009628}, glueContext))

job.commit()