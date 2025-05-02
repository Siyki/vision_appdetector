import os
import streamlit as st
import base64
from openai import OpenAI

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

st.set_page_config(
    page_title="Análisis de Imagen",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

html, body, .stApp {
    background: linear-gradient(120deg, #ccfc79, #96e6a1);
    color: #2d2d2d;
    font-family: 'Nunito', sans-serif;
    text-align: center;
}

h1, h2, h3, .stTitle, .stHeader {
    color: #3b7d4f;
    text-align: center;
}

.stButton>button {
    background-color: #3b7d4f;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}

.stImage > img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    border-radius: 12px;
}

.stTextInput > div > input,
.stTextArea > div > textarea {
    background-color: #f6fff5;
    color: #2d2d2d;
    border: 1px solid #d3e5cf;
}

.block-container {
    padding-left: 5%;
    padding-right: 5%;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠🔍 Análisis de Imagen con IA")

ke = st.text_input('🔑 Ingresa tu clave API de OpenAI')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

uploaded_file = st.file_uploader("📁 Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("🖼️ Imagen cargada", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

show_details = st.toggle("📝 ¿Deseas añadir contexto a la imagen?", value=False)

if show_details:
    additional_details = st.text_area("Agrega tu descripción o contexto aquí:")

analyze_button = st.button("🚀 Analiza la imagen", type="secondary")

if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("🔎 Analizando imagen..."):
        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe lo que ves en la imagen en español."

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o", messages=messages, max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")
else:
    if not uploaded_file and analyze_button:
        st.warning("⚠️ Por favor, sube una imagen.")
    if not api_key:
        st.warning("🔐 Por favor, ingresa tu API key.")
