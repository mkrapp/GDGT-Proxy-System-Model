import pandas as pd
import numpy as np

def load_duncan(age_max = 0.16):
    fnm_excel = "../data/external/GDGTdata_Antarctica_220923.xlsx"

    sheet_name = "iso modern cal"
    # sheet_name = "SO Modern data"
    df_calib = pd.read_excel(fnm_excel, sheet_name=sheet_name,skiprows=1).dropna()
    df_calib["Age (Ma)"] = 0.0
    df_calib["calibration"] = True

    sst_name = "Sea Surface Temp"

    if sheet_name == "SO Modern data":
        compound_names = df_calib.columns[4:10]
    else:
        compound_names = df_calib.columns[2:8]

    idx_calib = ~(df_calib[compound_names]==0).any(axis=1)

    df_ceno = pd.read_excel(fnm_excel, sheet_name="Combined")

    sst_name_ceno = "Sea Surface Temp"

    # Mapping of column names
    col_map = {
        1302: "GDGT-0",
        1300: "GDGT-1",
        1298: "GDGT-2",
        1296: "GDGT-3",
        1292: "Crenarchaeol",
        "1292'": "Cren'",
        sst_name_ceno: sst_name
        }

    df_ceno[sst_name_ceno] = np.nan
    df_ceno["latitude"] = df_ceno["Latitude (approx paleo)"].values
    df_ceno["calibration"] = False

    df_ceno = df_ceno.rename(columns=col_map)

    df_ceno = df_ceno.drop(1304)
    # filter and sort by age
    df_ceno = df_ceno[df_ceno["Age (Ma)"]<=age_max]
    df_ceno_ = df_ceno.sort_values("Age (Ma)")
    age = df_ceno_["Age (Ma)"]

    compound_names = df_ceno_.columns[8:14]

    idx_ceno = ~(df_ceno_[compound_names]==0).any(axis=1)

    columns = list(compound_names)+[sst_name,"Age (Ma)","calibration","latitude"]

    return compound_names, sst_name, pd.concat([df_ceno_[columns].loc[idx_ceno],df_calib[columns].loc[idx_calib]],axis=0)

