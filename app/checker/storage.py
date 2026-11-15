import os
import boto3
import time
from decimal import Decimal
from datetime import datetime, timezone

TTL_DAYS = 7 # expire old records after 7 days so the database stays clean

def get_table():
    endpoint = os.environ.get("DYNAMODB_ENDPOINT") # grab the local docker url if set, otherwise boto3 defaults to real aws cloud
    table_name = os.environ.get("DYNAMODB_TABLE", "uptime-sentinel")
    
    # connect to dynamodb in the specified region
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url = endpoint,
        region_name = os.environ.get("AWS_DEFAULT_REGION", "eu-central-1")
    )
    # return a reference to our table (no network call happens yet)
    return dynamodb.Table(table_name)

def put_result(result):
    # use utc time so timestamps stay consistent regardless of server timezone
    now = datetime.now(timezone.utc)
    element = {
        "site":result["name"], # partition key (hash)
        "timestamp": now.isoformat(), # sort key (range) - iso format sorts chronologically as text
        "status" : result["status"],
        # dynamodb rejects floats, so convert to string first to avoid precision bugs
        "latency_ms": Decimal(str(result["latency_ms"])),
        # current unix timestamp in seconds + 7 days in seconds
        "ttl": int(time.time()) + TTL_DAYS * 24 * 3600 
    }
    # actually write the item to the database
    get_table().put_item(Item = element)