import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_molstar


def get_label(string):
    return dbc.Label(string, width=3, className="fs-6")


def get_top_variant_column_defs(df):
    # mean_values = df[df["amino_acid_substitutions"] == "#PARENT#"].groupby("cas_number")["fitness_value"].mean()
    return [
        {
            "field": "cas_number",
            "headerName": "CAS #",
            "width": 180,
        },
        {
            "field": "plate",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": "well",
            "width": 125,
        },
        {
            "field": "amino_acid_substitutions",
            "headerName": "Substitutions",
        },
        {
            "field": "fitness_value",
            "filter": "agNumberColumnFilter",
            # "cellStyle": {"styleConditions": data_bars_colorscale(df, "fitness_value")},
        },
    ]


def get_all_experiments_column_defs():
    return [
        {  # Checkbox column
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
            "headerName": "",
            "width": 50,
        },
        {
            "field": "experiment_id",
            "filter": "agNumberColumnFilter",
            # "checkboxSelection": True,
        },
        {
            "field": "experiment_name",
        },
        {
            "field": "upload_time_stamp",
        },
        {
            "field": "experiment_date",
        },
        {
            "field": "sub_cas",
        },
        {
            "field": "prod_cas",
        },
        {
            "field": "assay",
        },
        {
            "field": "mutagenesis_method",
        },
        {
            "field": "plates_count",
            "filter": "agNumberColumnFilter",
        },
    ]


def get_table_experiment():
    return dag.AgGrid(
        id="id-table-top-variants",
        # rowData=data.to_dict("records"),
        # columnDefs=components.get_top_variant_column_defs(),
        # TODO: update this correctly
        defaultColDef={
            # do NOT set "flex": 1 in default col def as it overrides all
            # the column widths
            "sortable": True,
            "resizable": True,
            "filter": True,
            # Set BOTH items below to True for header to wrap text
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
        },
        # columnSize="sizeToFit",
        style={"height": "600px", "width": "100%"},
        dashGridOptions={
            # "rowDragManaged": True,
            # "rowDragEntireRow": True
            "rowSelection": "single",
        },
        rowClassRules={
            # "bg-secondary": "params.data.well == 'A2'",
            # "text-info fw-bold fs-5": "params.data.well == 'A1'",
            "fw-bold": "params.data.amino_acid_substitutions == '#PARENT#'",
            # "text-warning fw-bold fs-5": "['#PARENT#'].includes(
            # params.data.amino_acid_substitutions)",
        },
    )


def get_table_all_experiments():
    return dag.AgGrid(
        id="id-table-all-experiments",
        # rowData=data.to_dict("records"),
        columnDefs=get_all_experiments_column_defs(),
        # TODO: update this correctly
        defaultColDef={
            # do NOT set "flex": 1 in default col def as it overrides all
            # the column widths
            "sortable": True,
            "resizable": True,
            "filter": True,
            # Set BOTH items below to True for header to wrap text
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
            # "flex": 1,  # TODO: remove this after you put fixed width
        },
        columnSize="sizeToFit",
        # style={"height": "600px", "width": "100%"},
        # style={"width": "100%"},
        dashGridOptions={
            "rowSelection": "multiple",  # Enable multiple selection
            "suppressRowClickSelection": True,
            # Use only checkboxes for selection
            "animateRows": True,
        },
    )


def get_protein_viewer():
    return dash_molstar.MolstarViewer(
        id="id-viewer",
        # data=data,
        style={"width": "auto", "height": "600px"},
        layout={
            "layoutShowControls": False,
            "layoutIsExpanded": False,
            # TODO: do we want this option to be true?
        },
    )
