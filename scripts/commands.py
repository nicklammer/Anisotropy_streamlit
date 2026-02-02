# Functions that coordinate processing inputs, fitting, and plotting

import pandas as pd
import shutil
import os

from . import process_data, fit, plot


def process_anisotropy(data_dict, fit_dict, plot_dict, table_style, tmpdir):

    outdir_plots = f"{tmpdir}/plots"
    os.makedirs(outdir_plots, exist_ok = True)

    data_dict["parallel table"] = process_data.drop_empty_rows_columns(data_dict["parallel table"])
    data_dict["perpendicular table"] = process_data.drop_empty_rows_columns(data_dict["perpendicular table"])

    df_aniso = process_data.calculate_anisotropy(data_dict["parallel table"], data_dict["perpendicular table"])
    df_sample_data = process_data.compile_anisotropy(
        df_aniso, data_dict["sample table"], data_dict["titration direction"])
    
    # Merge all dataframes
    df_all = pd.merge(data_dict["sample table"], table_style, on="unique name")
    df_all = pd.merge(df_all, df_sample_data, on="unique name")

    # Add units to data df
    df_all["units"] = data_dict["units"]

    # Fit data and merge with df_all
    df_fit_results = fit_data(df_all, fit_dict, "anisotropy")

    df_all = df_all.merge(df_fit_results, on="unique name")

    total_num_plots = max(df_all["Plot"])

    plot_list = []

    for i in range(1, total_num_plots + 1):

        # subset data by plot groupings
        df_subset = df_all[df_all["Plot"] == i]
        plot_title = f"{plot_dict['plot title']} {str(i)}"
        filename = f"{plot_dict['filename']}_{str(i)}"

        plot_current = plot.logplot(df_subset, "anisotropy", plot_title,
                                    filename, plot_dict, outdir_plots,
                                    normalized=False)
        plot_list.append(plot_current)

        if plot_dict["normalized"]:

            plot_title = f"{plot_dict['plot title']} {str(i)} Normalized"
            filename = f"{plot_dict['filename']}_normalized_{str(i)}"
            
            plot_normalized = plot.logplot(df_subset, "Fraction bound", plot_title,
                                           filename, plot_dict, outdir_plots,
                                           normalized=True)
            plot_list.append(plot_normalized)

    zip_path = shutil.make_archive(outdir_plots, 'zip', outdir_plots)

    return zip_path, plot_list



def fit_data(df_all, fit_dict, y_type) -> pd.DataFrame:

    fit_functions = {
        "Simplified binding isotherm": fit.get_simple_fit,
        "Quadratic": fit.get_quad_fit,
        "Hill fit": fit.get_hill_fit,
        "Multi-step": fit.get_multi_fit
    }

    chosen_fit_function = fit_functions[fit_dict["fit type"]]

    def _fit_by_row(row):

        fit_function_args = {
            "x": row["concentration"],
            "y": row[y_type],
            "units": row["units"],
            "fit_dict": fit_dict,
            "ligand_conc": row.get("Ligand concentration") # just to be safe use .get
        }

        x_fit, y_fit, y_norm, y_fit_norm, fit_params = chosen_fit_function(**fit_function_args)

        return pd.Series({
            "unique name": row["unique name"],
            "x fit": x_fit,
            "y fit": y_fit,
            "y norm": y_norm,
            "y fit norm": y_fit_norm,
            "parameters": fit_params
        })

    df_fit_results = df_all.apply(_fit_by_row, axis=1)

    return df_fit_results