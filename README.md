# Summary
Use this package with your Centric Engineers tools to acquire user access levels from CentricEngineers.com.

# Usage

## Single Page Dash App
In a simple single page Dash-Plotly application.

```python
import dash
from dash import dcc, html, Input, Output
from cedashtools.user_access import validation, encryption
from cedashtools.user_access.website import AccessLevel, ToolPayload, ce_validation_url


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='content'),
])


@app.callback(Output('content', 'children'),
              Input('url', 'search'))
def display_content_based_on_access(search: str):
    # Tool ID provided by centricengineers.com
    tool_id = 'a_tool_id'
    
    # encryption keys can be specified by file path
    encryption.keys.PUBLIC_KEY_FILE_PATH = r'/Path/To/File/Containing/Public_Key'
    encryption.keys.PRIVATE_KEY_FILE_PATH = r'/Path/To/File/Containing/Private_Key'
    
    # get user's access level
    user_id = validation.get_user_id(validation.parse_url_params(search))  # URL vars contain user information
    payload = ToolPayload(user_id, tool_id)
    access_level = validation.get_access_level(ce_validation_url, payload, encryption.keys)
    
    # display content based on access level
    if access_level >= AccessLevel.PRO:
        layout = html.Div([html.H1(["Paid Content"])])
    else:
        layout = html.Div([html.H1(["Free Content"])])
    return layout
```

## Mult-Page Dash App
In a multi-page Dash-Plotly application (using pages).

### app.py
```python
import dash
from dash import html, dcc

APP_TITLE = "Dash App"  

app = dash.Dash(
    __name__,
    title=APP_TITLE,
    use_pages=True,  # New in Dash 2.7 - Allows us to register pages
)

app.layout = html.Div([dash.page_container])

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
```

### home.py

```python
from dash import html, register_page
from cedashtools.user_access import validation, encryption
from cedashtools.user_access.website import AccessLevel, ToolPayload, ce_validation_url

register_page(
    __name__,
    name='Home',
    path='/'
)


def layout(**url_vars):  # URL vars contain user information
    
    # Tool ID provided by CentricEngineers.com
    tool_id = 'a_tool_id'

    # encryption keys can also be specified by string
    encryption.keys.PUBLIC_KEY_STRING = '-----BEGIN PUBLIC KEY-----FakePublicKey-----END PUBLIC KEY-----'
    encryption.keys.PRIVATE_KEY_STRING = '-----BEGIN PRIVATE KEY-----FakePrivateKey-----END PRIVATE KEY-----'

    # get user's access level
    user_id = validation.get_user_id(url_vars)
    payload = ToolPayload(user_id, tool_id)
    access_level = validation.get_access_level(ce_validation_url, payload, encryption.keys)

    # display content based on access level
    if access_level >= AccessLevel.PRO:
        layout = html.Div([html.H1(["Paid Content"])])
    else:
        layout = html.Div([html.H1(["Free Content"])])
    return layout
```

# Change Log

## Version 0.3.0 (10-18-2024)

- Added cryptography support
- Refactored API

