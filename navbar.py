import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.Nav([
        dbc.NavItem(dbc.NavLink('WordCloud', href='wordcloud')),
        dbc.NavItem(dbc.NavLink('Frecuencias', href='freq')),
        dbc.NavItem(dbc.NavLink('Reglas de asociación', href='rules')),
    ], className='bg-secondary w-100 p-3')

    return navbar
