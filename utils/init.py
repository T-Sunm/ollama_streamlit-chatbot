import streamlit as st
from utils.process import extract_model_names
import ollama
from utils.icon import page_icon
def init():
  st.set_page_config(
      page_icon="💬",
      page_title="My Chat",
      layout="wide",
      initial_sidebar_state="expanded"
  )
  st.header("Your own ChatGpt ")

  available_models = extract_model_names(models_info=ollama.list())

  if available_models:
    selected_model = st.selectbox(
        "Pick a model available locally on your system", available_models
    )
  else:
    st.warning("You have not pulled any model from Ollama yet!", icon="⚠️")
    if st.button("Go to settings to download a model"):
      st.switch_page("pages/03_⚙_Settings.py")

  message_container = st.container(height=500, border=True)
  if "messages" not in st.session_state:
    st.session_state.messages = []
  return (message_container, selected_model)


def init_multimodal_page():
  st.subheader("LLaVA 1.6 Playground", divider="red", anchor=False)

  if "chats" not in st.session_state:
    st.session_state.chats = []
  if "upload_file_state" not in st.session_state:
    st.session_state.upload_file_state = None
