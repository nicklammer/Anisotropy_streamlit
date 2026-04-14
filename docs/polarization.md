# Fluorescence Polarization

## Overview
This page fits and plots fluorescence polarization binding data. Upload your raw plate-reader values or fill in the table, add sample info to the sample table, configure fit and plot options, then click **Fit and plot** to generate plots.

## Data Input
- Upload your plate reader `.xlsx` file or enter polarization data into the data table.
- Add sample information to the sample table.
- Titration row/column: which letter (row) or column (number) is your titration in?
- Titration range: which wells do you want to include in the analysis? Use numbers if in 1 row or letters if in 1 column.
- Starting concentration: maximum concentration of your titration.
- Dilution factor: how did you perform your serial dilution? Ex: 1:2 dilutions would be a dilution factor of 2.
- Ligand concentration: concentration of your constant variable. Same units as Starting concentration and only required for quadratic fits.
- Excluded wells: Any wells you want to exclude from the analysis. Use the same notation as in your Titration range.
- Data can be pasted directly from a spreadsheet for any of these tables.
- Don't forget to select options for Units and how you performed your titrations.

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
Once fitting is complete the **Download plots** button is enabled. Clicking it downloads a `.zip` file containing all plots as image files along with the plotted data in `.csv` format. You can edit this `.csv` and upload it to the **Plot data** page to re-analyze.
