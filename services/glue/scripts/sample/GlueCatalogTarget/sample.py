import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

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

# Script generated for node AWS Glue Data Catalog_m_item
AWSGlueDataCatalog_m_item_node1762739797247 = glueContext.create_dynamic_frame.from_catalog(database="oyaizu", table_name="master_m_item", transformation_ctx="AWSGlueDataCatalog_m_item_node1762739797247")

# Script generated for node AWS Glue Data Catalog_m_category
AWSGlueDataCatalog_m_category_node1762740097207 = glueContext.create_dynamic_frame.from_catalog(database="oyaizu", table_name="master_m_category", transformation_ctx="AWSGlueDataCatalog_m_category_node1762740097207")

# Script generated for node SQL Query
SqlQuery0 = '''
select * from table1 as A
inner join table2 as B on A.category_id = B.category_id
'''
SQLQuery_node1762739847726 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"table1":AWSGlueDataCatalog_m_item_node1762739797247, "table2":AWSGlueDataCatalog_m_category_node1762740097207}, transformation_ctx = "SQLQuery_node1762739847726")

# Script generated for node Change Schema
ChangeSchema_node1762740009628 = ApplyMapping.apply(frame=SQLQuery_node1762739847726, mappings=[("category_id", "string", "category_id", "long"), ("item_id", "string", "item_id", "long"), ("category_name", "string", "category_name", "string"), ("item_name", "string", "item_name", "string"), ("partition_date", "string", "partition_date", "string")], transformation_ctx="ChangeSchema_node1762740009628")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1762741462394 = glueContext.write_dynamic_frame.from_catalog(frame=ChangeSchema_node1762740009628, database="oyaizu", table_name="sample", additional_options={"partitionKeys": ["partition_date"]}, transformation_ctx="AWSGlueDataCatalog_node1762741462394")

job.commit()