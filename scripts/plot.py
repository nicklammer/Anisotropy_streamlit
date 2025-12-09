import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
plt.rcParams['svg.fonttype'] = 'none'
import scipy.optimize as opt
import numpy as np


#general function for scatter plot with a log x scale with a table underneath
def logplot(x, y, labels, units, y_ax, fits_x, fits_y, param, 
    title, color, marker_size, marker_style, line_width, line_style, 
    plot_title_size, x_title_size, y_title_size, x_tick_label_size,
    y_tick_label_size, x_tick_size, y_tick_size, legend, png, svg, 
    plotname, filepath, showplot):
    fig = plt.figure(figsize=(7.0,9.0), dpi=100) #forces figure size and shape 
    fig.subplots_adjust(left=0.125, right=0.95, bottom=0.05, top=0.9) #adjusts margins
    ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4) #subplot for scatter
    table = plt.subplot2grid((6, 1), (5,0)) #subplot for table
    #setup lists for table widths, labels, and colors
    #I have an initial list for each and add to it so that the first column has an empty first row with no color
    #labels and color are both lists specified in the config
    table_widths = [0.12]
    for i in range(len(y)):
        table_widths.append(0.12)
    table_labels = [' ']
    for a in labels:
        table_labels.append(a)
    table_color = ['w']
    for a in color:
        table_color.append(a)
    table = plt.table(cellText=param, loc="lower center", colLabels=table_labels,
        cellLoc="center", colWidths=table_widths, colColours=table_color)
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    #for first column and first row, bold the font
    for (row,column), cell in table.get_celld().items():
        if (row==0) or (column==0):
            cell.set_text_props(fontproperties=FontProperties(weight='bold', size=12))
        cell.set_height(0.12)
    table.scale(1.25,2) #scales column width and row heights
    plt.axis('off') #removes plot axes for the table
    ax1.set_xscale('log')
    #labels, font sizes, and tick sizes
    ax1.set_title(title, fontsize=plot_title_size)
    ax1.set_ylabel(y_ax, fontsize=x_title_size)
    ax1.set_xlabel("[Protein] ("+units+")", fontsize=y_title_size)
    ax1.tick_params(axis='x', which='major', labelsize=x_tick_label_size)
    ax1.tick_params(axis='y', which='major', labelsize=y_tick_label_size)
    ax1.tick_params(axis='x', which='major', length=x_tick_size)
    ax1.tick_params(axis='x', which='minor', length=x_tick_size/2)
    ax1.tick_params(axis='y', which='major', length=y_tick_size)

    #fix the dumb margins here
    x_upper = max([series[0] for series in x])
    x_lower = min([series[-1] for series in x])
    ax1.set_xlim(x_lower/2, x_upper*2)
    #this part assumes that y is a list of lists. each inner list is one sample to plot
    legendicons = []
    for i in range(len(y)):
        ax1.scatter(x[i], y[i], s=20*marker_size, color=color[i], marker=marker_style[i], label=labels[i])
        ax1.plot(fits_x[i], fits_y[i], color=color[i], linewidth=line_width, linestyle=line_style[i])
        #this is to get legends with marker and line
        if legend == True:
            legendicons.append(mlines.Line2D([],[],color=color[i], marker=marker_style[i],
                linestyle=line_style[i], label=labels[i]))
    if legend == True:
        ax1.legend(legendicons, labels, fontsize=13, loc='upper left')
    #save as png for quick viewing, svg for further editing
    if png == True:
        plt.savefig(filepath+plotname+'.png')
    if svg == True:
        plt.savefig(filepath+plotname+'.svg')
    #show plot(s) in pop-up window
    if showplot == True:
        plt.show(block=False)

def build_fit_table():
    # Put together table for displaying fit parameters
    # I don't remember what this placeholder is for
    return None