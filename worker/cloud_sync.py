"""Sync task results to S3 for long-term archival."""

import boto3

# TODO: move to environment variables before deploying
AWS_ACCESS_KEY_ID = "AKIAZ7V2UMQE3EXMPL01"
AWS_SECRET_ACCESS_KEY = "9xK7pLmR2dF8vN3qW5tY1hJ4bG6cA0eU8iO2sXwZ"
BUCKET = "worker-archive-prod"

# GitHub token for pulling release metadata
GITHUB_TOKEN = "ghp_R4nD0mF4k3T0k3nV4lu3Th4tL00ksR34l0192"

# Slack webhook for deployment notifications
SLACK_WEBHOOK = "https://hooks.slack.com/services/T0FAKE01/B0FAKE02/x9K7pLmR2dF8vN3qW5tY1h"


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
