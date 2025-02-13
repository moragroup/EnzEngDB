import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Center Title Placeholder
            # html.Div("App Title", className="mx-auto text-center", style={"fontSize": "24px", "fontWeight": "bold"}),
            dbc.NavbarBrand("Levseq Dashboard", className="fs1"),
            # Right Logo Placeholder
            html.Img(src="https://via.placeholder.com/150", height="40px"),
        ],
        className="d-flex justify-content-between align-items-center",
    ),
    color="dark",
    dark=True,
    className="bg-primary text-light py-4 text-center fs-1 fw-light border-bottom",
)

sidebar = html.Div(
    [
        html.Img(
            src="https://via.placeholder.com/150",  # Placeholder for the logo
            style={"width": "100%", "margin-bottom": "20px"},
        ),
        html.Hr(),
        html.Br(),
        dbc.NavItem(dbc.NavLink(
            [DashIconify(icon="mdi:home", width=20), " Lab Dashboard"],
            href="/")),
        dbc.NavItem(dbc.NavLink(
            [DashIconify(icon="mdi:tray-upload", width=20), " Upload New Experiment"],
            href="/upload")),
    ],
    style={
        # "background-color": "#f8f9fa",
        "height": "100%",
        "padding": "20px",
    },
    className="p-0 bg-light",
)
