# app.py

from page import best_route, congestion, density, tools as t

import streamlit as st

# declaration of constants
PAGES = {
    'Most congested streets': congestion,
    'Best route to go from point A to B': best_route,
    'Average car density of Beijing': density,
}

# create the containers
sidebar = st.sidebar
header = st.container()
main = st.container()
footer = st.container()

#  ----- body of the page ------
# sidebar of the page
with sidebar:
    st.markdown(
        "<h2 style='text-align: center;'>Beijing trafic research</h2>", unsafe_allow_html=True)  # title of the sidebar
    st.title('Our LinkedIn')

    linkX = 'LinkedIn  Xiangyu [link](https://www.linkedin.com/in/xiangyu-an-34109a196/)'
    st.markdown(linkX, unsafe_allow_html=True)

    linkM = 'LinkedIn Mélisande [link](https://www.linkedin.com/in/mélisande-grégoire-bégranger-a5654219b/)'
    st.markdown(linkM, unsafe_allow_html=True)

    linkS = 'LinkedIn Sugitha [link](https://www.linkedin.com/in/sugitha-nadarajah-07681119b/)'
    st.markdown(linkS, unsafe_allow_html=True)

    linkM = 'LinkedIn Mélisande [link](https://www.linkedin.com/in/mélisande-grégoire-bégranger-a5654219b/)'
    st.markdown(linkM, unsafe_allow_html=True)

    st.title('Our LinkedIn')
    gitxiangyu = 'Git  Xiangyu [link](https://github.com/AN-Xiang-yu)'
    st.markdown(gitxiangyu, unsafe_allow_html=True)

    gitmelisande = 'Git  Mélisande [link](https://github.com/melisandeGB)'
    st.markdown(gitxiangyu, unsafe_allow_html=True)

    gitsugitha = 'Git Sugitha [link](https://github.com/Sugitha-Nadarajah)'
    st.markdown(gitsugitha, unsafe_allow_html=True)
    selection = st.radio("Browsing", list(
        PAGES.keys()))  # navigation to the other page

# --- header of the page ---
with header:
    st.markdown(
        f"""<h1 style='text-align: center;'>{selection}</h1>""", unsafe_allow_html=True)  # h1 title of the page

# --- main of the page ----
with main:
    page = PAGES[selection]
    page.main()

# --- footer of the page ---
with footer:
    st.markdown(
        "<footer style='text-align: center;'>Copyright©2022-2023 Beijing trafic research Group 6 of DAI at EFREI Paris (promotion 2024) - All Rights Reserved. </footer>", unsafe_allow_html=True)
