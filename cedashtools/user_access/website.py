import requests
from enum import Enum
from tenacity import retry, wait_fixed, stop_after_attempt


class AccessLevel(Enum):
    FREE = 0
    LITE = 1
    STUDENT = 2
    PRO = 3
    ENTERPRISE = 4


ce_validation_url = "https://centricengineers.com/licenses/validateuser/"


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def validate_user(user_hash: str, tool_id: str) -> AccessLevel:
    ses = requests.Session()
    payload = {
        "user": user_hash,
        "product": tool_id,
    }
    response = ses.get(ce_validation_url, params=payload)
    response.raise_for_status()
    json = response.json()
    return AccessLevel(json["access_level"])


