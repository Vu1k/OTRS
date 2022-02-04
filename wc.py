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
        step=1,
        value=15,
        marks={1: "1", **{i: str(i) for i in range(5, 51, 5)}},
    ),
    className="p-3 mb-2",
)

max_vocab_slider = html.Div(
    dcc.Slider(
        id="max-vocab-slider",
        min=1,
        max=300,
        step=1,
        value=100,
        marks={1: "1", **{i: str(i) for i in range(30, 301, 30)}},
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
    className = 'me-2',
)

sw_query = dbc.Container(
    dcc.Input(
        id = 'sw_query',
        placeholder = 'Palabra para filtrar',
        type = 'text',
        value = '',
        style = {'width': '100%', 'height': 50},
    )
)

sw_button = dbc.Button(
    'Enviar',
    id = 'sw_button',
    className = 'me-2',
)

bars_wc_text = dbc.Container(
    dcc.Input(
        id = 'bars_wc_text',
        placeholder = 'Término para buscar servicios',
        type = 'text',
        value = '',
        style = {'width': '100%', 'height': 50},
    )
)

controls = dbc.Card(
    [
        dbc.Container([
            dbc.FormGroup([dbc.Label("Minimum frequency:"), min_freq_slider]),
            dbc.FormGroup(
                [dbc.Label("Maximum number of words:"), max_vocab_slider]
            ),
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
           ]),
           dbc.Row([
               dbc.Label('Ingrese las palabras excluidas separadas por coma'),
           ]),
           dbc.Row([
               dbc.Col(stop_words),
           ]),
           dbc.Row([
                dbc.Col(stop_words_button),
           ]),
           dbc.Row([
                dbc.Label('Ingrese el término que desea buscar en los tickets:'),
           ]),
           dbc.Row([
                dbc.Col(sw_query),
           ]),
           dbc.Row([
                dbc.Col(sw_button),
                dbc.Col(dbc.Label(
                    id='ticket_qty',
                    color='success'))
           ]),
           dbc.Row([
               dbc.Label('Ingrese el término para consultar los servicios'),
           ]),
           dbc.Row([
               dbc.Col(bars_wc_text),
           ]),
         ]),
    ],
)

output = dbc.Container([
    dbc.Card(dbc.CardImg(id='wc_output'))
])

output1 = dbc.Container([
    dbc.Card(dbc.CardImg(id='wc_output1'))
])

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
        page_size=20,
        export_format='csv',
        row_selectable=False,
    ),
])

def wc_layout():
    layout = dbc.Container([
        dbc.Row([
            nav,
        ]),

        dbc.Row([
            dbc.Col(controls, md=4),
            dbc.Col(output, md=8)
        ]),

        dbc.Row(
            dbc.Col(output_table, md=12)
        ),

        dbc.Row(
            dbc.Col(dcc.Graph(
                        id='bars_wc',
                        figure={},
                        ), md=12
                    ),
        )
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

    wordcloud = WordCloud(width = 800, height = 800,
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

    plt.figure()
    plt.imshow(wordcloud.generate(comment_words), interpolation='bilinear')
    plt.axis('off')

    out_url = fig_to_uri(plt)

    return out_url
