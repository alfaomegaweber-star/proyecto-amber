import streamlit as st
from google import genai
from google.genai import types

# Configuración visual de la página web
st.set_page_config(page_title="Proyecto Amber", page_icon="🤖", layout="centered")
st.title("🤖 Proyecto Amber")
st.subheader("Creador de Chatbots - Experimento 1")

# Inicializa el cliente de Gemini
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

# 1. Panel de Configuración de Personalidad
if "system_instruction" not in st.session_state:
    st.write("---")
    personalidad = st.text_input("Define la personalidad de tu chatbot:", placeholder="Ej: Eres un pirata...")
    if st.button("Iniciar Chatbot"):
        if personalidad:
            st.session_state.system_instruction = personalidad
            st.session_state.chat_session = st.session_state.client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(system_instruction=personalidad, temperature=0.7)
            )
            st.rerun()
else:
    # 2. Interfaz de Chat
    st.sidebar.success(f"Personalidad activa:\n'{st.session_state.system_instruction}'")
    if st.sidebar.button("Cambiar bot / Reiniciar"):
        del st.session_state.system_instruction
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    if user_input := st.chat_input("Escribe un mensaje a tu bot..."):
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "text": user_input})
        
        response = st.session_state.chat_session.send_message(user_input)
        
        with st.chat_message("assistant"):
            st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "text": response.text})
