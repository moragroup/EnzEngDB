from pathlib import Path

import pandas as pd
import pytest

from levseq_dash.app import global_strings as gs
from levseq_dash.app.experiment import Experiment, MutagenesisMethod

package_root = Path(__file__).resolve().parent.parent.parent

path_assay = package_root / "app" / "tests" / "data" / "assay_measure_list.csv"
path_exp_ep_data = package_root / "app" / "tests" / "data" / "flatten_ep_processed_xy_cas.csv"
path_exp_ep_cif = package_root / "app" / "tests" / "data" / "flatten_ep_processed_xy_cas_row8.cif"

path_exp_ssm_data = package_root / "app" / "tests" / "data" / "flatten_ssm_processed_xy_cas.csv"
path_exp_ssm_cif = package_root / "app" / "tests" / "data" / "flatten_ssm_processed_xy_cas_row3.cif"

test_assay_list = (pd.read_csv(path_assay, encoding="utf-8", usecols=["Technique"]))["Technique"].tolist()

experiment_ep_example = Experiment(
    data_df=pd.read_csv(path_exp_ep_data, usecols=gs.experiment_core_data_list),
    experiment_name="ep_file",
    experiment_date="TBD",
    mutagenesis_method=MutagenesisMethod.epPCR,
    geometry_file_path=path_exp_ep_cif,
    assay=test_assay_list[2],
)

experiment_ssm_example = Experiment(
    data_df=pd.read_csv(path_exp_ssm_data, usecols=gs.experiment_core_data_list),
    experiment_name="ssm_file",
    experiment_date="TBD",
    mutagenesis_method="SSM",
    geometry_file_path=path_exp_ssm_cif,
    assay=test_assay_list[1],
)


@pytest.fixture(scope="session")
def assay_list():
    return test_assay_list


@pytest.fixture(scope="session")
def experiment_empty():
    return Experiment()


@pytest.fixture(scope="session")
def experiment_ep_pcr():
    return experiment_ep_example


@pytest.fixture(scope="session")
def experiment_ep_pcr_with_user_cas():
    return Experiment(
        data_df=pd.read_csv(path_exp_ep_data, usecols=gs.experiment_core_data_list),
        experiment_name="ep_file",
        experiment_date="TBD",
        # these are RANDOM cas numbers for test only
        substrate_cas_number=["918704-25-2", "98053-92-1"],
        product_cas_number=["597635-11-3", "605026-90-8", "650843-51-7"],
        mutagenesis_method=MutagenesisMethod.epPCR,
        geometry_file_path=path_exp_ep_cif,
        assay=test_assay_list[3],
    )
