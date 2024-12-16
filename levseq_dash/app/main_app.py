import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, html
from dash_bootstrap_templates import load_figure_template

from levseq_dash.app import db_manager, layout_upload, parser
from levseq_dash.app import global_strings as gs

# Initialize the app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(
    __name__,
    title=gs.web_title,
    external_stylesheets=[dbc.themes.PULSE, dbc_css, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)

# VERY important line of code for running with gunicorn
# you run the 'server' not the 'app'. VS. you run the 'app' with uvicorn
server = app.server

load_figure_template(gs.dbc_template_name)
# Define the form layout

# app keeps one instance of the b manager
dbmgr = db_manager.DBManager()

app.layout = dbc.Container(
    [
        layout_upload.upload_form_layout,
        html.Div(id="temp-output", className="mt-4"),  # TODO: temp
    ],
    # fluid=True,
)


@app.callback(
    Output("temp-output", "children"),
    Input("id-button-upload-data", "contents"),
    State("id-button-upload-data", "filename"),
    State("id-button-upload-data", "last_modified"),
)
def on_upload_experiment(contents, filename, last_modified):
    if not contents:
        # TODO add the alert
        return "No file uploaded."

    result, df = parser.parse_csv_contents(contents, filename, last_modified)

    return result


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
