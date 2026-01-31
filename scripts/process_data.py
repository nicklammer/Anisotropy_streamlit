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


def compile_anisotropy(df_anisotropy, table_samples, titration_direction) -> pd.DataFrame:
    # Compiles anisotropy and concentration data for each sample
    
    # Transpose input data if titrations were performed column-wise
    if titration_direction == "Columns":
        df_anisotropy = df_anisotropy.T

    df_sample_data = table_samples.apply(
        get_data_over_titration,
        axis=1,
        args=(df_anisotropy, titration_direction))

    return df_sample_data


def get_data_over_titration(row, df_anisotropy, titration_direction):

    # unpack row
    titration_idx = row["Titration row/column"]
    titration_range = row["Titration range"]
    excluded_wells = row["Excluded wells"]
    starting_conc = row["Starting concentration"]
    dilution_factor = row["Dilution factor"]

    # get row from input dataframe
    anisotropy_row = df_anisotropy.loc[titration_idx]

    # parse titration range
    titration_range_split = titration_range.split("-")

    if titration_direction == "Rows":
        # Row-wise is default and range works for column names
        titration_indices = get_titration_indices_row(titration_range_split)

    elif titration_direction == "Columns":
        # Column-wise is alt method and requires more work to get a range (because of alphabetical indices)
        column_labels = df_anisotropy.columns.values
        titration_indices = get_titration_indices_column(titration_range_split, column_labels)
    # This check should happen in a dedicated input validation function
    else:
        raise Exception("Titration direction is required.")

    # subset row of data using list of column names/indices
    anisotropy_row = anisotropy_row.loc[titration_indices]

    # calculate serial dilution over titration range
    concentration_list = [starting_conc / (dilution_factor ** i) for i in range(len(anisotropy_row))]
    # create pd.Series to mirror the data row above
    concentration_row = pd.Series(concentration_list, index=anisotropy_row.index)

    # drop excluded wells
    if excluded_wells:
        excluded_wells_list = [well.strip() for well in excluded_wells.split(",")]
        anisotropy_row = anisotropy_row.drop(labels=excluded_wells_list, errors='ignore')
        concentration_row = concentration_row.drop(labels=excluded_wells_list, errors='ignore')

    return pd.Series({
        "unique name": row["unique name"],
        "concentration": concentration_row.to_list(),
        "anisotropy": anisotropy_row.to_list()
    })

def get_titration_indices_row(titration_range_split):

    return [str(t) for t in range(int(titration_range_split[0]), int(titration_range_split[1]) + 1)]

def get_titration_indices_column(titration_range_split, column_labels):

    start_idx = 0
    end_idx = -1
    
    for i, label in enumerate(column_labels):
        # Get alphabet labels, record indices within array of labels
        if label == titration_range_split[0]:
            start_idx = i
        
        if label == titration_range_split[1]:
            end_idx = i

    # Get labels required for titration range
    return column_labels[start_idx:end_idx]