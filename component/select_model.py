
from utils.process import get_allowed_model_names, download_model, get_image_base64
import ollama
import streamlit as st
import time

def select_model():
  models_info = ollama.list()
  available_models = get_allowed_model_names(models_info)
#  trả về một tập hợp mới chứa các phần tử chỉ có trong tập hợp thứ nhất và không có trong tập hợp thứ hai.
  missing_models = set(
      ["bakllava:latest", "llava:latest"]) - set(available_models)
  col_1, col_2 = st.columns(2)

  with col_1.popover("⚙️ Model Management", help="Manage models here"):
    if not available_models:
      st.error("No allowed models are available.", icon="😳")
      modal_to_download = st.selectbox(
          "Select a modal to download", ["bakllava:latest", "llava:latest"])
      if st.button(f"Download {modal_to_download}"):
        download_model(modal_to_download)
    else:
      if missing_models:
        modal_to_download = st.selectbox(
            # :green : tô màu xanh cho văn bản
            # ** ** : in đậm văn bản
            ":green[**📥 DOWNLOAD MODEL**]", list(missing_models))
        if st.button(f"Download {modal_to_download}"):
          download_model(modal_to_download)
      selected_model_delete = st.selectbox(
          ":red[**⛔️ DELETE MODEL**]", available_models)
      if st.button(f"Delee **_{selected_model_delete}_**"):
        try:
          start_time = time.time()
          with st.spinner(f"Deleting model: {selected_model_delete}"):
            ollama.delete(selected_model_delete)
          end_time = time.time()
          elapsed_time = end_time - start_time
          st.toast(
              f"Deleted model: {selected_model_delete} in {elapsed_time:.2f} seconds", icon="✅")
          st.rerun()
        except Exception as e:
          st.error(
              f"""Failed to download model: {
                                  modal_to_download}. Error: {str(e)}""",
              icon="😳",
          )
      selected_model = col_2.selectbox(
          "Pick a model available locally on your system", available_models, key=1
      )

      return selected_model
