# affichage/pages/theme.py
import streamlit as st

def apply_theme(mode="dark"):
    """
    Applique un thème sombre ou clair sur toutes les pages.
    mode: "dark" ou "light"
    """
    if mode == "dark":
        st.markdown("""
        <style>
        .stApp {background-color: #000000; color: #f0f0f0;}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {background-color: #ffffff; color: #000000;}
        </style>
        """, unsafe_allow_html=True)
