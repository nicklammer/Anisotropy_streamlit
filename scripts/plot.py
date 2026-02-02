import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
# Linux doesn't always ship with official Arial
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
# This makes it so the text in the svg file is editable
plt.rcParams['svg.fonttype'] = 'none'

from collections import defaultdict

import plot_styles


def map_plot_styles(df):
    # Map color reference names to the friendly names user chose
    df["Color"] = df["Color"].map(plot_styles.color_dict)
    df["Marker style"] = df["Marker style"].map(plot_styles.marker_dict)
    df["Line style"] = df["Line style"].map(plot_styles.line_dict)

    return df

def logplot(df_input, y_ax, plot_title, filename, plot_dict, tmpdir, normalized):
    # TODO: This needs updating. lots of formatting and confusing to read.
    df = df_input.copy()
    df = map_plot_styles(df)

    fig = plt.figure(figsize=(7.0,9.0), dpi=200) #forces figure size and shape 
    fig.subplots_adjust(left=0.125, right=0.95, bottom=0.05, top=0.9) #adjusts margins
    ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4) #subplot for scatter
    # TODO: not sure if this is needed as is
    table_ax = plt.subplot2grid((6, 1), (5,0)) #subplot for table

    table = build_fit_table(df)
    table.auto_set_font_size(False)
    table.set_fontsize(11)

    #for first column and first row, bold the font
    for (row,column), cell in table.get_celld().items():
        if (row==0) or (column==-1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold', size=12))
        cell.set_height(0.12)

    table.scale(1.25,2) #scales column width and row heights
    plt.axis('off') #removes plot axes for the table

    # Set log scale for plot x-axis
    ax1.set_xscale('log')

    # Temp variables
    y_ax_title = y_ax.capitalize()
    units = df_input["units"].values[0]

    # Account for normalized data
    y_ax = "y norm" if normalized else y_ax
    y_ax_fit = "y fit norm" if normalized else "y fit"

    ax1.set_title(plot_title, fontsize=plot_dict["plot title size"])
    ax1.set_ylabel(y_ax_title, fontsize=plot_dict["y-axis title size"])
    ax1.set_xlabel("[Protein] ("+units+")", fontsize=plot_dict["x-axis title size"])
    ax1.tick_params(axis='x', which='major', labelsize=plot_dict["x-tick label size"])
    ax1.tick_params(axis='y', which='major', labelsize=plot_dict["y-tick label size"])
    ax1.tick_params(axis='x', which='major', length=plot_dict["x-tick size"])
    ax1.tick_params(axis='x', which='minor', length=plot_dict["x-tick size"]/2)
    ax1.tick_params(axis='y', which='major', length=plot_dict["y-tick size"])

    # fix the weird margins here
    x_upper = max([max(conc) for conc in df["concentration"].to_list()])
    x_lower = min([min(conc) for conc in df["concentration"].to_list()])
    ax1.set_xlim(x_lower/2, x_upper*2)

    # go through data and plot curves for each row
    legendicons = []
    for i, row in df.iterrows():
        x = row["concentration"]
        y = row[y_ax]
        x_fit = row["x fit"]
        y_fit = row[y_ax_fit]

        ax1.scatter(x, y, s=20*plot_dict["marker size"], color=row["Color"], marker=row["Marker style"], label=row["Sample label"])
        ax1.plot(x_fit, y_fit, color=row["Color"], linewidth=plot_dict["line width"], linestyle=row["Line style"])

        # this is to get legends with marker and line
        if plot_dict["show legend"]:
            legendicons.append(mlines.Line2D([],[],color=row["Color"], marker=row["Marker style"],
                linestyle=row["Line style"], label=row["Sample label"]))
            
    if plot_dict["show legend"]:
        ax1.legend(legendicons, df["Sample label"], fontsize=13, loc='upper left')

    # save as png for quick viewing, svg for further editing
    if plot_dict["save png"]:
        plt.savefig(f"{tmpdir}/{filename}.png")

    if plot_dict["save svg"]:
        plt.savefig(f"{tmpdir}/{filename}.svg")

    # show plot(s) in pop-up window
    # if plot_dict["show plots"]:
    #     plt.show(block=False)

    return fig

def build_fit_table(df):
    # Put together table for displaying fit parameters
    # setup lists for table widths, labels, and colors
    #I have an initial list for each and add to it so that the first column has an empty first row with no color
    #labels and color are both lists specified in the config

    # Make df_param that combines parameter_dicts from each row of df
    # all should have the same keys.


    combined_param_dict = defaultdict(list)
    for param_dict in df["parameters"].to_list():
        for key, value in param_dict.items():
            combined_param_dict[key].append(value)

    column_labels = df["Sample label"].to_list()

    params_2d_list = []
    param_labels_list = []

    for key, value in combined_param_dict.items():
        params_2d_list.append(value)
        param_labels_list.append(key)
    
    
    df_param = pd.DataFrame(params_2d_list, columns=column_labels, index = param_labels_list)

    table_widths = [0.12 for i in range(len(df) + 1)]

    table_color = df["Color"].to_list()

    table_color = [color if "black" not in color else "w" for color in table_color]

    table = plt.table(cellText=df_param, loc="lower center",
        cellLoc="center", colWidths=table_widths, colColours=table_color)

    return table