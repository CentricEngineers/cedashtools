from .encryption import Keys
from .website import get_user_access, extract_level, ToolPayload, AccessLevel


def has_vars(params: str) -> bool:
    """Checks if url has parameters

    Args:
        params: the url parameters string to test

    Returns:
        True if url parameters exist, false otherwise
    """
    return '=' in params


def parse_url_params(params: str) -> dict:
    """Parses url parameters to dictionary

    Args:
        params: Example, '?a=test&b=pass'

    Returns:
        Dictionary of named url parameters containing their values
    """
    if not has_vars(params):
        return dict()
    return dict(arg_pair.split('=') for arg_pair in params[1:].split('&'))


def get_user_id(url_vars: dict) -> str:
    """Retrieves user id 'u' from dictionary

    Args:
        url_vars: dictionary containing 'u' key

    Returns:
        Contents of dictionary 'u' key
    """
    return url_vars.get('u')  # `u` varname is set by centricengineers.com


def get_access_level(validation_url: str, payload: ToolPayload, keys: Keys) -> AccessLevel:
    """Gets the user's access level for a specific Centric Engineers tool

    Args:
        validation_url: url for the access level request
        payload: ToolPayload containing user-id and tool-id
        keys: Keys containing Centric Engineers public and Tool private rsa keys

    Returns:
        The user's access level
    """
    json = get_user_access(validation_url, payload)
    return extract_level(json, keys)



