import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage

class StreamHandler(BaseCallbackHandler):
    def __init__(self,container,initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self,token: str,**kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

with st.sidebar:
    open_api_key = st.text_input("OPENAI API KEY",type="password")

if "messages" not in st.session_state:
    st.session_state['messages'] = [ChatMessage(role="Assistant",content="Hi I am your new assistant")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt:= st.chat_input():
    st.session_state.messages.append(ChatMessage(role='User',content=prompt))
    st.chat_message("user").write(prompt)

    if not open_api_key:
        st.info("please enter a valid open api key")
        st.stop()

    with st.chat_message('assistant'):
        streamhandler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=open_api_key,streaming=True,callbacks=[streamhandler])
        response = llm(st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="Assistant",content=response.content))
