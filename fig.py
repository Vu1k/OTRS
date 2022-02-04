import io
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = io.BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

def plot_bars_wc(df: pd.DataFrame) -> px.bar:

    fig = px.bar(df, x='title', y='count', color='title', barmode='group')

    return fig


