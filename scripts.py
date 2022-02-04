import pandas as pd
import plotly.express as px


def get_services_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the count of services from a word count dataframe
    - Parameters:
    ----------
        - df: pd.DataFrame
            - The word count dataframe

    - Returns:
    ----------
        - df: pd.DataFrame
    """
    df = pd.DataFrame(df['servicio'].value_counts()).reset_index().rename(
        columns={'index': 'servicio', 'servicio': 'cantidad'})

    return df


def plot_bars(df: pd.DataFrame) -> px.bar:
    """
    Builds a plotly bar chart from a word count dataframe
    - Parameters:
    ----------
        - df: pd.DataFrame
            - The word count dataframe

    - Returns:
    ----------
        - fig: px.bar
    """

    fig = px.bar(
        df,
        x='servicio',
        y='cantidad',
    ).update_layout(
        font={
            'size': 11,
        },
    )
    return fig


def build_plot_wc(word: str, month: int, year: int, ycheck: list, mcheck: list, df: pd.DataFrame) -> px.bar:
    """
    Builds a plotly bar chart from a word count dataframe
    - Parameters:
    ----------
        - word: str
            - The word to be plotted
        - month: int
            - The month to be plotted
        - year: int
            - The year to be plotted
        - ycheck: list
            - The year checkbox state
        - mcheck: list
            - The month checkbox state
        - df: pd.DataFrame
            - The word count dataframe

    - Returns:
    ----------
        - fig: px.bar
    """

    df['title'] = df['title'].str.lower()
    df = df[df.title.str.contains(word)].copy()


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
            df_bars_wc = get_services_counts(df_wc)
            return plot_bars(df_bars_wc)
        else:
            df_wc = df_wc.loc[str(year)].copy()
            df_bars_wc = get_services_counts(df_wc)
            return plot_bars(df_bars_wc)
    else:
        df_bars_wc = get_services_counts(df_wc)
        return plot_bars(df_bars_wc)
