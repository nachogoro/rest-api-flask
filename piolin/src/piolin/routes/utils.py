from flask import request
from datetime import datetime

def verify_token(request: request) -> str:
    '''
    Takes a request and verifies that the Authorization header correctly authorises
    a user.
    Returns the authorised user if successful, None otherwise.
    Currently, an authentication token is simply: nickname-secretstuff
    '''
    header_parts = request.headers.get('Authorization').split('-')

    if len(header_parts) != 2 or header_parts[1] != 'secretstuff':
        return None

    return header_parts[0]


def get_date() -> str:
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')
