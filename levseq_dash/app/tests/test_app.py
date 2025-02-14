import pytest

from levseq_dash.app import global_strings as gs
from levseq_dash.app import utils


def test_geometry_viewer_type(experiment_ep_pcr_with_user_cas):
    pdb = utils.get_geometry_for_viewer(experiment_ep_pcr_with_user_cas)
    assert pdb["type"] == "mol"


def test_geometry_viewer_format(experiment_ep_pcr_with_user_cas):
    pdb = utils.get_geometry_for_viewer(experiment_ep_pcr_with_user_cas)
    assert pdb["format"] == "mmcif"


def test_geometry_viewer_length(experiment_ep_pcr_with_user_cas):
    pdb = utils.get_geometry_for_viewer(experiment_ep_pcr_with_user_cas)
    assert len(pdb) == 4


def test_gather_residue_count(selected_row_top_variant_table):
    residues = utils.gather_residues_from_selection(selected_row_top_variant_table)
    assert len(residues) == 2


def test_gather_residue(selected_row_top_variant_table):
    residues = utils.gather_residues_from_selection(selected_row_top_variant_table)
    assert residues[0] == "99"
    assert residues[1] == "118"


@pytest.mark.parametrize(
    "residue, length",
    [
        ("K99R R118C", 1),
        ("K99", 0),
        ("99R*", 0),
    ],
)
def test_gather_residue_errors(residue, length):
    """
    assumption: residues must be in the format Letter-Number-Letter format
    """
    residues = utils.gather_residues_from_selection([{"amino_acid_substitutions": residue}])
    assert len(residues) == length


@pytest.mark.parametrize(
    "residue, numbers",
    [
        ("K99R_R118C", [99, 118]),
        ("A59L", [59]),
        ("C81T_T86A_A108G", [81, 86, 108]),
    ],
)
def test_gather_residue_errors(residue, numbers):
    """
    tests the molstar selection and focus functions
    """
    residues = utils.gather_residues_from_selection([{gs.c_substitutions: residue}])
    sel, foc = utils.get_selection_focus(residues)
    assert sel["mode"] == "select"
    assert sel["targets"][0]["residue_numbers"] == numbers
    assert foc["analyse"]


@pytest.mark.parametrize(
    "cas, plate, mean",
    [
        ("345905-97-7", "20240422-ParLQ-ep1-300-1", 1823393.4415588235),
        ("345905-97-7", "20240422-ParLQ-ep1-300-2", 599238.9788096774),
        ("345905-97-7", "20240422-ParLQ-ep1-500-1", 737378.5054485715),
        ("345905-97-7", "20240422-ParLQ-ep1-500-2", 740058.0916967741),
        ("345905-97-7", "20240502-ParLQ-ep2-300-1", 555981.8641939394),
        ("345905-97-7", "20240502-ParLQ-ep2-300-2", 363747.4904807692),
        ("345905-97-7", "20240502-ParLQ-ep2-300-3", 472821.28098),
        ("345905-97-7", "20240502-ParLQ-ep2-500-1", 385903.38386190473),
        ("345905-97-7", "20240502-ParLQ-ep2-500-2", 273690.4014826087),
        ("345905-97-7", "20240502-ParLQ-ep2-500-3", 578947.396785),
        ("395683-37-1", "20240422-ParLQ-ep1-300-1", 1340097.0553558823),
        ("395683-37-1", "20240422-ParLQ-ep1-300-2", 574284.2879645161),
        ("395683-37-1", "20240422-ParLQ-ep1-500-1", 748629.7012771429),
        ("395683-37-1", "20240422-ParLQ-ep1-500-2", 695933.5473419355),
        ("395683-37-1", "20240502-ParLQ-ep2-300-1", 416383.57166363636),
        ("395683-37-1", "20240502-ParLQ-ep2-300-2", 330711.85486538464),
        ("395683-37-1", "20240502-ParLQ-ep2-300-3", 380189.44049999997),
        ("395683-37-1", "20240502-ParLQ-ep2-500-1", 325416.7923809524),
        ("395683-37-1", "20240502-ParLQ-ep2-500-2", 216320.55895652174),
        ("395683-37-1", "20240502-ParLQ-ep2-500-3", 530547.46612),
    ],
)
def test_calculate_group_mean(experiment_ep_pcr, cas, plate, mean):
    df = utils.calculate_group_mean_ratios_per_cas_and_plate(experiment_ep_pcr.data_df)
    col_count = 11
    assert df.shape[0] == 1920
    assert df.shape[1] == col_count  # added columns
    plate_per_cas_data_per = df[(df[gs.c_cas] == cas) & (df[gs.c_plate] == plate)]  # Filter the row
    assert plate_per_cas_data_per.shape[0] == 96  # plate count expectation
    assert plate_per_cas_data_per.shape[1] == col_count
    assert plate_per_cas_data_per.iloc[0]["mean"] == mean
    assert (plate_per_cas_data_per["mean"].dropna() == mean).all()

    # ratio must be increasing. this ensures the ranking was done within group
    plate_per_cas_data_per.fillna(0)
    plate_per_cas_data_per = plate_per_cas_data_per.sort_values(by="ratio", ascending=True)
    assert plate_per_cas_data_per["ratio"].dropna().is_monotonic_increasing
