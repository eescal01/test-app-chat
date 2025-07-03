import json


def lambda_handler(event, context):
    """
    Basic test Lambda handler to verify the infrastructure is working.
    """
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": "✅ Test Lambda executed successfully.",
            "input": event
        })
    }
