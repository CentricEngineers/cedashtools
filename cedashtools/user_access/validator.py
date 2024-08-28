import rsa
from cedashtools.user_access import website


def has_vars(params: str) -> bool:
    return '=' in params


def parse_url_params(params: str) -> dict:
    """ Example: params='?a=test&b=pass' """
    if not has_vars(params):
        return dict()
    return dict(arg_pair.split('=') for arg_pair in params[1:].split('&'))


def get_public_key_object(key: bytes) -> rsa.PublicKey:
    return rsa.PublicKey.load_pkcs1(key)


def get_private_key_object(key: bytes) -> rsa.PrivateKey:
    return rsa.PrivateKey.load_pkcs1(key)


def get_access_level(url_vars: dict, tool_id: str,
                     my_private_key: bytes, ce_public_key: bytes) -> website.AccessLevel:
    user_id = url_vars.get('u')  # `u` varname is set by centricengineers.com
    my_priv = get_private_key_object(my_private_key)
    ce_pub = get_public_key_object(ce_public_key)
    return website.validate_user(user_id, tool_id, my_priv, ce_pub)



