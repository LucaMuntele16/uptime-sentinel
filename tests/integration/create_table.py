import os
import boto3

endpoint = os.environ.get("DYNAMODB_ENDPOINT", "http://localhost:8000")
dynamodb = boto3.client("dynamodb", endpoint_url = endpoint, region_name="eu-central-1")

dynamodb.create_table(
    TableName="uptime-sentinel",
    KeySchema=[
        {"AttributeName": "site", "KeyType":"HASH"},
        {"AttributeName": "timestamp", "KeyType":"RANGE"}
    ],
    AttributeDefinitions=[
        {"AttributeName": "site", "AttributeType" : "S"},
        {"AttributeName": "timestamp", "AttributeType" : "S"}
    ],
    BillingMode="PAY_PER_REQUEST",
)
print("Table created.")