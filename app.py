import streamlit as st
from multiapp import MultiApp
from apps import home

app = MultiApp() 

app.add_app("Home", home.app)

app.run()