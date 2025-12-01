# Functions for creating tabs. Hopefully keeps page files clean.
import streamlit as st
import helpers


def data_tab_selffill(tab, data_dict) -> dict:

    # TODO: make a separate polarization page to simplify processing of data
    data_dict["assay type"] = tab.selectbox(
        "Anisotropy or polarization?", options=["Anisotropy", "Polarization"]
    )

    excel_file = tab.file_uploader("Upload CLARIOstar .xlsx file here (optional)", accept_multiple_files=False, type="xlsx")

    if excel_file:
        df_parallel, df_perpendicular = helpers.read_excel_384well_clariostar(excel_file)
    else:
        df_parallel = helpers.generate_empty_plate()
        df_perpendicular = helpers.generate_empty_plate()

    tab.write("Parallel fluorescence")
    table_parallel = tab.data_editor(
        df_parallel,
        key="parallel",
        disabled=["_index"],
        column_config=helpers.column_config_data_plate,
    )

    tab.write("Perpendicular fluorescence")
    table_perpendicular = tab.data_editor(
        df_perpendicular,
        key="perpendicular",
        disabled=["_index"],
        column_config=helpers.column_config_data_plate,
    )

    tab.write("Enter sample information here:")

    # TODO: This table needs to have a number of rows controlled by
    # number_of_samples without erasing the contents.
    # or maybe this doesn't matter?
    table_samples = tab.data_editor(
        helpers.generate_sample_table(),
        key="samples",
        hide_index=True,
        num_rows="dynamic",
        column_config=helpers.column_config_sample_table,
    )

    data_dict["titration direction"] = tab.selectbox(
        "Titrated in rows or columns?", options=["Rows", "Columns"]
    )

    # Pack up tables
    data_dict["parallel table"] = table_parallel
    data_dict["perpendicular table"] = table_perpendicular
    data_dict["sample table"] = table_samples
    data_dict["sample names"] = table_samples["Sample label"]

    return data_dict


def fit_options_tab(tab, fit_dict) -> dict:

    left, right = tab.columns(2)

    left.write("Select type of fit:")
    fit_dict["fit type"] = left.selectbox(
        "Fit", options=["Simplified binding isotherm",
                        "Quadratic", "Hill fit", "Multi-step"]
    )

    right.write("Initial parameters:")

    # Available parameters depend on the fit equation
    # This is kind of like custom components?
    if fit_dict["fit type"] == "Multi-step":
        multi_fit_options(right, fit_dict)

    else:
        simplified_fit_options(right, fit_dict)

    return fit_dict

# TODO: display fit equations on page
def simplified_fit_options(tab_column, fit_dict):
    fit_dict["Kdi"] = tab_column.number_input("Kd")
    fit_dict["Si"] = tab_column.number_input("S")
    fit_dict["Oi"] = tab_column.number_input("O")


def multi_fit_options(tab_column, fit_dict):
    simplified_fit_options(tab_column, fit_dict)

    fit_dict["Kd2i"] = tab_column.number_input("Kd2")
    fit_dict["S2i"] = tab_column.number_input("S2")


def plot_options_tab(tab, plot_dict) -> dict:

    left, right = tab.columns(2)

    plot_dict["plot title"] = left.text_input("Plot title", value="plottitle")
    plot_dict["filename"] = left.text_input("Base filename", value="filename")

    plot_dict["samples per plot"] = left.number_input(
        "Number of samples per plot", min_value=1, value=4
    )
    plot_dict["show legend"] = left.checkbox("Show plot legend", value=True)
    plot_dict["save png"] = left.checkbox("Save .png files", value=True)
    plot_dict["save svg"] = left.checkbox("Save .svg files", value=True)
    # TODO: implement this differently for streamlit ui
    plot_dict["plot windows"] = left.checkbox("Show plots in a window", value=False)

    plot_dict["marker size"] = right.number_input(
        "Marker size", min_value=0.1, value=2.0
    )
    plot_dict["line width"] = right.number_input(
        "Line width", min_value=0.1, value=2.0
    )
    plot_dict["plot title size"] = right.number_input(
        "Plot title font size", min_value=1, value=13
    )
    plot_dict["x-axis title size"] = right.number_input(
        "x-axis title font size", min_value=1, value=13
    )
    plot_dict["y-axis title size"] = right.number_input(
        "y-axis title font size", min_value=1, value=13
    )
    plot_dict["x-tick label size"] = right.number_input(
        "x-tick label font size", min_value=1, value=13
    )
    plot_dict["y-tick label size"] = right.number_input(
        "y-tick label font size", min_value=1, value=13
    )
    plot_dict["x-tick size"] = right.number_input(
        "x-tick font size", min_value=1, value=6
    )
    plot_dict["y-tick size"] = right.number_input(
        "y-tick font size", min_value=1, value=6
    )

    return plot_dict


def style_options_tab(tab, style_dict) -> dict:

    table_plot_style = tab.data_editor(
        helpers.generate_plot_style_table(style_dict["sample names"]),
        key="plot_styles",
        hide_index=True,
        num_rows="fixed",
        column_config=helpers.column_config_style_table,
        disabled=["Sample"],
    )

    style_dict["plot style table"] = table_plot_style

    return style_dict
