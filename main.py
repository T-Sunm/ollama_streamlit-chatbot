import streamlit as st
from streamlit_chat import message
from langchain_community.chat_models import ChatOllama
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from utils.init import init
def main():
  llm = ChatOllama(model="mistral")
  init()
  messages = [
      SystemMessage(content="You are a helpful assistant")
  ]
  if prompt := st.chat_input("Say something"):
    message(prompt, is_user=True)
    messages.append(HumanMessage(content=prompt))
    response = llm.invoke(prompt)
    message(response.content, is_user=False)


if __name__ == "__main__":
  main()
