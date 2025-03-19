from levseq_dash.app import global_strings as gs
from levseq_dash.app import vis


def get_top_variant_column_defs(df):
    """
    Returns column definitions and setup for dash ag grid table per experiment
    """
    return [
        {
            "field": gs.c_cas,
            "headerName": "CAS #",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            # flex allows the resizing to be dynamic
            "flex": 2,
        },
        {
            "field": gs.c_plate,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 2,
        },
        {
            "field": gs.c_well,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 80,
        },
        {
            "field": gs.c_substitutions,
            "headerName": "Sub",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 2,
        },
        {
            "field": gs.c_fitness_value,
            "headerName": "Fitness",
            "initialSort": "desc",
            "filter": "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 2,
            # "cellStyle": {"styleConditions": vis.data_bars_colorscale(df, gs.c_fitness_value)},
        },
        {
            "field": "ratio",
            "filter": "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 2,
            "cellStyle": {"styleConditions": vis.data_bars_group_mean_colorscale(df)},
        },
    ]


def get_all_experiments_column_defs():
    """
    Returns column definitions and setup for dash ag grid table for all experiments
    """
    return [
        {  # Checkbox column
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
            "headerName": "",
            "width": 30,
            # "flex": 1,
        },
        {
            "field": "experiment_id",
            "headerName": "ID",
            "filter": "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 2,
        },
        {
            "field": "experiment_name",
            "headerName": "Name",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 3,
        },
        {
            "field": "experiment_date",
            "headerName": "Date",
            "filter": "agDateColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 4,
        },
        {
            "field": "upload_time_stamp",
            "headerName": "Uploaded",
            "filter": "agDateColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 4,
        },
        {
            "field": "substrate_cas_number",
            "headerName": "Sub CAS",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 3,
        },
        {
            "field": "product_cas_number",
            "headerName": "Prod CAS",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 4,
        },
        {
            "field": "assay",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 4,
        },
        {
            "field": "mutagenesis_method",
            "headerName": "Mutagenesis Method",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 4,
        },
        {
            "field": "plates_count",
            "headerName": "#Plates",
            "filter": "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "flex": 2,
        },
    ]


def get_matched_sequences_column_defs():
    """
    Returns column definitions for the matched sequences
    """
    return [
        {  # Checkbox column
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
            "headerName": "",
            "width": 30,
        },
        {
            "field": "target_name",
            "headerName": "Experiment ID",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 150,
        },
        {
            "field": "alignment_score",
            "filter": "agNumberColumnFilter",
            "headerName": "Raw Alignment Score",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 150,
        },
        {
            "field": "norm_score",
            "initialSort": "desc",
            "headerName": "Normed Score",
            "filter": "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 150,
        },
        {
            "field": "identities",
            "filter": "agNumberColumnFilter",
            "#headerName": "# matches",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 110,
        },
        {
            "field": "gaps",
            "filter": "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 110,
        },
        {
            "field": "mismatches",
            "filter": "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 130,
        },
        {
            "field": "coordinates",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 150,
            "cellRenderer": "addLineBreaksOnArrayRow",
            "autoHeight": True,
        },
        {
            "field": "alignment",
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "width": 650,
            "cellRenderer": "addLineBreaksOnNewLines",
            "autoHeight": True,
        },
        # {
        #     "field": "indices",
        #     "filterParams": {"buttons": ["reset", "apply"], "closeOnApply": True, },
        #     "width": 2000,
        #     'cellRenderer': "addLineBreaksOnArrayRow",
        #     "autoHeight": True,
        # },
    ]
