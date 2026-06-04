import streamlit as st
from google import genai
from google.genai import types

# Configuración visual de la página web
st.set_page_config(page_title="Proyecto Amber", page_icon="🤖", layout="centered")
st.title("🤖 Proyecto Amber")
st.subheader("Creador de Chatbots - Experimento 1")

# Inicializa el cliente de Gemini
# Inicializa el cliente de Gemini pasándole la clave directamente
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

# Inicializa el historial de mensajes si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Panel de Configuración de Personalidad
if "system_instruction" not in st.session_state:
    st.write("---")
    personalidad = st.text_input("Define la personalidad de tu chatbot:", placeholder="Ej: Eres un pirata...")
    if st.button("Iniciar Chatbot"):
        if personalidad:
            st.session_state.system_instruction = personalidad
            st.rerun()
else:
    # 2. Interfaz de Chat (Barra lateral)
    st.sidebar.success(f"Personalidad activa:\n'{st.session_state.system_instruction}'")
    if st.sidebar.button("Cambiar bot / Reiniciar"):
        del st.session_state.system_instruction
        st.session_state.messages = [] # Limpia los mensajes viejos
        st.rerun()

    # Mostrar los mensajes que ya se enviaron anteriormente
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    # Caja para que el usuario escriba un mensaje nuevo
    if user_input := st.chat_input("Escribe un mensaje a tu bot..."):
        # 1. Mostrar y guardar el mensaje del usuario
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "text": user_input})
        
        # 2. Construir el historial en el formato que Google Gemini exige
        historial_gemini = []
        for m in st.session_state.messages[:-1]: # Toma todos los mensajes anteriores
            historial_gemini.append(
                types.Content(
                    role="user" if m["role"] == "user" else "model",
                    parts=[types.Part.from_text(text=m["text"])]
                )
            )
        
        # 3. Mandar toda la conversación junta a Google con su personalidad
        config_ia = types.GenerateContentConfig(
            system_instruction=st.session_state.system_instruction,
            temperature=0.7
        )
        
        # Llamada directa al modelo usando la sesión unificada
        response = st.session_state.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=historial_gemini + [user_input],
            config=config_ia
        )
        
        # 4. Mostrar y guardar la respuesta de la IA
        with st.chat_message("assistant"):
            st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "text": response.text})
