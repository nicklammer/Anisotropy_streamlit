# Functions that coordinate processing inputs, fitting, and plotting

import pandas as pd
import shutil
import os

from . import validate_inputs, process_data, fit, plot, helpers

def validate_user_inputs(data_dict, plot_dict, table_style):
    # Function to collect all validation functions
        
    validate_inputs.check_sample_table_formatting(data_dict["sample table"])
    validate_inputs.check_unique_titration_idx(data_dict["sample table"])
    validate_inputs.check_titration_direction_match(data_dict["titration direction"],
                                               data_dict["sample table"])
    validate_inputs.check_ligand_concentration(data_dict["sample table"])

    if data_dict["assay"] == "anisotropy":
        validate_inputs.check_empty_dataframe(data_dict["parallel table"], "Parallel table")
        validate_inputs.check_empty_dataframe(data_dict["perpendicular table"], "Perpendicular table")
        validate_inputs.check_data_shape(data_dict["parallel table"], data_dict["perpendicular table"])
        validate_inputs.check_data_ranges(data_dict["parallel table"],
                                          data_dict["sample table"],
                                          data_dict["titration direction"])
        
    elif data_dict["assay"] == "polarization":
        validate_inputs.check_empty_dataframe(data_dict["polarization table"], "Polarization table")
        validate_inputs.check_data_ranges(data_dict["polarization table"],
                                          data_dict["sample table"],
                                          data_dict["titration direction"])


    validate_inputs.check_plot_options(plot_dict)
    validate_inputs.check_empty_dataframe(table_style, "Plot style table")


def preprocess_anisotropy(data_dict):

    data_dict["parallel table"] = helpers.drop_empty_rows_columns(
        data_dict["parallel table"]
    )
    data_dict["perpendicular table"] = helpers.drop_empty_rows_columns(
        data_dict["perpendicular table"]
    )

    df_aniso = process_data.calculate_anisotropy(
        data_dict["parallel table"], data_dict["perpendicular table"]
    )
    df_sample_data = process_data.compile_anisotropy(
        df_aniso, data_dict["sample table"], data_dict["titration direction"]
    )

    return data_dict, df_sample_data

def preprocess_polarization(data_dict):

    data_dict["polarization table"] = helpers.drop_empty_rows_columns(
        data_dict["polarization table"]
    )

    df_sample_data = process_data.compile_polarization(
        data_dict["polarization table"], data_dict["sample table"], data_dict["titration direction"]
    )

    return data_dict, df_sample_data

def process_fit_data(data_dict, fit_dict, plot_dict, table_style, tmpdir):

    validate_user_inputs(data_dict, plot_dict, table_style)

    outdir = f"{tmpdir}/plots"
    os.makedirs(outdir, exist_ok=True)

    assay = data_dict["assay"]

    if assay == "anisotropy":
        data_dict, df_sample_data = preprocess_anisotropy(data_dict)

    elif assay == "polarization":
        data_dict, df_sample_data = preprocess_polarization(data_dict)

    # Merge all dataframes
    df_all = pd.merge(data_dict["sample table"], table_style, on="unique name")
    df_all = pd.merge(df_all, df_sample_data, on="unique name")

    # Add units to data df
    df_all["units"] = data_dict["units"]

    # Fit data and merge with df_all
    df_fit_results = fit_data(df_all, fit_dict, assay)

    df_all = df_all.merge(df_fit_results, on="unique name")

    total_num_plots = max(df_all["Plot"])

    plot_list = []

    for i in range(1, total_num_plots + 1):

        # subset data by plot groupings
        df_subset = df_all[df_all["Plot"] == i]
        plot_title = f"{plot_dict['plot title']} {str(i)}"
        filename = f"{plot_dict['filename']}_{str(i)}"

        plot_current = plot.logplot(
            df_subset,
            assay,
            plot_title,
            filename,
            plot_dict,
            outdir,
            normalized=False,
        )
        plot_list.append(plot_current)

        if plot_dict["normalized"]:

            plot_title = f"{plot_dict['plot title']} {str(i)} Normalized"
            filename = f"{plot_dict['filename']}_normalized_{str(i)}"

            plot_normalized = plot.logplot(
                df_subset,
                "Fraction bound",
                plot_title,
                filename,
                plot_dict,
                outdir,
                normalized=True,
            )
            plot_list.append(plot_normalized)

    helpers.save_data_csv(df_all, assay, f"{outdir}/data_{plot_dict['filename']}.csv")

    zip_path = shutil.make_archive(outdir, "zip", outdir)

    return zip_path, plot_list


def fit_data(df_all, fit_dict, y_type) -> pd.DataFrame:

    fit_functions = {
        "Simplified binding isotherm": fit.get_simple_fit,
        "Quadratic": fit.get_quad_fit,
        "Hill fit": fit.get_hill_fit,
        "Multi-step": fit.get_multi_fit,
    }

    chosen_fit_function = fit_functions[fit_dict["fit type"]]

    def _fit_by_row(row):

        fit_function_args = {
            "x": row["concentration"],
            "y": row[y_type],
            "units": row["units"],
            "fit_dict": fit_dict,
            "ligand_conc": row.get("Ligand concentration"),  # just to be safe use .get
        }

        x_fit, y_fit, y_norm, y_fit_norm, fit_params = chosen_fit_function(
            **fit_function_args
        )

        return pd.Series(
            {
                "unique name": row["unique name"],
                "x fit": x_fit,
                "y fit": y_fit,
                "y norm": y_norm,
                "y fit norm": y_fit_norm,
                "parameters": fit_params,
            }
        )

    df_fit_results = df_all.apply(_fit_by_row, axis=1)

    return df_fit_results
