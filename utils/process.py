import ollama
import streamlit as st
import time
from io import BytesIO
from PIL import Image
import base64
def extract_model_names(models_info: dict):
  return tuple([model["name"] for model in models_info["models"]])

def get_allowed_model_names(models_info: dict):
  allowed_models = ["bakllava:latest", "llava:latest"]
  available_models = extract_model_names(models_info)
  return tuple(
      [model for model in available_models if model in allowed_models]
  )

def download_model(modal_to_download):
  try:
    start_time = time.time()
    with st.spinner(f"Downloading model: {modal_to_download}"):
      ollama.pull(modal_to_download)
    end_time = time.time()
    elapsed_time = end_time - start_time
    st.toast(
        f"""Downloaded model: {modal_to_download} in {elapsed_time:.2f} seconds""", icon="✅"
    )
    st.experimental_rerun()
  except Exception as e:
    st.error(
        f"""Failed to download model: {modal_to_download}. Error: {str(e)}""",
        icon="😳",
    )
def get_image_base64(image: Image):
  buffered = BytesIO()
  image.save(buffered, format="PNG")
  return base64.b64encode(buffered.getvalue()).decode()
