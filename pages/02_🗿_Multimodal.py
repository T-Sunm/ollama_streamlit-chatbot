import streamlit as st
import requests
from PIL import Image
import json
import ollama
from utils.icon import page_icon
from utils.process import get_allowed_model_names, download_model, get_image_base64
from utils.init import init_multimodal_page
from component.select_model import select_model
import time

st.set_page_config(
    page_title="LLaVA Playground",
    page_icon="🗿",
    layout="wide",
    initial_sidebar_state="expanded",
)
def main():
  page_icon("🗿")

  init_multimodal_page()

  selected_model = select_model()

  uploaded_file = st.file_uploader(
      "Upload an image for analysis", type=["png", "jpg", "jpeg"]
  )

  col_1, col_2 = st.columns(2)

  with col_2:
    if uploaded_file is not None:
      st.session_state.upload_file_state = uploaded_file.getvalue()
      image = Image.open(uploaded_file)
      image_base64 = get_image_base64(image)

      # xài html để chỉnh height flexible hơn, xài height:auto để chiều cao tự dãn ra
      st.markdown(f"""
        <div style="border: 1px solid; padding: 10px; width:100%; height:auto;">
            <img src="data:image/png;base64,{image_base64}"
                 style="width: 100%;" alt="{uploaded_file.name}">
        </div>
        """, unsafe_allow_html=True)

  with col_1:
    container1 = st.container(height=500, border=True)

    if uploaded_file is not None:

      if user_input := st.chat_input(
          "Question about the image...", key="chat_input"
      ):
        st.session_state.chats.append({"role": "user", "content": user_input})
        container1.chat_message("user", avatar="🫠").markdown(user_input)

# https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion

#  api generate dựa tên ảnh
      API_URL = "http://localhost:12345/api/generate"
      headers = {
          "Content-Type": "application/json",
          "Accept": "application/json",
      }
      data = {
          "model": selected_model,
          "prompt": user_input,
          "images": [image_base64],
      }
      if user_input:
        with container1.chat_message("assistant", avatar="🗿"):
          with st.spinner(":blue[processing...]"):
            response = requests.post(API_URL, json=data, headers=headers)
          if response.status_code == 200:

            # response return về string, trong string chứa nhiều hàng obj response nhỏ, dùng split("/n") chia chúng thành mảng
            response_lines = response.text.split("\n")
            llava_response = ""
            response_container = st.empty()
            try:
              for res_line in response_lines:
                response_data = json.loads(res_line)
                if "response" in response_data:
                  llava_response += response_data["response"]

                  #  sài response_container viết từng từ vào để ui hiển thị như write_stream
                  response_container.write(llava_response)
                  time.sleep(0.1)
            except json.JSONDecodeError:
              pass  # Skip invalid JSON lines


if __name__ == "__main__":
  main()
