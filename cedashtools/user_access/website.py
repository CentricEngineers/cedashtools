import requests
from enum import Enum
import rsa
from tenacity import retry, wait_fixed, stop_after_attempt


ce_validation_url = "https://centricengineers.com/licenses/validateuser/"


class AccessLevel(Enum):
    FREE = 0
    LITE = 1
    STUDENT = 2
    PRO = 3
    ENTERPRISE = 4


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def validate_user(user_hash: str, tool_id: str,
                  my_private_key: rsa.PrivateKey,
                  ce_public_key: rsa.PublicKey) -> AccessLevel:
    ses = requests.Session()
    payload = {
        "user": user_hash,
        "product": tool_id,
    }
    response = ses.get(ce_validation_url, params=payload)
    response.raise_for_status()
    json = response.json()
    level = _extract_level(json, my_private_key, ce_public_key)
    return AccessLevel(level)


def _extract_level(json: dict, my_private_key: rsa.PrivateKey,
                   ce_public_key: rsa.PublicKey) -> int:
    level = rsa.decrypt(json['access_level'], my_private_key)
    signature = json['signature']
    validation = rsa.verify(level, signature, ce_public_key)
    if validation == 'SHA-512':
        return int(level.decode('utf8'))
    return 0



