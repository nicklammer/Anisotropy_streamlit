# Placeholder for input validation functions
'''
Need functions for:
if quad fit chosen, requires ligand concentrations for each sample
plot title and filename cannot be empty
style options table can't be empty
'''
import pandas as pd
import numpy as np
import re

from . import helpers


def check_sample_table_formatting(table_samples):
    # validate formatting of sample table inputs

    required_cols = [
        "Sample label",
        "Titration row/column",
        "Titration range",
        "Starting concentration",
        "Dilution factor"
    ]

    # First check for None or empty strings
    for _, row in table_samples.iterrows():
        for col in required_cols:
            if row[col] is None or row[col] == '':
                if col == "Sample label":
                    raise Exception(f"{col} is required. Check sample table.")
                else:
                    raise Exception(f"{col} is required. See sample {row["Sample label"]}.")
                
        # Validate titration range formatting
        # Pattern looks for something like "1-20" or "A-P"
        range_pattern = r"(\d+-\d+)|([A-Z]+-[A-Z]+)"
        if not re.fullmatch(range_pattern, row["Titration range"]):
            raise Exception(f"Invalid titration range for {row["Sample label"]}. Format for range should be like 1-20 or A-M.")
        
        # Validate excluded wells formatting.
        # Pattern looks for something like "1, 2, 3", "1,2,3", "1" or characters
        excluded_pattern = r"((\d+)(,\s*\d+)*)|(([A-Z]+)(,\s*[A-Z]+)*)"
        if row["Excluded wells"] is not None and not re.fullmatch(excluded_pattern, row["Excluded wells"]):
            raise Exception(f"Format of excluded wells is invalid for {row["Sample label"]}. Format should be like 1,2,3 or 1, 2, 3.")

def check_unique_titration_idx(table_samples):
    titration_indices = table_samples["Titration row/column"]
    
    if len(titration_indices) != len(set(titration_indices)):
        raise Exception("Cannot have duplicate values for Titration row/column.")

def check_titration_direction_match(titration_direction, table_samples):
    # If titration direction is Rows, row should be a character with integer columns
    # Opposite for Columns

    idx_format = "alphabetical" if titration_direction == "Rows" else "numerical"
    range_format = "numerical" if titration_direction == "Rows" else "alphabetical"

    idx_pattern = r"[A-Z]+" if titration_direction == "Rows" else r"\d+"
    range_pattern = r"\d+" if titration_direction == "Rows" else r"[A-Z]+"

    for _, row in table_samples.iterrows():
        if not re.fullmatch(idx_pattern, row["Titration row/column"]):
            raise Exception(f"Titration row/column for {row["Sample label"]} should be {idx_format}.")
        
        range_split = row["Titration range"].split("-")
        if not re.fullmatch(range_pattern, range_split[0]):
            raise Exception(f"Titration range for {row["Sample label"]} should be {range_format}.")
        
        if row["Excluded wells"] is not None:
            excluded_wells = [well.strip() for well in row["Excluded wells"].split(",")]
            if not re.fullmatch(range_pattern, excluded_wells[0]):
                raise Exception(f"Excluded wells for {row["Sample label"]} should be {range_format}.")


def check_ligand_concentration(table_samples):
    # If using the quad fit, ligand concentration is required
    # should only run if quad fit is chosen

    ligand_conc = table_samples["Ligand concentration"]

    if None in ligand_conc:
        raise Exception("Ligand concentration is required for quadratic fit.")
    
    if 0 in ligand_conc:
        raise Exception("Ligand concentration must be greater than zero.")


def check_empty_dataframe(df, tag):

    # TODO: Is this how this works?
    if df.empty():
        raise Exception(f"{tag} is empty.")

def check_data_shape(df_parallel, df_perpendicular):
    # Check if both dataframes have the same shape
    if df_parallel.shape != df_perpendicular.shape:
        raise ValueError("Data layout for both tables must match.")

def check_data_ranges(df, table_samples, titration_direction):
    # given df, row/column, and ranges, check for None

    if titration_direction == "Columns":
        df = df.T

    for _, row in table_samples.iterrows():
        sample = row["Sample label"]
        titration_idx = row["Titration row/column"]
        titration_range = row["Titration range"]

        # get row from input dataframe
        try:
            row_data = df.loc[titration_idx]
        except:
            raise Exception(f"Invalid titration row/column for {sample}.")

        # parse titration range
        titration_range_split = titration_range.split("-")

        if titration_direction == "Rows":
            # Row-wise is default and range works for column names
            titration_indices = helpers.get_titration_indices_row(titration_range_split)

        else:
            # Column-wise is alt method and requires more work to get a range (because of alphabetical indices)
            column_labels = df.columns.values
            titration_indices = helpers.get_titration_indices_column(
                titration_range_split, column_labels
        )
            
        # subset row of data using list of column names/indices
        row_data = row_data.loc[titration_indices]

        # if row contains none/nan raise exception
        if any(row_data.isna()):
            raise Exception(f"Titration range for {sample} invalid.")
