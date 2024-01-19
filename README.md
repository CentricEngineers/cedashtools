# Summary
Use this package with your Centric Engineers tools to acquire user access levels from centricengineers.com.

# Usage

## Single Page Dash App
In a simple single page Dash-Plotly application.

```python
import dash
from dash import dcc, html, Input, Output
from cedashtools.user_access import validator
from cedashtools.user_access.website import AccessLevel

# set default
USER_PAID = False

# Tool ID provided by centricengineers.com
TOOL_ID = 'a_tool_id'

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='content'),
])


@app.callback(Output('content', 'children'),
              [Input('url', 'search')])
def display_content_based_on_access(search: str):
    # run the validator and set the USER_PAID variable for the duration of this session
    validator.website.login('username', 'password')
    url_vars = validator.parse_url_params(search)  # URL vars contain user information
    access_level = validator.get_access_level(url_vars, TOOL_ID)
    if access_level == AccessLevel.PAID:
        global USER_PAID
        USER_PAID = True  # set USER_PAID variable for access-level testing throughout application
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

# set default
USER_PAID = False

# Tool ID provided by centricengineers.com
TOOL_ID = 'a_tool_id'

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
import app
from dash import html, register_page
from cedashtools.user_access import validator
from cedashtools.user_access.website import AccessLevel

register_page(
    __name__,
    name='Home',
    path='/'
)


def layout(**url_vars):  # URL vars contain user information
    # run the validator on the home page and set the app.USER_PAID variable for the duration of this session
    validator.website.login('username', 'password')
    access_level = validator.get_access_level(url_vars, app.TOOL_ID)
    if access_level == AccessLevel.PAID:
        app.USER_PAID = True  # set app.USER_PAID for access-level testing throughout application
        layout = html.Div([html.H1(["Paid Content"])])
    else:
        layout = html.Div([html.H1(["Free Content"])])
    return layout
```
