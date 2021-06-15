import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from navbar import Navbar

nav = Navbar()

options=[
    {"label": "servicio", "value": "servicio"},
    {"label": "servicio_padre", "value": "servicio_padre"},
    {"label": "servicio_hijo", "value": "servicio_hijo"},
]

year_check = dbc.Container(
    dbc.FormGroup([
        dbc.Checklist(
            options=[
                {'label': 'Filtro año', 'value': '1'},
            ],
            value = ['1'],
            id = 'year_check_rules',
            switch = True,
        )
    ])
)

month_check = dbc.Container(
    dbc.FormGroup([
        dbc.Checklist(
            options=[
                {'label': 'Filtro mes', 'value': '1'}
            ],
            value = ['1'],
            id = 'month_check_rules',
            switch = True,
        )
    ])
)

month_list = [{'label': x, 'value': x} for x in range(1,13)]

month_dropdown = dbc.Container(
    dbc.Select(
        id='month_dropdown_rules',
        value=datetime.now().month,
    )
)

year_dropdown = dbc.Container(
    dbc.Select(
        id='year_dropdown_rules',
        value=datetime.now().year,
    )
)

controls = dbc.Card([
    dbc.Container([
        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    options=options,
                    value='servicio',
                    id='field',
                )
            ]),
     ]),
       dbc.Row([
           dbc.Col(year_check),
           dbc.Col(month_check)
       ]),
       dbc.Row([
           dbc.Col(
               dbc.FormGroup([year_dropdown]),
           ),
           dbc.Col(
               dbc.FormGroup([month_dropdown]),
           )
       ])
])

cols = [
    {'name': 'antecedents', 'id': 'antecedents'},
    {'name': 'consequents', 'id': 'consequents'},
    {'name': 'ant sup', 'id': 'antecedent support'},
    {'name': 'cons sup', 'id': 'consequent support'},
    {'name': 'sup', 'id': 'support'},
    {'name': 'conf', 'id': 'confidence'},
]

output = dbc.Container([
    dash_table.DataTable(
        id="rules",
        columns=cols,
        data=[],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        filter_action='native',
        page_size=20,
        export_format='csv',
        row_selectable='single',
    ),
])

cols = ['title', 'ticket_numero']

tickets = dbc.Container([
    dash_table.DataTable(
        id="tickets",
        columns=[{'name': 'ticket', 'id': 'link', 'presentation': 'markdown'}, 
                 {'name': 'title', 'id': 'title'},
],
        data=[],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        filter_action='native',
        page_size=20,
        export_format='csv',
    ),
])

temp = dbc.Container(
    html.A(id='temp_label')
)

def rules_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([nav]),
        ]),
        dbc.Row([
            dbc.Col([controls]),
        ]),
        dbc.Row([
            dbc.Col([output], md=8),
            dbc.Col([tickets], md=4),
        ], no_gutters=True),
    ], fluid=True,
    )
    return layout

def encode(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

def show_pivot(df, field):
    df['cantidad_servicio'] = 1
    df_pivot = df.pivot_table(index='fecha_creacion', \
                              columns=field, \
                              aggfunc='sum', \
                              values='cantidad_servicio', \
                              fill_value=0)

    df_pivot = df_pivot.applymap(encode)
    return df_pivot

def show_rules(df, field):
    df_pivot = show_pivot(df, field)
    df_freqserv = apriori(df_pivot, min_support=0.3, use_colnames=True)
    df_rules = association_rules(df_freqserv, min_threshold=1, metric='lift')

    df_rules['antecedents'] = df_rules['antecedents'].apply(lambda x: str(set(x)))
    df_rules['consequents'] = df_rules['consequents'].apply(lambda x: str(set(x)))

    df_rules.drop(columns=['lift', 'leverage', 'conviction'], inplace=True)

    df_rules['antecedent support'] = df_rules['antecedent support'].apply(lambda x: '{:,.1f}%'.format(x*100))
    df_rules['consequent support'] = df_rules['consequent support'].apply(lambda x: '{:,.1f}%'.format(x*100))
    df_rules['support'] = df_rules['support'].apply(lambda x: '{:,.1f}%'.format(x*100))
    df_rules['confidence'] = df_rules['confidence'].apply(lambda x: '{:,.1f}%'.format(x*100))

    return df_rules.reset_index().to_dict('records')

