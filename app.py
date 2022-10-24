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
title = st.container()
main = st.container()
footer = st.container()


def show_sidebar():
    """show the sidebar of the page

    Returns:
        str: the selection of the page
    """
    st.markdown(
        "<h2 style='text-align: center;'>Beijing trafic research</h2>", unsafe_allow_html=True)  # title of the sidebar
    # team member
    st.markdown(f"""<div style="text-align: left">
                        <h3 style='text-align: center;'>Team 6 members</h3>
                        <a href='https://www.linkedin.com/in/xiangyu-an-34109a196/'><span style="text-transform:uppercase;">AN</span> Xiangyu</a>
                        <a href='https://www.linkedin.com/in/m%C3%A9lisande-gr%C3%A9goire-b%C3%A9granger-a5654219b/'><span style="text-transform:uppercase;">Grégoire--Bégranger</span> Mélisande</a>
                        <a href='https://www.linkedin.com/in/xiangyu-an-34109a196/'><span style="text-transform:uppercase;">Nadarajah</span> Sugitha</a>
                    </div>""", unsafe_allow_html=True)
    # github
    st.markdown(
        f"""<
            <div style="text-align: center">
                <h3 style='text-align: center;'>Our Github</h3>
                <a href='https://github.com/AN-Xiang-yu/Beijing_traffic_analysis_ver2'>{t.img_to_html('img/github.png')}</a>
            </div>""", unsafe_allow_html=True)
    # image of EFREI Paris
    st.image("img\logo-efrei.png")
    # selection of page
    selection = st.radio("Browsing", list(
        PAGES.keys()))  # navigation to the other page

    return selection


#  --- body of the page ---

with sidebar:  # sidebar of the page
    selection = show_sidebar()

with title:  # title of the page
    st.markdown(
        f"""<h1 style='text-align: center;'>{selection}</h1>""", unsafe_allow_html=True)  # h1 title of the page

with main:  # main of the page
    page = PAGES[selection]
    page.main()

with footer:  # footer of the page
    st.markdown(
        "<footer style='text-align: center;'>Copyright©2022-2023 Beijing trafic research Group 6 of DAI at EFREI Paris (promotion 2024) - All Rights Reserved. </footer>", unsafe_allow_html=True)
