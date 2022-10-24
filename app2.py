# app.py

import best_route
import congestion
import density
import streamlit as st

# Declaration of constants
PAGES = {
    'Most congested streets': congestion,
    'Best route to go from point A to B': best_route,
    'Average car density of Beijing': density,
}

#  ----- body of the page ------
# sidebar of the page
sidebar = st.sidebar
with sidebar:
    st.markdown(
        "<h2 style='text-align: center;'>Beijing trafic research</h2>", unsafe_allow_html=True)  # title of the sidebar
    st.text('Team 6')
    st.text('Xiangyu AN')
    st.text('Mélisande GREGOIRE--BEGRANGER')
    st.text('Sugitha NADARAJAH')
    st.text('M1 DAI')
    selection = st.radio("Browsing", list(
        PAGES.keys()))  # navigation to the other page
# --- header of the page ---
header = st.container()
with header:
    st.markdown(
        f"""<h1 style='text-align: center;'>{selection}</h1>""", unsafe_allow_html=True)  # h1 title of the page

# --- main of the page ----
page = PAGES[selection]
page.main()

# --- footer of the page ---
footer = st.container()
with footer:
    st.markdown(
        "<footer style='text-align: center;'>Copyright©2022-2023 Beijing trafic research Group 6 of DAI at EFREI Paris (promotion 2024) - All Rights Reserved. </footer>", unsafe_allow_html=True)
