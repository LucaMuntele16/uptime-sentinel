import os
import pytest
from app.checker.storage import put_result, get_table

#skip all tests in this file if local dynamodb endpoint is not configured
pytestmark = pytest.mark.skipif(
    not os.environ.get("DYNAMODB_ENDPOINT"),
    reason = "DynamoDB Local is not on",
)
def test_write_and_read():
    #write a sample check result to the local database
    result = {"name": "test-site", "status": "UP", "latency_ms":120.5}
    put_result(result)
    
    #query by partition key using a placeholder (:s) for safe value binding
    table = get_table()
    response = table.query(
        KeyConditionExpression="site = :s",
        ExpressionAttributeValues={":s": "test-site"},
    )
    
    # verify at least one record exists and the latest one has the right status
    assert response["Count"] >= 1
    assert response["Items"][-1]["status"] == "UP"