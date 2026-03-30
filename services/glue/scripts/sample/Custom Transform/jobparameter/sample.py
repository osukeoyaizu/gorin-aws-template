import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame

# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
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

    # フィルタ処理
    pandas_df = pandas_df.loc[pandas_df['partition_date'] == filter_date]


    # 空データ対応
    if pandas_df.empty:
        empty_df = glueContext.spark_session.createDataFrame([], df.schema)
        dynamic_frame = DynamicFrame.fromDF(empty_df, glueContext, "dynamic_frame")
        return DynamicFrameCollection({"CustomTransform0": dynamic_frame}, glueContext)


    # Pandas → Spark → DynamicFrame
    spark_df = glueContext.spark_session.createDataFrame(pandas_df)
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

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

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

# Script generated for node Select From Collection
SelectFromCollection_node1762753164962 = SelectFromCollection.apply(dfc=CustomTransform_node1762743231358, key=list(CustomTransform_node1762743231358.keys())[0], transformation_ctx="SelectFromCollection_node1762753164962")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SelectFromCollection_node1762753164962, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1762753030650", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1762753171779 = glueContext.write_dynamic_frame.from_options(frame=SelectFromCollection_node1762753164962, connection_type="s3", format="glueparquet", connection_options={"path": "s3://oyaizu-datalake/sample/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1762753171779")

job.commit()