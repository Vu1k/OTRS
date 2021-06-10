import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
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
            value = ['1'],
            id = 'year_check',
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
            id = 'month_check',
            switch = True,
        )
    ])
)

month_list = [{'label': x, 'value': x} for x in range(1,13)]

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
           ])
         ]),
    ],
)

output = dbc.Container([
    dbc.Card(dbc.CardImg(id='wc_output'))
])

def wc_layout():
    layout = dbc.Container([
        dbc.Row([
            nav,
         ]),
        dbc.Row([
            dbc.Col(controls, md=4),
            dbc.Col(output, md=8)
        ], no_gutters=True)
    ], fluid=True)
    return layout

def my_wordcloud(df_wc, min_freq, max_vocab):
    comment_words = ''
    stopwords = set(['con', 'el', 'de', 'la', 'y', 'para', 'por', 'a', 'no', 'del', 'sin', 'not', 'in', 're', 'se', 'rv', 'lo', 'las', 'en'])
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
                    stopwords = stopwords,
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


