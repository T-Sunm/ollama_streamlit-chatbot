import streamlit as st

def page_icon(emoji):
  st.write(
      f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
      unsafe_allow_html=True,)
