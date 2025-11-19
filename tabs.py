# Functions for creating tabs. Hopefully keeps page files clean.
import streamlit as st
import helpers


def data_tab_selffill(tab, parameters) -> dict:
    tab.write("Parallel fluorescence")
    table_parallel = tab.data_editor(
        helpers.generate_empty_plate(),
        key="parallel",
        disabled=["_index"],
        column_config=helpers.column_config_data_plate,
    )

    tab.write("Perpendicular fluorescence")
    table_perpendicular = tab.data_editor(
        helpers.generate_empty_plate(),
        key="perpendicular",
        disabled=["_index"],
        column_config=helpers.column_config_data_plate,
    )

    number_of_samples = tab.number_input(
        "How many samples do you have?", min_value=1, value=1
    )

    parameters["titration direction"] = tab.selectbox(
        "Titrated in rows or columns?", options=["Rows", "Columns"]
    )

    tab.write("Enter sample information here:")

    # TODO: This table needs to have a number of rows controlled by
    # number_of_samples without erasing the contents.
    # or maybe this doesn't matter?
    table_samples = tab.data_editor(
        helpers.generate_sample_table(number_of_samples),
        key="samples",
        hide_index=True,
        num_rows="dynamic",
        column_config=helpers.column_config_sample_table,
    )

    parameters["assay type"] = tab.selectbox(
        "Anisotropy or polarization?", options=["Anisotropy", "Polarization"]
    )

    # Pack up tables
    parameters["parallel table"] = table_parallel
    parameters["perpendicular table"] = table_perpendicular
    parameters["sample table"] = table_samples
    parameters["sample names"] = table_samples["Sample label"]

    return parameters


def fit_options_tab(tab, parameters) -> dict:

    left, right = tab.columns(2)

    left.write("Select type of fit:")
    parameters["fit type"] = left.selectbox(
        "Fit", options=["Simplified binding isotherm", "Hill fit", "Multi-step"]
    )

    right.write("Initial parameters:")

    # Available parameters depend on the fit equation
    # This is kind of like custom components?
    if parameters["fit type"] == "Simplified binding isotherm":
        simplified_fit_options(right, parameters)

    elif parameters["fit type"] == "Hill fit":
        simplified_fit_options(right, parameters)
        # hill_fit_options()

    elif parameters["fit type"] == "Multi-step":
        simplified_fit_options(right, parameters)
        # multi_fit_options()

    return parameters


def simplified_fit_options(tab_column, parameters):
    parameters["Kdi"] = tab_column.number_input("Kd")
    parameters["Si"] = tab_column.number_input("S")
    parameters["Oi"] = tab_column.number_input("O")


def hill_fit_options():
    return NotImplemented


def multi_fit_options():
    return NotImplemented


def plot_options_tab(tab, parameters) -> dict:

    left, right = tab.columns(2)

    parameters["plot title"] = left.text_input("Plot title")
    parameters["filename"] = left.text_input("Base filename")

    parameters["samples per plot"] = left.number_input(
        "Number of samples per plot", min_value=1, value=4
    )
    parameters["show legend"] = left.checkbox("Show plot legend", value=True)
    parameters["save png"] = left.checkbox("Save .png files", value=True)
    parameters["save svg"] = left.checkbox("Save .svg files", value=True)
    # TODO: implement this different for streamlit ui
    parameters["plot windows"] = left.checkbox("Show plots in a window", value=False)

    parameters["marker size"] = right.number_input(
        "Marker size", min_value=0.1, value=2.0
    )
    parameters["line width"] = right.number_input(
        "Line width", min_value=0.1, value=2.0
    )
    parameters["plot title size"] = right.number_input(
        "Plot title font size", min_value=1, value=13
    )
    parameters["x-axis title size"] = right.number_input(
        "x-axis title font size", min_value=1, value=13
    )
    parameters["y-axis title size"] = right.number_input(
        "y-axis title font size", min_value=1, value=13
    )
    parameters["x-tick label size"] = right.number_input(
        "x-tick label font size", min_value=1, value=13
    )
    parameters["y-tick label size"] = right.number_input(
        "y-tick label font size", min_value=1, value=13
    )
    parameters["x-tick size"] = right.number_input(
        "x-tick font size", min_value=1, value=6
    )
    parameters["y-tick size"] = right.number_input(
        "y-tick font size", min_value=1, value=6
    )

    return parameters


def style_options_tab(tab, parameters) -> dict:

    table_plot_style = tab.data_editor(
        helpers.generate_plot_style_table(parameters["sample names"]),
        key="plot_styles",
        hide_index=True,
        num_rows="fixed",
        column_config=helpers.column_config_style_table,
        disabled=["Sample"],
    )

    return parameters
