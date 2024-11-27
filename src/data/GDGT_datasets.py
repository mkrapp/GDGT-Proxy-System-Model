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
GDGT      = ["GDGT-0", "GDGT-1", "GDGT-2", "GDGT-3", "Crenarchaeol", "Cren'"]

@validate_params(
        {"return_X_y": ["boolean"], "as_frame": ["boolean"]},
        prefer_skip_nested_validation=True,
        )
def load_varma2024(*, return_X_y=False, as_frame=False):

    data_file_name = "../data/external/DAS_ohgdgt_surfacesediment_data.xlsx"

    df = pd.read_excel(data_file_name,sheet_name="Table",skiprows=1,usecols="C,D,F,H:M")

    # Mapping of column names
    col_map = {
            "fGDGT-0": "GDGT-0",
            "fGDGT-1": "GDGT-1",
            "fGDGT-2": "GDGT-2",
            "fGDGT-3": "GDGT-3",
            "fcren": "Crenarchaeol",
            "fcren'": "Cren'",
            "Longitude": LONGITUDE,
            "Latitude": LATITUDE,
            "Annual mean SST (°C)a": SST
            }

    df = df.rename(columns=col_map)

    idx = ~(df[GDGT]==0).any(axis=1)

    columns = GDGT+[SST,LONGITUDE,LATITUDE]
    df = df[columns].loc[idx]

    df = df.dropna(axis=0)

    df = df.astype(np.float64)

    feature_columns = GDGT+[LONGITUDE,LATITUDE]

    data, target, feature_names, target_names = df[feature_columns].values, df[SST].values, feature_columns, [SST]

    fdescr = read_text(DESCR_MODULE, "varma2024.rst")

    frame = None
    target_columns = [
            SST,
            ]
    if as_frame:
        frame, data, target = _convert_data_dataframe(
                "load_varma2024", data, target, feature_names, target_columns
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
def load_tierney2015(*, return_X_y=False, as_frame=False):

    data_file_name = "../data/external/tierney2015tex86.txt"

    df = pd.read_csv(data_file_name,sep="\t",comment="#",na_values=[-999])

    # Mapping of column names
    col_map = {
            "fGDGT_0": "GDGT-0",
            "fGDGT_1": "GDGT-1",
            "fGDGT_2": "GDGT-2",
            "fGDGT_3": "GDGT-3",
            "fGDGT_cren": "Crenarchaeol",
            "fGDGT_cren'": "Cren'",
            "longitude": LONGITUDE,
            "latitude": LATITUDE,
            "WOA09_SST": SST
            }

    df = df.rename(columns=col_map)

    idx = ~(df[GDGT]==0).any(axis=1)

    columns = GDGT+[SST,LONGITUDE,LATITUDE]
    df = df[columns].loc[idx]

    df = df.dropna(axis=0)

    df = df.astype(np.float64)

    feature_columns = GDGT+[LONGITUDE,LATITUDE]

    data, target, feature_names, target_names = df[feature_columns].values, df[SST].values, feature_columns, [SST]

    fdescr = read_text(DESCR_MODULE, "tierney2015.rst")

    frame = None
    target_columns = [
            SST,
            ]
    if as_frame:
        frame, data, target = _convert_data_dataframe(
                "load_tierney2015", data, target, feature_names, target_columns
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
def load_rattanasriampaipong2022(*, modern=True, return_X_y=False, as_frame=False):

    data_file_name = "../data/external/pnas.2123193119.sd02.xlsx"

    df = pd.read_excel(data_file_name,index_col=0)

    # Mapping of column names
    col_map = {
            "cal_frac_1302": "GDGT-0",
            "cal_frac_1300": "GDGT-1",
            "cal_frac_1298": "GDGT-2",
            "cal_frac_1296": "GDGT-3",
            "cal_frac_1292": "Crenarchaeol",
            "cal_frac_1292_iso": "Cren'",
            "WOA18_decav_SST": SST
            }

    age_str = "Modern" if modern else "Ancient"
    class_str = "sediment-totalGDGTs" if modern else "paleoGDGTs"

    if not modern:
        df[LATITUDE] = df["paleolat"].values
        df[LONGITUDE] = df["paleolon"].values

    df = df[np.logical_and(df["dataType_level0"] == age_str,df["lipidClass"] == class_str)]
    df[AGE] = df["sampleAge"].values

    df = df.rename(columns=col_map)

    idx = ~(df[GDGT]==0).any(axis=1)

    columns = GDGT+[SST,AGE,LONGITUDE,LATITUDE]
    df = df[columns].loc[idx]

    #if modern:
    #    df = df.dropna(axis=0)
    #    df = df.drop([108, 110, 120])
    if not modern:
        df = df.sort_values(AGE)

    df = df.astype(np.float64)

    feature_columns = GDGT+[AGE,LONGITUDE,LATITUDE]

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
def load_duncan2023(*, modern=True, remove_zeros=False, return_X_y=False, as_frame=False):
    data_file_name = "../data/external/GDGTdata_Antarctica_220923.xlsx"

    if modern:
        df = pd.read_excel(data_file_name, sheet_name="iso modern cal" ,skiprows=1).dropna()
        df[AGE] = 0.0

        idx = ~(df[GDGT]==0).any(axis=1)
        columns = GDGT+[SST,AGE,LONGITUDE,LATITUDE]
        df[LATITUDE] = df["latitude"].values
        df[LONGITUDE] = df["longitude"].values
        df[SST]       = df["Sea Surface Temp"].values
        if remove_zeros:
            df = df[columns].loc[idx]
        else:
            df = df[columns]
    else:
        df = pd.read_excel(data_file_name, sheet_name="Combined")

        # Mapping of column names
        col_map = {
                1302: "GDGT-0",
                1300: "GDGT-1",
                1298: "GDGT-2",
                1296: "GDGT-3",
                1292: "Crenarchaeol",
                "1292'": "Cren'"
                }
        df = df.rename(columns=col_map)

        df[SST] = np.nan
        df[LATITUDE] = df["Latitude (approx paleo)"].values
        df[LONGITUDE] = df["Longitude (approx paleo)"].values

        df = df.drop(1304)

        idx = ~(df[GDGT]==0).any(axis=1)
        columns = GDGT+[SST,AGE,LONGITUDE,LATITUDE]
        if remove_zeros:
            df = df[columns].loc[idx]
        else:
            df = df[columns]

        df = df.sort_values(AGE)

    feature_columns = GDGT+[AGE,LONGITUDE,LATITUDE]

    data, target, feature_names, target_names = df[feature_columns].values, df[SST].values, feature_columns, [SST]

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
