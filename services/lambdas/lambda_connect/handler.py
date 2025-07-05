from use_case import handle_connect


def lambda_handler(event, context):
    return handle_connect(event, context)
