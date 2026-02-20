import streamlit as st
import google.generativeai as genai

# Configuración de la interfaz
st.set_page_config(page_title="Prototipo AI Gen GR", page_icon="🤖")
st.title("🤖 Asistente Virtual - AI Gen GR")
st.write("Prueba nuestro agente inteligente de atención al cliente.")

# AQUÍ DEBES PEGAR TU API KEY DE GOOGLE ENTRE LAS COMILLAS
API_KEY = "AIzaSyDIuDVlTWIhazP_1yZ5JnblQZlh_V36_Lg"

# Autenticación y configuración del modelo
genai.configure(api_key=API_KEY)
# Ocultar menú de Streamlit y marca de agua
ocultar_estilo = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(ocultar_estilo, unsafe_allow_html=True)


instrucciones = """
Eres el asistente virtual de la Clínica Estética 'Lumina', desarrollado por AI Gen GR.
Tu tono es amable y conciso (máximo 3 líneas).
Servicios: Limpieza facial ($15.000) y Masajes ($20.000). Horario: Lunes a Viernes de 9 a 18hs.
Tu objetivo es responder dudas y pedir el nombre y teléfono del cliente para agendar un turno.
Si preguntan algo fuera de estos servicios, di amablemente que no tienes esa información.
"""

modelo = genai.GenerativeModel("gemini-2.5-flash", system_instruction=instrucciones)

# Memoria del chat
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

# Interacción
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.mensajes.append({"rol": "user", "contenido": prompt})

    historial_ia = [
        {"role": "user" if m["rol"] == "user" else "model", "parts": [m["contenido"]]} 
        for m in st.session_state.mensajes[:-1]
    ]

    chat = modelo.start_chat(history=historial_ia)
    respuesta = chat.send_message(prompt)

    with st.chat_message("assistant"):
        st.markdown(respuesta.text)
    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta.text})
