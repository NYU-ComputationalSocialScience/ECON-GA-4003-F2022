import dash
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output

from components import navbar

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.FONT_AWESOME
    ],
    use_pages=True,
    pages_folder="pages"
)
app.title = "NYC Citi Bike Fun"
server = app.server
app.config.suppress_callback_exceptions = True

# -----------
# Base layout
# -----------
app.layout = dbc.Container(
    [
        navbar,
        dash.page_container
    ]
)



if __name__ == '__main__':
    app.run_server(debug=True)
