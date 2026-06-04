import streamlit as st
from google import genai
from google.genai import types
import os

st.set_page_config(page_title="Proyecto Amber", page_icon="🤖", layout="centered")
st.title("🤖 Proyecto Amber")
st.subheader("Creador de Chatbots - Experimento 1")

# Cliente Gemini
@st.cache_resource
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Falta configurar GEMINI_API_KEY en Secrets o variables de entorno.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_instruction" not in st.session_state:
    st.write("---")
    personalidad = st.text_area(
        "Define la personalidad de tu chatbot:",
        placeholder="Ej: Eres Amber, una asistente técnica, clara y amable..."
    )

    if st.button("Iniciar Chatbot"):
        if personalidad.strip():
            st.session_state.system_instruction = personalidad.strip()
            st.session_state.messages = []
            st.rerun()
        else:
            st.warning("Escribe primero una personalidad para tu bot.")
else:
    st.sidebar.success(f"Personalidad activa:\n{st.session_state.system_instruction}")

    if st.sidebar.button("Cambiar bot / Reiniciar"):
        st.session_state.clear()
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    if user_input := st.chat_input("Escribe un mensaje a tu bot..."):
        st.session_state.messages.append({"role": "user", "text": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=st.session_state.system_instruction,
                    temperature=0.7
                )
            )

            bot_reply = response.text or "No recibí respuesta del modelo."

        except Exception as e:
            bot_reply = f"Error al llamar a Gemini: {e}"

        with st.chat_message("assistant"):
            st.write(bot_reply)

        st.session_state.messages.append({"role": "assistant", "text": bot_reply})
