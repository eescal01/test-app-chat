from models import PostConfirmationEvent
from use_case import PostConfirmationUseCase


def lambda_handler(event, context):
    print("Received event:", event)
    try:
        request_data = event.get("request", {})
        print(f"Extracted request data: {request_data}")
        post_event: PostConfirmationEvent = PostConfirmationEvent(request=request_data)

        user_attributes = post_event.get_user_attributes()
        print(f"User attributes extracted: {user_attributes}")

        use_case = PostConfirmationUseCase(user_attributes)
        print("Initialized use case, starting execution")
        use_case.execute()

        print("PostConfirmation Lambda executed successfully")
        return event

    except Exception as e:
        print(f"Error in PostConfirmation Lambda: {e}")
        raise e
