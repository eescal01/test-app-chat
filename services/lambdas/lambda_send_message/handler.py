from use_case import handle_send_message

def lambda_handler(event, context):
    return handle_send_message(event, context)
