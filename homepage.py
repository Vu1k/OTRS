import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar

nav = Navbar()

body = dbc.Container(
    [
        dcc.Location(id='url'),
#       dbc.Row(nav, id='topnav'),
        dbc.Row([
#           dbc.Col(controls, md=3),
            dbc.Col(
                dbc.Card(dbc.CardImg(id='body'))
            ),
        ])
    ],
    fluid=True,
)

def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()

if __name__ == "__main__":
    app.run_server()
