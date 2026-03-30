from pyathena import connect
import pandas as pd
import boto3
import json
# set parameter
session = boto3.Session(profile_name=None)
REGION = session.region_name
ATHENA_STAGING = 's3://<BUCKET_NAME>/<KEY>/' #クエリの結果の場所のS3パス

def lambda_handler(event, context):
    # make connection
    conn = connect(s3_staging_dir=ATHENA_STAGING,
                region_name=REGION)
    
    query = """
    SELECT * 
    FROM YourDatabase.YourTable 
    LIMIT 8;
    """

    # query
    df = pd.read_sql(query, conn)
    print(df)


    return {
        'statusCode': 200,
        'body': json.dumps('sample')
    }
