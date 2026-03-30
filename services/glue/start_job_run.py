import os
import json
import boto3

glue = boto3.client("glue")

def start_glue_job(job_name, args)
    resp = glue.start_job_run(JobName=job_name, Arguments=args)
    job_run_id = resp["JobRunId"]
    return job_run_id


def lambda_handler(event, context):
    job_name = 'sample-job'
    args = {
        "--SAMPLE_1": "value1",
        "--SAMPLE_2": "value2" ,
    }

    job_run_id = start_glue_job(job_name = job_name, args=args)

    body = {
        "status": "OK",
        "message": f"Glue job started with REFERENCE_DATE={reference_date}",
        "job_run_id": job_run_id,
    }
    return {"statusCode": 200, "body": json.dumps(body, ensure_ascii=False)}