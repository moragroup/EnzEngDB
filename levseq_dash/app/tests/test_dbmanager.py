import pandas as pd
import pytest

from levseq_dash.app import utils


def test_db_load(dbmanager_read_all_from_file):
    assert len(dbmanager_read_all_from_file.experiments_dict) == 6
    assert len(dbmanager_read_all_from_file.assay_list) == 24


@pytest.mark.parametrize(
    "index",
    [0, 1, 2, 3, 4, 5],
)
def test_db_delete(dbmanager_read_all_from_file, index):
    assert len(dbmanager_read_all_from_file.experiments_dict) == 6
    assert dbmanager_read_all_from_file.delete_experiment(index)
    assert len(dbmanager_read_all_from_file.experiments_dict) == 5


def test_db_get_lab_experiments_with_meta_data_general(dbmanager_read_all_from_file):
    data_list_of_dict = dbmanager_read_all_from_file.get_lab_experiments_with_meta_data()
    assert len(data_list_of_dict) == 6
    df = pd.DataFrame.from_records(data_list_of_dict)
    assert df.shape[0] == 6
    assert df.shape[1] == 13


@pytest.mark.parametrize(
    "index,name,n_plates, n_unique_cas",
    [
        (0, "flatten_ep_processed_xy_cas.csv", 10, 2),
        (1, "flatten_ssm_processed_xy_cas.csv", 4, 1),
        (2, "mod_test_1_ssm.csv", 7, 1),
        (3, "mod_test_2_ssm.csv", 1, 1),
        (4, "mod_test_3_ssm.csv", 6, 1),
        (5, "mod_test_4_v2_ep.csv", 6, 1),
    ],
)
def test_db_get_lab_experiments_with_meta_data_data(dbmanager_read_all_from_file, index, name, n_plates, n_unique_cas):
    list_of_all_lab_experiments_with_meta = dbmanager_read_all_from_file.get_lab_experiments_with_meta_data()
    sorted_list = sorted(list_of_all_lab_experiments_with_meta, key=lambda x: x["experiment_name"])
    assert sorted_list[index]["experiment_name"] == name
    assert sorted_list[index]["plates_count"] == n_plates
    assert len(sorted_list[index]["unique_cas_in_data"]) == n_unique_cas


@pytest.mark.parametrize(
    "index",
    [0, 1, 2, 3, 4, 5],
)
def test_extract_all_unique_cas_from_lab_data(dbmanager_read_all_from_file, index):
    list_of_all_lab_experiments_with_meta = dbmanager_read_all_from_file.get_lab_experiments_with_meta_data()

    all_cas = utils.extract_all_unique_cas_from_lab_data(list_of_all_lab_experiments_with_meta)
    assert len(all_cas) != 0
    # get the substrate_cas from the test data and make sure they are found in the unique list
    cas_list = list_of_all_lab_experiments_with_meta[index]["substrate_cas_number"].split(",")
    assert (all_cas.find(c) != -1 for c in cas_list)
