from models import PostConfirmationEvent
from use_case import PostConfirmationUseCase


def lambda_handler(event, context):
    print("Received event:", event)
    try:
        post_event = PostConfirmationEvent(request=event.get("request", {}))
        user_attributes = post_event.get_user_attributes()

        use_case = PostConfirmationUseCase(user_attributes)
        use_case.execute()

        print("PostConfirmation Lambda executed successfully")
        return event

    except Exception as e:
        print(f"Error in PostConfirmation Lambda: {e}")
        raise e
