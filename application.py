# dash
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from wc import wc_layout, my_wordcloud
from dist import dist_layout, show_distribution
from rules import rules_layout, show_pivot, show_rules
from homepage import Homepage
import mysql.connector
# pandas
import pandas as pd
import plotly.express as px
from flask import Flask
import unidecode

# scripts
from dist import dist_layout, show_distribution
from homepage import Homepage
from rules import rules_layout, show_pivot, show_rules
from wc import my_wordcloud, wc_layout
from scripts import build_plot_wc

# mysql & data pull
otrs_user = 'dbadminotrs'
otrs_pass = 'jacsos-tygwuv-Dipky6'

cnx = mysql.connector.connect(user=otrs_user, password=otrs_pass,
                              host='otrs.cluster-ro-cwqmr5tsjjh9.us-west-2.rds.amazonaws.com',
                              database='tronex.otrs')

query = ('SELECT T.title, S.* \
         FROM `tronex.otrs`.itv_sabana_tickets AS S \
         INNER JOIN `tronex.otrs`.ticket AS T \
             ON S.ticket_id = T.id \
         WHERE cola = "SERVICIOS IT" AND \
             correo_cliente NOT IN \
                ("soporte@sasaconsultoria.com", \
                "telefonia@tronex.com", \
                 "serviciosit@tronex.com") \
            AND T.title not like "%has low free space" \
            AND agente in ("JAIME ALBERTO GONZALEZ", "ROBINSON CASTRO", "RODOLFO LEON VELEZ") \
            AND estado_ticket <> "merged"')

df = pd.read_sql(query, con=cnx)

years = pd.to_datetime(df['fecha_creacion']).dt.year.unique()
year_list = [{'label': x, 'value': x} for x in years]
# --------------------------------------------------------------------------------

# server
server = Flask(__name__)
# ------------------------------------------------------------------------------

# app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
)
application = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
# --------------------------------------------------------------------------------


# testing area

# --------------------------------------------------------------------------------


#
@app.callback(Output('year_dropdown', 'options'),
              [Input('year_dropdown', 'value')])
def update_dropdown(year):
    return year_list


@app.callback(Output('month_dropdown', 'options'),
              [Input('year_dropdown', 'value')])
def update_dropdown(year):
    month = pd.to_datetime(df[pd.to_datetime(df['fecha_creacion']).dt.year == int(
        year)]['fecha_creacion']).dt.month.unique()
    month_list = [{'label': x, 'value': x} for x in month]
    return month_list


@app.callback(Output('year_dropdown_dist', 'options'),
              [Input('year_dropdown_dist', 'value')])
def update_dropdown(year):
    return year_list


@app.callback(Output('month_dropdown_dist', 'options'),
              [Input('year_dropdown_dist', 'value')])
def update_dropdown(year):
    month = pd.to_datetime(df[pd.to_datetime(df['fecha_creacion']).dt.year == int(
        year)]['fecha_creacion']).dt.month.unique()
    month_list = [{'label': x, 'value': x} for x in month]
    return month_list


@app.callback(Output('year_dropdown_rules', 'options'),
              [Input('year_dropdown_rules', 'value')])
def update_dropdown(year):
    return year_list


@app.callback(Output('month_dropdown_rules', 'options'),
              [Input('year_dropdown_rules', 'value')])
def update_dropdown(year):
    month = pd.to_datetime(df[pd.to_datetime(df['fecha_creacion']).dt.year == int(
        year)]['fecha_creacion']).dt.month.unique()
    month_list = [{'label': x, 'value': x} for x in month]
    return month_list


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
    Output('year_dropdown_dist', 'disabled'),
    Output('month_dropdown_dist', 'disabled'),
    [Input('x-variable', 'value'),
        Input('month_dropdown_dist', 'value'),
        Input('year_dropdown_dist', 'value'),
        Input('year_check_dist', 'value'),
        Input('month_check_dist', 'value')]
)
def update_dist(x_variable, month, year, ycheck, mcheck):
    month = int(month)
    month_list = pd.to_datetime(df[pd.to_datetime(
        df['fecha_creacion']).dt.year == int(year)]['fecha_creacion']).dt.month.unique()
    if month not in month_list:
        month = month_list[0]
    df_wc = df.copy()
    try:
        df_wc['fecha_creacion'] = pd.to_datetime(df_wc['fecha_creacion'])
        df_wc.set_index('fecha_creacion', inplace=True)
    except:
        pass
    if ycheck == ['1']:
        if mcheck == ['1']:
            df_wc = df_wc.loc[str(year) + '-' + str(month)].copy()
            graph = show_distribution(df_wc, x_variable)
            return graph, False, False
        else:
            df_wc = df_wc.loc[str(year)].copy()
            graph = show_distribution(df_wc, x_variable)
            return graph, False, True
    else:
        graph = show_distribution(df_wc, x_variable)
        return graph, True, True


@app.callback(
    Output('month_check_rules', 'className'),
    Output('month_dropdown_rules', 'className'),
    [Input('year_check_rules', 'value'), ]
)
def update_mcheck(ycheck):
    if ycheck == ['1']:
        return 'd-block', 'd-block'
    else:
        return 'd-none', 'd-none'


@app.callback(
    Output('month_check_dist', 'className'),
    Output('month_dropdown_dist', 'className'),
    [Input('year_check_dist', 'value'), ]
)
def update_mcheck(ycheck):
    if ycheck == ['1']:
        return 'd-block', 'd-block'
    else:
        return 'd-none', 'd-none'


@app.callback(
    Output('month_check', 'className'),
    Output('month_dropdown', 'className'),
    [Input('year_check', 'value'), ]
)
def update_mcheck(ycheck):
    if ycheck == ['1']:
        return 'd-block', 'd-block'
    else:
        return 'd-none', 'd-none'


@app.callback(
    Output('wc_output', 'src'),
    Output('wc_table', 'data'),
    Output('bars_wc', 'figure'),
    Output('year_dropdown', 'disabled'),
    Output('month_dropdown', 'disabled'),
    Output('ticket_qty', 'children'),
    [Input('min-freq-slider', 'value'),
    Input('max-vocab-slider', 'value'),
    Input('month_dropdown', 'value'),
    Input('year_dropdown', 'value'),
    Input('year_check' , 'value'),
    Input('month_check', 'value'),
    Input('stop_words_button', 'n_clicks'),
    Input('sw_button', 'n_clicks')],
    State('stop_words', 'value'),
    State('sw_query', 'value')
)
def update_wc(min, max, month, year, ycheck, mcheck, stop_words_button,sw_button, stop_words, sw_query):
    sw = set(stop_words.replace(' ', '').split(','))
    month_list = pd.to_datetime(df[pd.to_datetime(df['fecha_creacion']).dt.year == int(year)]['fecha_creacion']).dt.month.unique()

    if month not in month_list:
        month = month_list[0]
    df_wc = df.copy()

    df_wc['title'] = df_wc['title'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    try:
        df_wc['fecha_creacion'] = pd.to_datetime(df_wc['fecha_creacion'])
        df_wc.set_index('fecha_creacion', inplace=True)
    except:
        pass
    if ycheck == ['1']:
        if mcheck == ['1']:
            df_wc = df_wc.loc[str(year) + '-' + str(month)].copy()
            graph = my_wordcloud(df_wc, min, max, sw)
            sw_table = wc_table_out(df_wc, sw_query)
            ticket_qty = 'Encontrados ' + str(len(sw_table)) + ' tickets'

            graph_bar = build_plot_wc(sw_query, month, year, ycheck, mcheck, df_wc)

            return graph, sw_table, graph_bar, False, True, ticket_qty
        else:
            df_wc = df_wc.loc[str(year)].copy()
            graph = my_wordcloud(df_wc, min, max, sw)
            sw_table = wc_table_out(df_wc, sw_query)
            ticket_qty = 'Encontrados ' + str(len(sw_table)) + ' tickets'

            graph_bar = build_plot_wc(sw_query, month, year, ycheck, mcheck, df_wc)

            return graph, sw_table, graph_bar, False, True, ticket_qty
    else:
        graph = my_wordcloud(df_wc, min, max, sw)
        sw_table = wc_table_out(df_wc, sw_query)
        ticket_qty = 'Encontrados ' + str(len(sw_table)) + ' tickets'

        graph_bar = build_plot_wc(sw_query, month, year, ycheck, mcheck, df_wc)

        return graph, sw_table, graph_bar, False, True, ticket_qty

def wc_table_out(df_wc, sw_query):
            df_wc['title'] = df_wc['title'].str.lower()
            sw_table = df_wc.loc[df_wc['title'].str.contains(sw_query, case=False), :]
            sw_table = sw_table[['title', 'ticket_id', 'ticket_numero', 'servicio']]
            sw_table['ticket_id'] = sw_table['ticket_id'].astype(str)
            sw_table['link'] = 'http://servicios.tronex.com/otrs/index.pl?Action=AgentTicketZoom;TicketID=' + sw_table['ticket_id'].copy()
            sw_table['link'] = sw_table[['ticket_numero', 'link']].apply(lambda x: '[{}]({})'.format(x[0], x[1]), axis=1).copy()
            sw_table = sw_table[['title', 'servicio', 'link']]
            sw_table = sw_table.reset_index().to_dict('records')

            return sw_table

# -------------------------------Bar plot WC----------------------------------
# @app.callback(
#     Output('bars_wc', 'figure'),
#     [Input('bars_wc_button', 'n_clicks'),
#      Input('month_dropdown', 'value'),
#      Input('year_dropdown', 'value'),
#      Input('year_check', 'value'),
#      Input('month_check', 'value')],
#      State('bars_wc_text', 'value')
# )
# def plot_bars_wc_layout(bars_wc_button, m , y, yc , mc, txt):
#     graph = build_plot_wc(txt, m, y, yc, mc, df)
#     return graph

#------------------------------------------------------------------------------


@app.callback(
    Output('rules', 'data'),
    Output('year_dropdown_rules', 'disabled'),
    Output('month_dropdown_rules', 'disabled'),
    [Input('field', 'value'),
     Input('month_dropdown_rules', 'value'),
     Input('year_dropdown_rules', 'value'),
     Input('year_check_rules', 'value'),
     Input('month_check_rules', 'value')]
)
def update_rules(field, month, year, ycheck, mcheck):
    #   return show_rules(df, field), False, False
    month = int(month)
    month_list = pd.to_datetime(df[pd.to_datetime(
        df['fecha_creacion']).dt.year == int(year)]['fecha_creacion']).dt.month.unique()
    if month not in month_list:
        month = month_list[0]
    df_wc = df.copy()
    try:
        df_wc['fecha_creacion'] = pd.to_datetime(df_wc['fecha_creacion'])
        df_wc.set_index('fecha_creacion', inplace=True)
    except:
        pass
    if ycheck == ['1']:
        if mcheck == ['1']:
            df_wc = df_wc.loc[str(year) + '-' + str(month)].copy()
            graph = show_rules(df_wc, field)
            return graph, False, False
        else:
            df_wc = df_wc.loc[str(year)].copy()
            graph = show_rules(df_wc, field)
            return graph, False, True
    else:
        graph = show_rules(df_wc, field)
        return graph, True, True


def f(row):
    return "[{}]({})".format(row["link"])


@app.callback(
    Output('tickets', 'data'),
    [Input('rules', 'selected_rows'),
     Input('rules', 'data'),
     Input('field', 'value')]
)
def update_rules(rows, df_rules, field):
    if rows == None:
        return None
    else:
        df_rules = pd.DataFrame.from_dict(df_rules)
        serv_1 = df_rules.iloc[rows[0], 1].split("'")[1]
        serv_2 = df_rules.iloc[rows[0], 2].split("'")[1]
        df_pivot = show_pivot(df, field)
        fechas = df_pivot.loc[(df_pivot[serv_1] == 1) & (
            df_pivot[serv_2] == 1)].reset_index()['fecha_creacion']
        df_tickets = df.loc[(df.fecha_creacion.isin(fechas)) &
                            (df.servicio.isin([serv_1, serv_2]))]
        df_tickets['ticket_id'] = df_tickets['ticket_id'].astype(str)
        df_tickets['link'] = 'http://servicios.tronex.com/otrs/index.pl?Action=AgentTicketZoom;TicketID=' + \
            df_tickets['ticket_id'].copy()
        df_tickets['link'] = df_tickets[['ticket_numero', 'link']].apply(
            lambda x: '[{}]({})'.format(x[0], x[1]), axis=1).copy()
        df_tickets = df_tickets.loc[:, ['title', 'link']]
        return df_tickets.reset_index().to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
