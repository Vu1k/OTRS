import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
from navbar import Navbar
import matplotlib.pyplot as plt
from fig import fig_to_uri

nav = Navbar()

options=[
    {"label": 'nuevo_asignado', "value": 'nuevo_asignado'},
    {"label": 'asignado_en_progreso', "value": 'asignado_en_progreso'},
    {"label": 'asignado_pendiente', "value": 'asignado_pendiente'},
    {"label": 'asignado_cerrado', "value": 'asignado_cerrado'},
    {"label": 'asignado_espera', "value": 'asignado_espera'},
    {"label": 'nuevo_cerrado', "value": 'nuevo_cerrado'},
]

controls = dbc.Card([
    dbc.Container([
            dbc.FormGroup(
                [
                    dbc.Label("X variable"),
                    dcc.Dropdown(
                        options=options,
                        value="nuevo_cerrado",
                        id='x-variable',
                    ),
                ], id="x-dropdown",
             ),

    ])
])

output = dbc.Container([
    dbc.Card(dbc.CardImg(id='output'))
])

def dist_layout():
    layout = html.Div([
        nav,
        controls,
        output,
    ])
    return layout

def show_distribution(df, x_variable):

    var_data = pd.Series(pd.to_timedelta(df.loc[df[x_variable] != '0', \
                                       x_variable].values).seconds/3600)

    # Get statistics
    min_val = var_data.min()
    max_val = var_data.max()
    mean_val = var_data.mean()
    med_val = var_data.median()
    mod_val = var_data.mode()[0]

    # Create a figure for 2 subplots (2 rows, 1 column)
    fig, ax = plt.subplots(2, 1, figsize = (10,4))

    # Plot the histogram
    ax[0].hist(var_data, color='yellowgreen' , edgecolor="#6A9662")
    ax[0].set_ylabel('Frequency')

    # Add lines for the mean, median, and mode
    ax[0].axvline(x=min_val, color = 'gray', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=mean_val, color = 'cyan', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=med_val, color = 'red', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=mod_val, color = 'yellow', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=max_val, color = 'gray', linestyle='dashed', linewidth = 2)

    # Plot the boxplot
    ax[1].boxplot(var_data, vert=False)
    ax[1].set_xlabel('Value')

    # Add a title to the Figure
    fig.suptitle('Data Distribution')

    out_url = fig_to_uri(fig)

    return out_url


