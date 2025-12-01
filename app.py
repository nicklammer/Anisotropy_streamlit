import streamlit as st
import pandas as pd
import tempfile
import time

import tabs

st.set_page_config(layout="wide")

data_dict = {}
fit_dict = {}
plot_dict = {}
style_dict = {}

st.title("Analyze Fluorescence Anisotropy")
# st.header("Self fill")

buttons_left, buttons_right = st.columns([0.15, 0.85])
plot_button = buttons_left.button("Fit and plot", type="primary")
save_button = buttons_right.button("Save parameters")

data_tab, fit_tab, plot_tab, style_tab = st.tabs(
    ["Data", "Fit options", "Plot options", "Style options"]
)

tabs.data_tab_selffill(data_tab, data_dict)

tabs.fit_options_tab(fit_tab, fit_dict)

tabs.plot_options_tab(plot_tab, plot_dict)

tabs.style_options_tab(style_tab, style_dict)

with tempfile.TemporaryDirectory() as tmpdir:
    if plot_button:
        with st.spinner("Processing data...", show_time=True):
            # for file in encr_logs:
            #     encrypted_filenames.append(file.name)
            #     with open(f"{tmpdir}/{file.name}", "wb") as tmp_file:
            #         tmp_file.write(file.getvalue())
            # outzip = crypto_main.decrypt_parse_logs(encrypted_filenames, tmpdir,
            #                                    log_samples, parse_check,
            #                                    compile_check, segment_logs_check,
            #                                    keep_logs_check)
        #     st.success("Done!")
        # with open(outzip, "rb") as file:
        #     timestamp = time.strftime("%Y%m%d_%H%M%S")
        #     st.download_button("Download logs", data=file, on_click='ignore',
        #                        file_name=f'decrypted_logs_{timestamp}.zip')