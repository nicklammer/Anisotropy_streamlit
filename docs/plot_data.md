# Analyze from CSV File

## Overview
This page accepts pre-formatted CSV data and fits/plots it directly, without requiring raw plate-reader data.

## Data Input
- Upload a `.csv` file using the file uploader in the **Data** tab. You cannot paste data into this table.
- The expected format is two columns per sample. 
    - The first column is concentration values with units in parentheses.
    - The second column is the name of the assay and the sample name. Ex: Anisotropy sample1.
- The sample table will autofill the Sample label column. Ligand concentration is only needed if using the quadratic fit.

## Fit Options
- Choose a binding model.
- Set initial parameter guesses as needed.

## Plot Options
- Customize plot formatting and output options.
- Plot title will increment by number if there are multiple plots.
- You can increase the number of plots created if you want to spread them out more. Select which samples go on which plots in the **Style options** tab
- Normalized plots convert data to fraction bound (0-1).
- `.svg` files can be edited in apps that accept `.svg` files (Illustrator, Inkscape, etc.).
- Use the **Style options** tab to control colors, markers, and line styles per sample.

## Fit and plot
Once all information is entered, hit **Fit and plot** and wait a few seconds. A confirmation message will appear when it is complete. You can view all plots in the **Plot view** tab.

## Download
Once fitting is complete the **Download plots** button is enabled. Clicking it downloads a `.zip` file containing all plots as image files.