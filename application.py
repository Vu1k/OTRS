import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from wc import wc_layout, my_wordcloud
from dist import dist_layout, show_distribution
from rules import rules_layout, show_pivot, show_rules
from homepage import Homepage
import mysql.connector
import pandas as pd
from flask import Flask

server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
application = app.server

app.config.suppress_callback_exceptions = True

otrs_user = 'usr_tronexotrs'
otrs_pass = 'usr$otrs#56aN7Rt*mp1'

cnx = mysql.connector.connect(user=otrs_user, password=otrs_pass,
                              host='pantermysql.cwqmr5tsjjh9.us-west-2.rds.amazonaws.com',
                              database='tronex.otrs')

query = ('SELECT T.title, S.* \
         FROM `tronex.otrs`.itv_sabana_tickets AS S \
         INNER JOIN `tronex.otrs`.ticket AS T \
             ON S.ticket_id = T.id \
         WHERE cola = "SERVICIOS IT" AND \
             correo_cliente NOT IN \
                ("soporte@sasaconsultoria.com", \
                "telefonia@tronex.com" \
                 "serviciosit@tronex.com") \
            AND T.title not like "%has low free space" \
            AND YEAR(S.fecha_creacion)=2020 \
            AND agente in ("JAIME ALBERTO GONZALEZ", "ROBINSON CASTRO", "RODOLFO LEON VELEZ") \
            AND estado_ticket <> "merged"')

df = pd.read_sql(query, con=cnx)

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/freq':
        return dist_layout()
    elif pathname == '/wordcloud':
        return wc_layout()
    elif pathname == '/rules':
        return rules_layout()
    else:
        return Homepage()

@app.callback(
    Output('output', 'src'),
    [Input('x-variable', 'value')]
)
def update_graph(x_variable):
    graph = show_distribution(df, x_variable)
    return graph

@app.callback(
    Output('wc_output', 'src'),
    [Input('min-freq-slider', 'value'),
    Input('max-vocab-slider', 'value')]
)
def update_graph(min, max):
    graph = my_wordcloud(df, min, max)
    return graph

@app.callback(
    Output('rules', 'data'),
    [Input('field', 'value')]
)
def update_rules(field):
    return show_rules(df, field)

@app.callback(
    Output('temp_label', 'children'),
    [Input('rules', 'selected_rows'),
    Input('rules', 'data'),
    Input('field', 'value')]
)
def update_temp(rows, df_rules, field):
    if rows == None:
        return None
    else:
        df_rules = pd.DataFrame.from_dict(df_rules)
        serv_1 = df_rules.iloc[rows[0], 1].split("'")[1]
        df_pivot = show_pivot(df, field)
        print(serv_1)
        print(df_pivot[[serv_1]])
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
