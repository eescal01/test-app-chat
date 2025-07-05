from use_case import handle_disconnect


def lambda_handler(event, context):
    return handle_disconnect(event, context)
