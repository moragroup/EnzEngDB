from dash import html
from dash_iconify import DashIconify
import plotly_express as px
import pandas as pd

# --------------------
#   Inline styles
# --------------------
upload_default = {
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "padding": "10px",
    "textAlign": "center",
    "cursor": "pointer",
}
upload_success = success_style = {
    "borderWidth": "4px",
    "borderStyle": "dashed",
    "padding": "10px",
    "textAlign": "center",
    "cursor": "pointer",
    "borderColor": "green",
}

border_row = {"border": "0px solid blue"}
border_column = {"border": "0px solid red"}
border_table = {"border": "0px solid magenta"}
card_shadow = {"box-shadow": "1px 2px 7px 0px grey", "border-radius": "5px"}

top_card_head = "card-title fw-bold custom-card-header"
top_card_body = "text-primary-emphasis"

# --------------------
#   Icons
# --------------------
MEDIUM = 20
SMALL = 16

icon_del_exp = html.I(
    DashIconify(icon="fa-solid:trash-alt", height=SMALL, width=SMALL),
    # style={"margin-right": "8px"} # add the margin if there is text next to it
    # style={"color": "var(--bs-danger)"}
)
icon_go_to_next = html.I(DashIconify(icon="mdi:chart-line", height=SMALL, width=SMALL), style={"margin-left": "8px"})
icon_home = DashIconify(icon="mdi:home", width=20)
icon_upload = DashIconify(icon="mdi:tray-upload", width=20)


# --------------------
#   AGGrid Cell colorings
# --------------------
def data_bars_colorscale(df, column):
    """
    colors the bars in the cells in the table
    color max and min is based on the column values max and min
    uses color scale

    """
    # this doesn't use the mean value as the center of the coloring
    n_bins = 200
    min_value = df[column].min()
    max_value = df[column].max()

    # Generate color scale from Plotly
    color_scale = px.colors.sample_colorscale(px.colors.diverging.RdBu, [i / n_bins for i in range(n_bins)])
    # rdbu goes from blue to red, I want it the other way
    color_scale.reverse()

    # color_scale = px.colors.sample_colorscale(color_scale, [i / n_bins for i in range(n_bins)])

    # Convert to RGBA with transparency
    alpha = 1.0
    color_scale = [color.replace("rgb", "rgba").replace(")", f", {alpha})") for color in color_scale]

    styles = []
    for i in range(1, n_bins + 1):
        ratio_min = min_value + (i - 1) * (max_value - min_value) / n_bins
        ratio_max = min_value + i * (max_value - min_value) / n_bins
        max_bound_percentage = (i / n_bins) * 100
        color = color_scale[i - 1]  # Pick color from scale

        styles.append(
            {
                "condition": f"params.value >= {ratio_min}" + (f" && params.value < {ratio_max}" if i < n_bins else ""),
                "style": {
                    "background": f"""
                        linear-gradient(90deg,
                        {color} 0%,
                        {color} {max_bound_percentage}%,
                        white {max_bound_percentage}%,
                        white 100%)
                    """,
                    "color": "black",
                },
            }
        )

    return styles


