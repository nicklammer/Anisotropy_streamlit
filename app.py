import streamlit as st

# Define pages in this list as tuples
# (File name, page name, icon, navigation section)

pages = [
    ("anisotropy.py", "Anisotropy", ":material/table_view:"),
    ("polarization.py", "Polarization", ":material/table:"),
    ("plot_data.py", "Plot data", ":material/table:")
]

# Iterate to make st.Page objects

pages_nav = []

for page in pages:
    pages_nav.append(st.Page(
        f"pages/{page[0]}",
        title=page[1],
        icon=page[2]
    ))

pg = st.navigation(pages_nav)

pg.run()