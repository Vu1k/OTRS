#from turtle import ht
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from datetime import datetime
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import matplotlib.pyplot as plt
from fig import fig_to_uri
from navbar import Navbar

nav = Navbar()

min_freq_slider = html.Div(
    dcc.Slider(
        id="min-freq-slider",
        min=1,
        max=50,
        step=10,
        value=15,
        marks={1: "1", **{i: str(i) for i in range(10, 51, 10)}},
    ),
    className="p-3 mb-2",
)

max_vocab_slider = html.Div(
    dcc.Slider(
        id="max-vocab-slider",
        min=1,
        max=50,
        step=10,
        value=15,
        marks={1: "1", **{i: str(i) for i in range(10, 51, 10)}},
    ),
    className="p-3",
)

year_check = dbc.Container(
    dbc.FormGroup([
        dbc.Checklist(
            options=[
                {'label': 'Filtro año', 'value': '1'},
            ],
            value=['1'],
            id='year_check',
            switch=True,
        )
    ])
)

month_check = dbc.Container(
    dbc.FormGroup([
        dbc.Checklist(
            options=[
                {'label': 'Filtro mes', 'value': '1'}
            ],
            value=['1'],
            id='month_check',
            switch=True,
        )
    ])
)

month_list = [{'label': x, 'value': x} for x in range(1, 13)]

month_dropdown = dbc.Container(
    dbc.Select(
        id='month_dropdown',
        value=datetime.now().month,
    )
)

year_dropdown = dbc.Container(
    dbc.Select(
        id='year_dropdown',
        value=datetime.now().year,
    )
)

stop_words = html.Div(
    dcc.Textarea(
        id = 'stop_words',
        placeholder = 'Escriba las palabras a excluir separadas por coma',
        value='',
        style = {'width': '100%', 'height': 50},
    )
)

stop_words_button = dbc.Button(
    'Enviar',
    id = 'stop_words_button',
    color='dark',
    className = 'me-1',
)

sw_query = dbc.Container(
    dcc.Input(
        id = 'sw_query',
        placeholder = 'Escriba una palabra para filtrar por el título de los tickets',
        type = 'text',
        value = '',
        style = {'width': '100%', 'height': 50},
    )
)

sw_button = dbc.Button(
    'Enviar',
    id = 'sw_button',
    color='dark',
    className = 'me-1',
)

bars_wc_text = dbc.Container(
    dcc.Input(
        id = 'bars_wc_text',
        placeholder = 'Término para buscar servicios asociados',
        type = 'text',
        value = '',
        style = {'width': '100%', 'height': 50},
    )
)

bars_wc_button = dbc.Button(
    'Enviar',
    id = 'bars_wc_button',
    color='dark',
    className = 'me-1',
)

output = dbc.Container([
    dbc.Card(dbc.CardImg(id='wc_output'))
])

controls_wc = dbc.Card(
    [
        dbc.CardHeader([
            dbc.Row([
                html.H4('Palabras a excluir'),
            ]),
            dbc.Row([
                dbc.Col(stop_words, md=9),
                dbc.Col(stop_words_button),
            ]),
        ]),
        dbc.CardBody(
            dbc.Row(output),
        ),
        dbc.CardFooter([
            dbc.Row([
                dbc.Col(
                    dbc.FormGroup([dbc.Label("Minimum frequency:"), min_freq_slider]), md=6
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [dbc.Label("Maximum number of words:"), max_vocab_slider]
                        ), md=6,
                ),
            ]),
            dbc.Row([
                dbc.Col(year_check),
                dbc.Col(
                    dbc.FormGroup([year_dropdown]),
                ),
            ]),
            dbc.Row([
                dbc.Col(month_check),
                dbc.Col(
                    dbc.FormGroup([month_dropdown]),
                )
            ]),
          ]),
    ], color='dark', outline=True, style={'width':'95%'})

cols = [
    {'name': 'ticket', 'id': 'link', 'presentation': 'markdown'},
    {'name': 'title', 'id': 'title'},
    {'name': 'servicio', 'id': 'servicio'},
]

output_table = dbc.Container([
    dash_table.DataTable(
        id="wc_table",
        columns=cols,
        data=[],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        filter_action='native',
        page_size=10,
        export_format='csv',
        row_selectable=False,
    ),
])

controls_qy = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                html.H4('Busqueda de tickets'),
            ]),
            dbc.Row([
                dbc.Col(sw_query),
                dbc.Col(sw_button),
            ]),
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Alert(
                    id='ticket_qty',
                    color='light'))
                ]),
            dbc.Row([
                dbc.Col(output_table),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bars_wc', figure={}))
            ])
        ]),
    ], color='dark', outline=True, style={'width':'95%'}),

controls_fg = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                html.H4('Consulta de servicios'),
            ]),
            dbc.Row([
                dbc.Col(bars_wc_text),
                dbc.Col(bars_wc_button),
            ]),
        ]),
        dbc.CardBody([
                dbc.Col(dcc.Graph(id='bars_wc', figure={}))
        ]),
    ], color='dark', outline=True, style={'width':'95%'}),


def wc_layout():
    layout = dbc.Container([
        dbc.Row([
            nav,
        ]),
        dbc.Row([
            dbc.Col(controls_wc, md=4),
            dbc.Col([
                dbc.Row(controls_qy),
            ], md=8),
        ]),
    ], fluid=True)
    return layout

def my_wordcloud(df_wc, min_freq, max_vocab, sw_query):
    comment_words = ''
    stopwords = set(['con', 'el', 'de', 'la', 'y', 'para', 'por', 'a', 'no',
                    'del', 'sin', 'not', 'in', 're', 'se', 'rv', 'lo', 'las', 'en'])
    stopwordsfinal = stopwords.union(sw_query)
    for val in df_wc.title:
        # typecaste each val to string

        val = str(val)
    # split the value
        tokens = val.split()
        tokens = [i.strip() for i in tokens]
    # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens)+" "

    wordcloud = WordCloud(width = 600, height = 600,
                    background_color ='white',
                    stopwords = stopwordsfinal,
                    min_font_size = 10)

    # filter frequencies based on min_freq and max_vocab
    sorted_frequencies = sorted(
        wordcloud.process_text(comment_words).items(), key=lambda x: x[1], reverse=True
    )
    frequencies = {
        k: v for k, v in sorted_frequencies[:max_vocab] if v >= min_freq
    }

    wc = WordCloud(
        max_words=max_vocab,
        background_color="white",
        colormap="plasma",
    )

#   wc.generate_from_frequencies(frequencies).to_image()

    plt.figure(figsize=(20,20))
    plt.imshow(wordcloud.generate(comment_words), interpolation='bilinear', aspect='auto')
    plt.tight_layout(pad=5)
    plt.axis('off')

    out_url = fig_to_uri(plt)

    return out_url
