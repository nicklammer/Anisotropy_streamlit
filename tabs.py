# Functions for creating tabs. Hopefully keeps page files clean.
import streamlit as st
from math import ceil

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

    data_dict["units"] = tab.selectbox(
        "Units for concentration (must be same for all samples)",
        options=["fM", "pM", "nM", "uM", "mM", "M"],
        index=2
    )

    data_dict["titration direction"] = tab.selectbox(
        "Titrated in rows or columns?", options=["Rows", "Columns"]
    )

    # Create a unique name column using the dataframe index and sample label
    sample_names = table_samples["Sample label"]
    sample_idx = table_samples.index.tolist()
    new_sample_idx = [
        f"{str(idx)}_{name}" for idx, name in zip(sample_idx,sample_names)
    ]
    table_samples["unique name"] = new_sample_idx

    # Pack up tables
    data_dict["parallel table"] = table_parallel
    data_dict["perpendicular table"] = table_perpendicular
    data_dict["sample table"] = table_samples
    data_dict["sample names"] = sample_names

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
        multi_fit_options(left, right, fit_dict)
    
    elif fit_dict["fit type"] == "Hill fit":
        hill_fit_options(left, right, fit_dict)

    else:
        simplified_fit_options(left, right, fit_dict)

    display_fit_equation(left, fit_dict["fit type"])

    return fit_dict

# TODO: display fit equations on page
def simplified_fit_options(left, right, fit_dict):

    fit_dict["Kdi"] = right.number_input("Kd", value=50.0)
    fit_dict["Si"] = right.number_input("S", value=0.1)
    fit_dict["Oi"] = right.number_input("O", value=0.05)

def hill_fit_options(left, right, fit_dict):
    simplified_fit_options(left, right, fit_dict)

    fit_dict["ni"] = right.number_input("n", value=1.0)

def multi_fit_options(left, right, fit_dict):
    simplified_fit_options(left, right, fit_dict)

    fit_dict["Kd2i"] = right.number_input("Kd2", value=500.0)
    fit_dict["S2i"] = right.number_input("S2", value=0.15)

def display_fit_equation(left, fit_type):

    fit_equations_latex = {
        "Simplified binding isotherm": r'''
                y = S\left ( \frac{x}{x + K_{D}} \right )+ O
                ''',
        "Quadratic": r'''
                y = S\left ( \frac{x + L + K_{D}-\sqrt{\left ( x + L + K_{D} \right )^{2}-\left ( 4*x*L \right )}}{2*L} \right )+ O
                ''',
        "Hill fit": r'''
                y = S\left ( \frac{x^{n}}{x^{n} + K_{D}^{n}} \right )+ O
                ''',
        "Multi-step": r'''
                y = S_{1}\left ( \frac{x}{x + K_{D1}} \right )+S_{2}\left ( \frac{x}{x + K_{D2}} \right )+ O
                '''
    }

    chosen_fit_latex = fit_equations_latex[fit_type]

    left.latex(chosen_fit_latex)

def plot_options_tab(tab, plot_dict, num_of_samples) -> dict:

    left, right = tab.columns(2)

    plot_dict["plot title"] = left.text_input("Plot title", value="plottitle")
    plot_dict["filename"] = left.text_input("Base filename", value="filename")

    plot_dict["number of plots"] = left.number_input(
        "Number of plots to create", min_value=1, value=ceil(num_of_samples/4)
    )
    plot_dict["normalized"] = left.checkbox("Generate normalized plots", value=True)
    plot_dict["show legend"] = left.checkbox("Show plot legend", value=True)
    plot_dict["save png"] = left.checkbox("Save .png files", value=True)
    plot_dict["save svg"] = left.checkbox("Save .svg files", value=True)
    # TODO: implement this differently for streamlit ui
    plot_dict["show plots"] = left.checkbox("Show plots in a window", value=False)

    plot_dict["marker size"] = right.number_input(
        "Marker size", min_value=0.1, value=2., step=0.1
    )
    plot_dict["line width"] = right.number_input(
        "Line width", min_value=0.1, value=2., step=0.1
    )
    plot_dict["plot title size"] = right.number_input(
        "Plot title font size", min_value=1., value=13., step=0.5
    )
    plot_dict["x-axis title size"] = right.number_input(
        "x-axis title font size", min_value=1., value=13., step=0.5
    )
    plot_dict["y-axis title size"] = right.number_input(
        "y-axis title font size", min_value=1., value=13., step=0.5
    )
    plot_dict["x-tick label size"] = right.number_input(
        "x-tick label font size", min_value=1., value=13., step=0.5
    )
    plot_dict["y-tick label size"] = right.number_input(
        "y-tick label font size", min_value=1., value=13., step=0.5
    )
    plot_dict["x-tick size"] = right.number_input(
        "x-tick size", min_value=1., value=6., step=0.5
    )
    plot_dict["y-tick size"] = right.number_input(
        "y-tick size", min_value=1., value=6., step=0.5
    )

    return plot_dict


def style_options_tab(tab, sample_names,
                      unique_names, num_of_plots) -> dict:

    df_style, column_config = helpers.generate_plot_style_table(sample_names, unique_names, num_of_plots)

    table_plot_style = tab.data_editor(
        df_style,
        key="plot_styles",
        hide_index=True,
        num_rows="fixed",
        column_config=column_config,
        disabled=["Sample"],
    )

    return table_plot_style


def plot_view_tab(tab, plot_list):

    if not plot_list:
        tab.write("Nothing plotted")

    left, right = tab.columns(2)
    left_col = True
    for fig in plot_list:
        if left_col:
            left.pyplot(fig)
            left_col = False
        else:
            right.pyplot(fig)
            left_col = True
