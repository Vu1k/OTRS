import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.Nav(
	children = [
        dbc.NavItem(dbc.NavLink('WordCloud', href='wordcloud'), className='navbar-text'),
        dbc.NavItem(dbc.NavLink('Frecuencias', href='freq'), className='navbar-text'),
        dbc.NavItem(dbc.NavLink('Reglas de asociación', href='rules'), className='navbar-text'),
#   ], className='bg-secondary w-100 p-3')
	], className='navbar navbar-expand-lg navbar-dark bg-dark w-100 p-3')
    return navbar
