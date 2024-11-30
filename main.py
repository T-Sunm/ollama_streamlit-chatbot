import streamlit as st
from streamlit_chat import message
from langchain_community.chat_models import ChatOllama
from utils.init import init

from openai import OpenAI
def main():
  llm = OpenAI(
      base_url="http://localhost:12345/v1",
      api_key="ollama",
  )
  message_container, selected_model = init()


# ----------chat------------
  if prompt := st.chat_input("Say something"):
    try:
      st.session_state.messages.append(
          {"role": "user", "content": prompt}
      )
      message_container.chat_message("user", avatar="😎").markdown(prompt)

      # vì message stream nên phải xài with
      with message_container.chat_message("assistant", avatar="🤖"):
        with st.spinner("Model working"):
          response_stream = llm.chat.completions.create(
              model=selected_model,
              # format mesage của opanai khi gửi prompt
              messages=[
                  # tải lịch sử cuộc trò chuyện vào list message để duy trì ngữ cảnh câu chuyện
                  {"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages
              ],
              stream=True
          )
          response = st.write_stream(response_stream)
      st.session_state.messages.append(
          {"role": "assistant", "content": response})
    except Exception as e:
      st.error(e, icon="⛔️")


if __name__ == "__main__":
  main()
