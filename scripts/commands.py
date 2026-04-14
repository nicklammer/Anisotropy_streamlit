# Functions that coordinate processing inputs, fitting, and plotting

import pandas as pd
import shutil
import os

from . import validate_inputs, process_data, fit, plot, helpers


def validate_user_inputs(data_dict, fit_dict, plot_dict, table_style):
    validate_inputs.check_sample_table_formatting(data_dict["sample table"])
    validate_inputs.check_unique_titration_idx(data_dict["sample table"])
    validate_inputs.check_titration_direction_match(data_dict["titration direction"],
                                               data_dict["sample table"])
    if fit_dict["fit type"] == "Quadratic":
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


def validate_user_inputs_from_csv(data_dict, fit_dict, plot_dict, table_style):
    if fit_dict["fit type"] == "Quadratic":
        validate_inputs.check_ligand_concentration(data_dict["sample table"])

    validate_inputs.check_plot_options(plot_dict)
    validate_inputs.check_empty_dataframe(table_style, "Plot style table")


def preprocess_anisotropy(data_dict):
    data_dict["parallel table"] = helpers.drop_empty_rows_columns(data_dict["parallel table"])
    data_dict["perpendicular table"] = helpers.drop_empty_rows_columns(data_dict["perpendicular table"])
    data_dict["anisotropy table"] = process_data.calculate_anisotropy(
        data_dict["parallel table"], data_dict["perpendicular table"]
    )
    return data_dict


def preprocess_polarization(data_dict):
    data_dict["polarization table"] = helpers.drop_empty_rows_columns(data_dict["polarization table"])
    return data_dict


def _fit_and_plot(df_sample_data, data_dict, fit_dict, plot_dict, table_style, outdir, save_csv):
    """Shared core: merge, fit, plot, and archive."""
    assay = data_dict["assay"]

    df_all = pd.merge(data_dict["sample table"], table_style, on="unique name")
    df_all = pd.merge(df_all, df_sample_data, on="unique name")
    df_all["units"] = data_dict["units"]

    df_fit_results = fit_data(df_all, fit_dict, assay)
    df_all = df_all.merge(df_fit_results, on="unique name")

    plot_list = []
    for i in range(1, max(df_all["Plot"]) + 1):
        df_subset = df_all[df_all["Plot"] == i]
        plot_title = f"{plot_dict['plot title']} {i}"
        filename   = f"{plot_dict['filename']}_{i}"

        plot_list.append(plot.logplot(
            df_subset, assay, plot_title, filename, plot_dict, outdir, normalized=False
        ))

        if plot_dict["normalized"]:
            plot_list.append(plot.logplot(
                df_subset, "Fraction bound",
                f"{plot_title} Normalized",
                f"{plot_dict['filename']}_normalized_{i}",
                plot_dict, outdir, normalized=True,
            ))

    if save_csv:
        helpers.save_data_csv(df_all, assay, f"{outdir}/data_{plot_dict['filename']}.csv")

    return shutil.make_archive(outdir, "zip", outdir), plot_list


def process_fit_data(data_dict, fit_dict, plot_dict, table_style, tmpdir):
    validate_user_inputs(data_dict, fit_dict, plot_dict, table_style)

    outdir = f"{tmpdir}/plots"
    os.makedirs(outdir, exist_ok=True)

    assay = data_dict["assay"]
    if assay == "anisotropy":
        data_dict = preprocess_anisotropy(data_dict)
    elif assay == "polarization":
        data_dict = preprocess_polarization(data_dict)

    df_sample_data = process_data.compile_data_assay_concentration(
        data_dict[f"{assay} table"], data_dict["sample table"],
        data_dict["titration direction"], assay
    )

    return _fit_and_plot(df_sample_data, data_dict, fit_dict, plot_dict, table_style, outdir, save_csv=True)


def process_fit_data_from_csv(data_dict, fit_dict, plot_dict, table_style, tmpdir):
    validate_user_inputs_from_csv(data_dict, fit_dict, plot_dict, table_style)

    outdir = f"{tmpdir}/plots"
    os.makedirs(outdir, exist_ok=True)

    df_sample_data = process_data.compile_data_assay_concentration_from_csv(
        data_dict["data table"], data_dict["assay"]
    )

    return _fit_and_plot(df_sample_data, data_dict, fit_dict, plot_dict, table_style, outdir, save_csv=False)


def fit_data(df_all, fit_dict, y_type) -> pd.DataFrame:

    fit_functions = {
        "Simplified binding isotherm": fit.get_simple_fit,
        "Quadratic": fit.get_quad_fit,
        "Hill fit": fit.get_hill_fit,
        "Multi-step": fit.get_multi_fit,
    }

    chosen_fit_function = fit_functions[fit_dict["fit type"]]

    def _fit_by_row(row):
        x_fit, y_fit, y_norm, y_fit_norm, fit_params = chosen_fit_function(
            x=row["concentration"],
            y=row[y_type],
            units=row["units"],
            fit_dict=fit_dict,
            ligand_conc=row.get("Ligand concentration"),
        )
        return pd.Series({
            "unique name": row["unique name"],
            "x fit": x_fit,
            "y fit": y_fit,
            "y norm": y_norm,
            "y fit norm": y_fit_norm,
            "parameters": fit_params,
        })

    return df_all.apply(_fit_by_row, axis=1)
