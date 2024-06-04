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
    # run the validator and set the USER_PAID variable for the duration of this session
    validator.website.login('username', 'password')
    url_vars = validator.parse_url_params(search)  # URL vars contain user information
    access_level = validator.get_access_level(url_vars, tool_id)
    if access_level == AccessLevel.PAID:
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
    # Tool ID provided by centricengineers.com
    tool_id = 'a_tool_id'
    # run the validator on the home page and set the app.USER_PAID variable for the duration of this session
    validator.website.login('username', 'password')
    access_level = validator.get_access_level(url_vars, tool_id)
    if access_level == AccessLevel.PAID:
        layout = html.Div([html.H1(["Paid Content"])])
    else:
        layout = html.Div([html.H1(["Free Content"])])
    return layout
```
