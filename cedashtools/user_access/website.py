import requests
from enum import Enum
from cryptography.hazmat.primitives.asymmetric import rsa
from tenacity import retry, wait_fixed, stop_after_attempt
from cedashtools.user_access.encryption import verify_signature, decrypt_message


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


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def validate_user(user_hash: str, tool_id: str,
                  public_key: rsa.RSAPublicKey, private_key: rsa.RSAPrivateKey) -> AccessLevel:
    ses = requests.Session()
    payload = {
        "user": user_hash,
        "product": tool_id,
    }
    response = ses.get(ce_validation_url, params=payload)
    response.raise_for_status()
    json = response.json()
    level = extract_level(json, public_key, private_key)
    return AccessLevel(level)


def extract_level(json: dict, public_key: rsa.RSAPublicKey, private_key: rsa.RSAPrivateKey) -> int:
    encrypted_level = bytes.fromhex(json['access_level'])
    signature = bytes.fromhex(json['signature'])
    if verify_signature(public_key, signature, encrypted_level):
        return int(decrypt_message(private_key, encrypted_level))
    return 0

