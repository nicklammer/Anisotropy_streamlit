# helper functions and variables
import streamlit as st
import pandas as pd
from string import ascii_uppercase
from math import ceil

import plot_styles

column_config_data_plate = dict(
    [(str(column), st.column_config.NumberColumn()) for column in range(1, 25)]
)

column_config_sample_table = {
    "Sample label": st.column_config.TextColumn(),
    "Titration row/column": st.column_config.TextColumn(),
    "Titration range": st.column_config.TextColumn(),
    "Starting concentration": st.column_config.NumberColumn(),
    "Dilution factor": st.column_config.NumberColumn(),
    "Ligand concentration": st.column_config.NumberColumn(),
    "Units": st.column_config.SelectboxColumn(options=["nM", "uM", "mM"], default="nM"),
    "Excluded wells": st.column_config.TextColumn(),
}

# column config for style table is in the style table function

# def create_column_config_style_table():
# {
#     "Sample": st.column_config.TextColumn(),
#     "Color": st.column_config.SelectboxColumn(
#         options=list(plot_styles.color_dict.keys())
#     ),
#     "Marker style": st.column_config.SelectboxColumn(
#         options=list(plot_styles.marker_dict.keys())
#     ),
#     "Line style": st.column_config.SelectboxColumn(
#         options=list(plot_styles.line_dict.keys())
#     ),
# }


def generate_empty_plate() -> pd.DataFrame:
    # Generate a table based on a 384-well plate

    # Get A-P in a list
    ROW_IDX = [letter for letter in ascii_uppercase[0:16]]

    COLUMNS = range(1, 25)

    plate_dict = dict([(column, [None] * 16) for column in COLUMNS])

    empty_plate = pd.DataFrame.from_dict(plate_dict)

    empty_plate.set_index(pd.Series(ROW_IDX), inplace=True)

    return empty_plate


def generate_sample_table() -> pd.DataFrame:
    # Generate sample info table

    empty_column = [None] #* number_of_samples

    table_dict = {
        "Sample label": empty_column,
        "Titration row/column": empty_column,
        "Titration range": empty_column,
        "Starting concentration": empty_column,
        "Dilution factor": empty_column,
        "Ligand concentration": empty_column,
        "Units": ["nM"],
        "Excluded wells": empty_column,
    }

    sample_table = pd.DataFrame.from_dict(table_dict)

    return sample_table


def generate_plot_style_table(sample_names, num_of_plots) -> tuple:
    # Generate table for choosing line and marker styles

    color_names = list(plot_styles.color_dict.keys())
    marker_names = list(plot_styles.marker_dict.keys())
    line_names = list(plot_styles.line_dict.keys())

    column_config = {
        "Sample": st.column_config.TextColumn(),
        "Color": st.column_config.SelectboxColumn(
            options=list(plot_styles.color_dict.keys())
        ),
        "Marker style": st.column_config.SelectboxColumn(
            options=list(plot_styles.marker_dict.keys())
        ),
        "Line style": st.column_config.SelectboxColumn(
            options=list(plot_styles.line_dict.keys())
        ),
    }

    table_dict = {
        "Sample": sample_names,
        "Color": color_names[0 : len(sample_names)],
        "Marker style": [marker_names[0]] * len(sample_names),
        "Line style": [line_names[1]] * len(sample_names),
    }

    column_config["Plot"] = st.column_config.SelectboxColumn(
            options=list(range(1, num_of_plots + 1))
            )

    plot_assignments = []
    num_assigned = 1
    plot_id = 1
    # TODO: I think this is the source of some weirdness
    samples_per_plot = ceil(len(sample_names)/num_of_plots)

    for i, _ in enumerate(sample_names):
        if num_assigned <= samples_per_plot:
            plot_assignments.append(plot_id)
            num_assigned += 1

        else:
            plot_id += 1
            plot_assignments.append(plot_id)
            num_assigned = 1

    table_dict["Plot"] = plot_assignments

    # TODO: the default numnber of plots is weird. try it out. fix pls
    # I think it has something to do with 

    df_style = pd.DataFrame.from_dict(table_dict)

    return df_style, column_config


def read_excel_384well_clariostar(input_file) -> tuple:
    # Function for reading the output of CLARIOstar instruments
    # I haven't used one of these in a while so this might be outdated

    df_input = pd.read_excel(input_file, names=range(0,25))
    
    parallel_found = False
    perpendicular_found = False

    for i, row in df_input.iterrows(): # iterate over each dataframe entry (row) of the excel file

        parallel_table = True if "parallel" in str(row[1]) else False
        perpendicular_table = True if "perpendicular" in str(row[1]) else False

        if parallel_table:
            df_parallel = format_384well_table(df_input, i)
            parallel_found = True

        if perpendicular_table:
            df_perpendicular = format_384well_table(df_input, i)
            perpendicular_found = True


    if parallel_found and perpendicular_found:
        return df_parallel, df_perpendicular
    
    else:
        raise Exception("Input file is missing recognizable parallel or perpendicular table.")

def format_384well_table(df_input, i):
    # For 384-well plate, get excel table and rename columns and re-index

    ROW_IDX = [letter for letter in ascii_uppercase[0:16]]
    COLUMNS = range(1, 25)

    start_row = i + 2
    end_row = start_row + 16
    start_col = 1
    num_of_columns = len(COLUMNS)

    df_output = excel_pull_table(df_input, start_row, end_row, start_col, num_of_columns)

    df_output.columns = COLUMNS
    df_output.set_index(pd.Series(ROW_IDX), inplace=True)

    return df_output

def excel_pull_table(df_excel, start_row, end_row, start_col, num_of_columns) -> pd.DataFrame:
    # Given table dimensions and position, subset and return dataframe

    df_rows = df_excel.iloc[start_row:end_row]
    df_table = df_rows.iloc[:, start_col:num_of_columns + start_col]
   
    return df_table