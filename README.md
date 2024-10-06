# Summary
Use this package with your Centric Engineers tools to acquire user access levels from centricengineers.com.

# Usage

## Single Page Dash App
In a simple single page Dash-Plotly application.

```python
import dash
from dash import dcc, html, Input, Output
from cedashtools.user_access import validator, encryption
from cedashtools.user_access.website import AccessLevel


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='content'),
])


@app.callback(Output('content', 'children'),
              [Input('url', 'search')])
def display_content_based_on_access(search: str):
    # Tool ID provided by centricengineers.com
    tool_id = 'a_tool_id'
    encryption.keys.PUBLIC_KEY_FILE_PATH = r'/Path/To/File/Containing/Public_Key'
    encryption.keys.PRIVATE_KEY_FILE_PATH = r'/Path/To/File/Containing/Private_Key'
    
    url_vars = validator.parse_url_params(search)  # URL vars contain user information
    access_level = validator.get_access_level(
        url_vars, tool_id, encryption.keys.public_key, encryption.keys.private_key
    )
    
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
from cedashtools.user_access import validator, encryption
from cedashtools.user_access.website import AccessLevel

register_page(
    __name__,
    name='Home',
    path='/'
)


def layout(**url_vars):  # URL vars contain user information
    
    # Tool ID provided by centricengineers.com
    tool_id = 'a_tool_id'
    encryption.keys.PUBLIC_KEY_STRING = '-----BEGIN PUBLIC KEY-----FakePublicKey-----END PUBLIC KEY-----'
    encryption.keys.PRIVATE_KEY_STRING = '-----BEGIN PRIVATE KEY-----FakePrivateKey-----END PRIVATE KEY-----'

    access_level = validator.get_access_level(
        url_vars, tool_id, encryption.keys.public_key, encryption.keys.private_key
    )
    
    if access_level >= AccessLevel.PRO:
        layout = html.Div([html.H1(["Paid Content"])])
    else:
        layout = html.Div([html.H1(["Free Content"])])
    return layout
```
