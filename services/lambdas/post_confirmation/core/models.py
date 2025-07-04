from pydantic import BaseModel, Field
from typing import Optional
import ast

class CognitoUserAttributes(BaseModel):
    sub: str
    name: Optional[str] = ""
    email: Optional[str] = ""
    picture: Optional[str] = ""
    identities: Optional[str] = "[]"

    def extract_google_id(self) -> str:
        print(f"Extracting googleId from identities: {self.identities}")
        try:
            identities_list = ast.literal_eval(self.identities)
            if identities_list and isinstance(identities_list, list):
                google_id = identities_list[0].get("userId", self.sub)
                print(f"Found googleId: {google_id}")
                return google_id
        except Exception as e:
            print(f"Failed to parse identities, fallback to sub: {e}")
        return self.sub

class PostConfirmationEvent(BaseModel):
    request: dict

    def get_user_attributes(self) -> CognitoUserAttributes:
        print(f"Getting user attributes from event: {self.request}")
        return CognitoUserAttributes(**self.request.get("userAttributes", {}))
