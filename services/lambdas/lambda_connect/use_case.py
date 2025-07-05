import boto3
import os
from datetime import datetime, timedelta

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handle_connect(event, context):
    connection_id = event["requestContext"]["connectionId"]
    # Supón que pasas el user_id en el querystring (por seguridad puedes usar JWT en producción)
    params = event.get("queryStringParameters") or {}
    user_id = params.get("user_id")
    if not user_id:
        return {"statusCode": 401, "body": "Missing user_id"}

    # Guarda el connectionId en DynamoDB
    table.put_item(Item={
        "PK": f"USER#{user_id}",
        "SK": "CONNECTION",
        "connectionId": connection_id
    })

    # Marca como online (presencia con TTL, 1 min ejemplo)
    ttl = int((datetime.utcnow() + timedelta(minutes=1)).timestamp())
    table.put_item(Item={
        "PK": f"USER#{user_id}",
        "SK": f"ACTIVE#{datetime.utcnow().isoformat()}",
        "ttl": ttl
    })

    return {"statusCode": 200, "body": "Connected"}
