import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handle_disconnect(event, context):
    connection_id = event["requestContext"]["connectionId"]

    # 1. Recupera el user_id usando el PK secundario
    resp = table.get_item(Key={
        "PK": f"CONNECTION#{connection_id}",
        "SK": "PROFILE"
    })
    if "Item" in resp:
        user_id = resp["Item"]["user_id"]
        # 2. Borra el registro CONNECTION secundario
        table.delete_item(Key={
            "PK": f"CONNECTION#{connection_id}",
            "SK": "PROFILE"
        })
        # 3. Borra el registro CONNECTION principal del usuario
        table.delete_item(Key={
            "PK": f"USER#{user_id}",
            "SK": "CONNECTION"
        })
        # (Opcional) Aquí puedes también borrar los ítems de presencia ACTIVE#
        # usando query + batch_delete (opcional según tu lógica de presencia)

    return {"statusCode": 200, "body": "Disconnected"}
