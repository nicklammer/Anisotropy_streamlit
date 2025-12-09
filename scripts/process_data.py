# Process plate data

import pandas as pd
import numpy as np

def drop_empty_rows_columns(df_input):
    df_output = df_input.dropna(axis=1, how="all")
    df_output = df_output.dropna(axis=0, how="all")

    return df_output

def calculate_anisotropy(df_parallel, df_perpendicular):
    # Check if both dataframes have the same shape
    if df_parallel.shape != df_perpendicular.shape:
        raise ValueError("Data layout for both tables must match.")

    # Define the anisotropy calculation function
    def _anisotropy_equation(parallel_value, perpendicular_value):
        return ((parallel_value-perpendicular_value)/(parallel_value + 2 * perpendicular_value))

    # Calculate anisotropy for each element where both values are not NaN
    none_mask = df_parallel.notna() & df_perpendicular.notna()
    df_anisotropy = pd.DataFrame(
        np.where(none_mask, 
                 _anisotropy_equation(df_parallel, df_perpendicular), 
                 np.nan),
        index=df_parallel.index,
        columns=df_parallel.columns
    )

    return df_anisotropy

def convert_df_to_dict(df_anisotropy, table_samples, titration_direction) -> pd.DataFrame:
    # Converts dataframe containing anisotropy data to dictionaries

    combined_dict = {
        "unique name": [],
        "concentration": [],
        "anisotropy": []
    }

    # Assume titration in rows for this
    # TODO: This will need cleaning up after i know it works
    for _, row in table_samples.iterrows():
        # unpack row
        unique_name = row["unique name"]
        titration_idx = row["Titration row/column"]
        titration_range = row["Titration range"]
        excluded_wells = row["Excluded wells"]
        starting_conc = row["Starting concentration"]
        dilution_factor = row["Dilution factor"]

        anisotropy_row = df_anisotropy.loc[titration_idx]

        titration_range = titration_range.split("-")
        titration_indices = [str(t) for t in range(int(titration_range[0]), int(titration_range[1]) + 1)]
        anisotropy_row = anisotropy_row.loc[titration_indices]

        concentration_list = [starting_conc / (dilution_factor ** i) for i in range(len(anisotropy_row))]
        concentration_row = pd.Series(concentration_list, index=anisotropy_row.index)

        if excluded_wells:
            excluded_wells = excluded_wells.split(",")
            excluded_wells = [well.strip() for well in excluded_wells]

            anisotropy_row = anisotropy_row.drop(labels=excluded_wells)
            concentration_row = concentration_row.drop(labels=excluded_wells)

        combined_dict["unique name"].append(unique_name)
        combined_dict["concentration"].append(concentration_row.to_list())
        combined_dict["anisotropy"].append(anisotropy_row.to_list())
        # anisotropy_dict[unique_name] = anisotropy_row.to_list()
        # concentration_dict[unique_name] = concentration_row.to_list()
    
    df_sample_data = pd.DataFrame.from_dict(combined_dict)

    return df_sample_data


def fit_plot_anisotropy(data_dict, fit_dict, plot_dict, style_dict):
    # should this process 1 sample or have a loop integrated?

    # drop columns and rows that only contain NA/None value in input tables
    return None


def get_titration_indices_row():
    return NotImplementedError

def get_titration_indices_column():
    return NotImplementedError