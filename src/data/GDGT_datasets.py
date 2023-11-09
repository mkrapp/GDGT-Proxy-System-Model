import sys
sys.path.append("../src")

import pandas as pd
import numpy as np

from sklearn.datasets._base import Bunch, _convert_data_dataframe, validate_params

from importlib.resources import read_text

DATA_MODULE = "GDGT-Proxy-System-Model.src.data"
DESCR_MODULE = "data"

# standard names
AGE       = "Age (Ma)"
LATITUDE  = "Latitude"
LONGITUDE = "Longitude"
SST       = "SST"

@validate_params(
    {"return_X_y": ["boolean"], "as_frame": ["boolean"]},
    prefer_skip_nested_validation=True,
)
def load_rattanasriampaipong2022(*, modern=True, return_X_y=False, as_frame=False):

    data_file_name = "../data/external/pnas.2123193119.sd02.xlsx"

    df = pd.read_excel(data_file_name,index_col=0)
    
    # sst_name = "Sea Surface Temp"
    sst_name = "WOA18_decav_SST"
    
    # Mapping of column names
    col_map = {
        "cal_frac_1302": "GDGT-0",
        "cal_frac_1300": "GDGT-1",
        "cal_frac_1298": "GDGT-2",
        "cal_frac_1296": "GDGT-3",
        "cal_frac_1292": "Crenarchaeol",
        "cal_frac_1292_iso": "Cren'",
        sst_name: SST
        }
    
    age_str = "Modern" if modern else "Ancient"
    class_str = "sediment-totalGDGTs" if modern else "paleoGDGTs"
    
    if not modern:
        df[LATITUDE] = df["paleolat"].values
        df[LONGITUDE] = df["paleolon"].values
    
    df = df[np.logical_and(df["dataType_level0"] == age_str,df["lipidClass"] == class_str)]
    df[AGE] = df["sampleAge"].values

    df = df.rename(columns=col_map)

    compound_names = df.columns[19:25]

    idx = ~(df[compound_names]==0).any(axis=1)

    columns = list(compound_names)+[SST,AGE,LONGITUDE,LATITUDE]
    df = df[columns].loc[idx]

    if modern:
        df = df.dropna(axis=0)
        df = df.drop([108, 110, 120])
    else:
        df = df.sort_values(AGE)
        
    df = df.astype(np.float64)
        
    feature_columns = list(compound_names)+[AGE,LONGITUDE,LATITUDE]
    
    data, target, feature_names, target_names = df[feature_columns].values, df[SST].values, feature_columns, [SST]

    fdescr = read_text(DESCR_MODULE, "rattanasriampaipong2022.rst")

    frame = None
    target_columns = [
        SST,
    ]
    if as_frame:
        frame, data, target = _convert_data_dataframe(
            "load_rattanasriampaipong2022", data, target, feature_names, target_columns
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


@validate_params(
    {"return_X_y": ["boolean"], "as_frame": ["boolean"]},
    prefer_skip_nested_validation=True,
)
def load_duncan2023(*, modern=True, return_X_y=False, as_frame=False):
    data_file_name = "../data/external/GDGTdata_Antarctica_220923.xlsx"
    
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
        df = pd.read_excel(data_file_name, sheet_name="iso modern cal" ,skiprows=1).dropna()
        df[AGE] = 0.0

        compound_names = df.columns[2:8]

        idx = ~(df[compound_names]==0).any(axis=1)
        columns = list(compound_names)+[sst_name,AGE,LONGITUDE,LATITUDE]
        df[LATITUDE] = df["latitude"].values
        df[LONGITUDE] = df["longitude"].values
        df = df[columns].loc[idx]
    else:
        df = pd.read_excel(data_file_name, sheet_name="Combined")
        df[sst_name] = np.nan
        df[LATITUDE] = df["Latitude (approx paleo)"].values
        df[LONGITUDE] = df["Longitude (approx paleo)"].values
        
        df = df.rename(columns=col_map)

        df = df.drop(1304)
        
        compound_names = df.columns[8:14]

        idx = ~(df[compound_names]==0).any(axis=1)
        columns = list(compound_names)+[sst_name,AGE,LONGITUDE,LATITUDE]
        df = df[columns].loc[idx]
        
        df = df.sort_values(AGE)
    
    feature_columns = list(compound_names)+[AGE,LONGITUDE,LATITUDE]
    
    data, target, feature_names, target_names = df[feature_columns].values, df[sst_name].values, feature_columns, [SST]

    fdescr = read_text(DESCR_MODULE, "duncan2023.rst")

    frame = None
    target_columns = [
        SST,
    ]
    if as_frame:
        frame, data, target = _convert_data_dataframe(
            "load_duncan2023", data, target, feature_names, target_columns
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