import streamlit as st
from groq import Groq
import os

st.set_page_config(
    page_title="START IA",
    page_icon="🤖",
    layout="centered"
)

# API KEY (desde variable de entorno)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# SIDEBAR
with st.sidebar:
    st.image("assets/logo.png", width=200)
    st.title("START IA")
    st.write("Asistente inteligente")

    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hola, soy START IA. ¿En qué puedo ayudarte?"}
        ]
        st.rerun()

    st.markdown("---")
    st.caption("IA online gratuita")

# HEADER
col1, col2 = st.columns([1,3])

with col1:
    st.image("assets/logo.png", width=90)

with col2:
    st.title("START IA")
    st.caption("Tu asistente inteligente")

st.divider()

# MEMORIA
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Eres un asistente llamado START IA. Fuiste creado por Luiggi Castillo Atoche. Si alguien pregunta quién es tu creador o quién te desarrolló, debes responder que tu creador es Luggi Castillo Atoche, Tecnico en Ingenieria de Ciberseguridad."
        },
        {
            "role": "assistant",
            "content": "Hola, soy START IA. ¿En qué puedo ayudarte?"
        }
    ]

# MOSTRAR CHAT
for message in st.session_state.messages:
    if message["role"] != "system":

        avatar = None
        if message["role"] == "assistant":
            avatar = "assets/logo.png"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# INPUT
prompt = st.chat_input("Escribe tu pregunta...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="assets/logo.png"):

        with st.spinner("Pensando..."):

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                temperature=0.7
            )

            reply = completion.choices[0].message.content

            st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )
