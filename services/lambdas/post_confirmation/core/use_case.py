import boto3
import os


class PostConfirmationUseCase:
    def __init__(self, user_attributes):
        self.user_attributes = user_attributes
        print(f"Initialized PostConfirmationUseCase with attributes: {user_attributes}")

        region = os.environ.get("AWS_REGION", "us-east-1")
        session = boto3.session.Session(region_name=region)
        self.dynamodb = session.resource("dynamodb")

        table_name = os.environ["TABLE_NAME"]
        self.table = self.dynamodb.Table(table_name)
        print(f"Connected to DynamoDB table: {table_name}")

    def execute(self):
        google_id = self.user_attributes.extract_google_id()
        item = {
            "PK": f"USER#{google_id}",
            "SK": "PROFILE",
            "name": self.user_attributes.name,
            "email": self.user_attributes.email,
            "avatar": self.user_attributes.picture,
            "googleId": google_id
        }

        print(f"Putting item into DynamoDB: {item}")
        self.table.put_item(Item=item)
        print("Item successfully stored in DynamoDB")
