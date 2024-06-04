import requests
from enum import Enum
from tenacity import retry, wait_fixed, stop_after_attempt


class AccessLevel(Enum):
    FREE = 0
    PAID = 1


ses = requests.Session()
ce_login_url = 'https://centricengineers.com/accounts/login/'
ce_validation_url = 'https://centricengineers.com/licenses/validateuser/'


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def validate_user(user_hash: str, tool_id: str) -> AccessLevel:
    payload = {
        "user": user_hash,
        "product": tool_id,
    }
    response = ses.get(ce_validation_url, params=payload)
    response.raise_for_status()
    json = response.json()
    return AccessLevel(json['access_level'])


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def login(username: str, password: str):
    ses.get(ce_login_url)
    csrf = ses.cookies['csrftoken']
    login_data = {'username': username, 'password': password, 'csrfmiddlewaretoken': csrf}
    headers = {'X-CSRFToken': csrf, 'Referer': ce_login_url}
    response = ses.post(ce_login_url, data=login_data, headers=headers)
    response.raise_for_status()

