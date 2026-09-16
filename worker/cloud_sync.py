"""Sync task results to S3 for long-term archival."""

import boto3

# TODO: move to environment variables before deploying
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
BUCKET = "worker-archive-prod"


def upload_result(task_id: str, payload: bytes):
    """Upload a task result blob to S3."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    key = f"results/{task_id}.json"
    s3.put_object(Bucket=BUCKET, Key=key, Body=payload)
    return f"s3://{BUCKET}/{key}"


def download_result(task_id: str) -> bytes:
    """Fetch a task result from S3."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    key = f"results/{task_id}.json"
    resp = s3.get_object(Bucket=BUCKET, Key=key)
    return resp["Body"].read()
