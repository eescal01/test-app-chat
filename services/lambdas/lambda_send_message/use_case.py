import os
import boto3
import contextlib
import json
from datetime import datetime
from models import SendMessage

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
region = os.environ.get("REGION", "us-east-1")
ws_api_id = os.environ["WS_API_ID"]
endpoint_url = f"https://{ws_api_id}.execute-api.{region}.amazonaws.com/prod"
apigw = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)


def handle_send_message(event, context):
    body = json.loads(event["body"])
    try:
        msg = SendMessage(**body)
    except Exception as e:
        return {"statusCode": 400, "body": str(e)}

    now = datetime.utcnow().isoformat()
    # Guarda el mensaje en DynamoDB
    table.put_item(Item={
        "PK": f"CHAT#{msg.chat_id}",
        "SK": f"MSG#{now}",
        "from": msg.from_user,
        "to": msg.to_user,
        "content": msg.content,
        "Type": "Message",
        "timestamp": now
    })
    # Actualiza referencia de chat en ambos usuarios
    table.put_item(Item={
        "PK": f"USER#{msg.from_user}",
        "SK": f"CHAT#{msg.chat_id}",
        "lastUpdated": now
    })
    table.put_item(Item={
        "PK": f"USER#{msg.to_user}",
        "SK": f"CHAT#{msg.chat_id}",
        "lastUpdated": now
    })
    # Busca el connectionId del destinatario
    resp = table.get_item(Key={"PK": f"USER#{msg.to_user}", "SK": "CONNECTION"})
    if "Item" in resp and "connectionId" in resp["Item"]:
        connection_id = resp["Item"]["connectionId"]
        with contextlib.suppress(apigw.exceptions.GoneException):
            apigw.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps({
                    "chat_id": msg.chat_id,
                    "from": msg.from_user,
                    "content": msg.content,
                    "timestamp": now
                })
            )

    # Opcional: confirmar al emisor
    return {"statusCode": 200, "body": "Message sent"}
