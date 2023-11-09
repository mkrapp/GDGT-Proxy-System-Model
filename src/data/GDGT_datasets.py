import sys
sys.path.append("../")

import pandas as pd
import numpy as np

from sklearn.datasets._base import Bunch, _convert_data_dataframe, validate_params
from sklearn.datasets import load_diabetes, load_iris

from importlib.resources import read_text

DATA_MODULE = "GDGT-Proxy-System-Model.src.data"
DESCR_MODULE = "src.data"

def load_excel_data(modern=True):
    fnm_excel = "../data/external/GDGTdata_Antarctica_220923.xlsx"
    
    sst_name = "Sea Surface Temp"

    # Mapping of column names
    col_map = {
        1302: "GDGT-0",
        1300: "GDGT-1",
        1298: "GDGT-2",
        1296: "GDGT-3",
        1292: "Crenarchaeol",
        "1292'": "Cren'"
        }

    if modern:
        df = pd.read_excel(fnm_excel, sheet_name="iso modern cal" ,skiprows=1).dropna()
        df["Age (Ma)"] = 0.0

        compound_names = df.columns[2:8]

        idx = ~(df[compound_names]==0).any(axis=1)
        columns = list(compound_names)+[sst_name,"Age (Ma)","Longitude","Latitude"]
        df["Latitude"] = df["latitude"].values
        df["Longitude"] = df["longitude"].values
        df = df[columns].loc[idx]
    else:
        df = pd.read_excel(fnm_excel, sheet_name="Combined")
        df[sst_name] = np.nan
        df["Latitude"] = df["Latitude (approx paleo)"].values
        df["Longitude"] = df["Longitude (approx paleo)"].values
        
        df = df.rename(columns=col_map)

        df = df.drop(1304)
        
        compound_names = df.columns[8:14]

        idx = ~(df[compound_names]==0).any(axis=1)
        columns = list(compound_names)+[sst_name,"Age (Ma)","Longitude","Latitude"]
        df = df[columns].loc[idx].sort_values("Age (Ma)")
    
    feature_columns = list(compound_names)+["Age (Ma)","Longitude","Latitude"]
    
    return df[feature_columns].values, df[sst_name].values, feature_columns, ["SST"]


@validate_params(
    {"return_X_y": ["boolean"], "as_frame": ["boolean"]},
    prefer_skip_nested_validation=True,
)
def load_duncan2023(*, modern=True, return_X_y=False, as_frame=False):
    data_file_name = "../data/external/GDGTdata_Antarctica_220923.xlsx"
    data, target, feature_names, target_names = load_excel_data(modern)
    # target, data, target_names, feature_names = load_excel_data()

    fdescr = read_text(DESCR_MODULE, "duncan2023.rst")

    frame = None
    target_columns = [
        "SST",
    ]
    # target_columns = target_names
    if as_frame:
        frame, data, target = _convert_data_dataframe(
            "load_duncan2023_modern", data, target, feature_names, target_columns
        )

    if return_X_y:
        return data, target

    return Bunch(
        data=data,
        target=target,
        frame=frame,
        target_names=target_names,
        DESCR=fdescr,
        feature_names=feature_names,
        filename=data_file_name,
        data_module=DATA_MODULE,
    )