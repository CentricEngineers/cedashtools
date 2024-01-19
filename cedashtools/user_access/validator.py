from cedashtools.user_access import website


def has_vars(params: str) -> bool:
    return '=' in params


def parse_url_params(params: str) -> dict:
    """ Example: params='?a=test&b=pass' """
    if not has_vars(params):
        return dict()
    return dict(arg_pair.split('=') for arg_pair in params[1:].split('&'))


def get_access_level(url_vars: dict, tool_id: str) -> website.AccessLevel:
    user_id = url_vars.get('u')  # `u` varname is set by centricengineers.com
    return website.validate_user(user_id, tool_id)



