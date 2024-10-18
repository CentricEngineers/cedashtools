from dataclasses import dataclass
import requests
from enum import Enum
from tenacity import retry, wait_fixed, stop_after_attempt
from .encryption import verify_signature, decrypt_message, Keys


#: url used for user validation at CentricEngineers.com
ce_validation_url = "https://centricengineers.com/licenses/validateuser/"


class AccessLevel(Enum):
    FREE = 0
    LITE = 1
    STUDENT = 2
    PRO = 3
    ENTERPRISE = 4

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value


@dataclass
class ToolPayload:
    user_id: str
    tool_id: str


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def get_user_access(validation_url: str, payload: ToolPayload) -> dict:
    """Request user access level from url

    Args:
        validation_url: url for access level request
        payload: ToolPayload containing user-id and tool-id

    Returns:
        json response
    """
    ses = requests.Session()
    request_json = {
        "user": payload.user_id,
        "product": payload.tool_id,
    }
    response = ses.get(validation_url, params=request_json)
    response.raise_for_status()
    return response.json()


def extract_level(json: dict, keys: Keys) -> AccessLevel:
    """Extracts access level from json response

    Args:
        json: json from access level request
        keys: Keys containing Centric Engineers public and Tool private rsa keys

    Returns:
        The extracted access level
    """
    access_level = 0
    encrypted_level = bytes.fromhex(json['access_level'])
    signature = bytes.fromhex(json['signature'])
    if verify_signature(keys.public_key, signature, encrypted_level):
        access_level = int(decrypt_message(keys.private_key, encrypted_level))
    return AccessLevel(access_level)

