from groq import Groq
import streamlit as st
from PIL import Image

# Inicializa el cliente de Groq
client = Groq(api_key="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")

# Carga las imágenes y ajusta el tamaño
logo_image = Image.open("/mount/src/streamlit-ia/icons/logo-ia.png")  # Imagen del logo junto al título
logo_image = logo_image.resize((70, 70))  # Ajusta el tamaño del logo

user_icon_image = Image.open("/mount/src/streamlit-ia/icons/icono-user.png")  # Imagen del icono del usuario
user_icon_image = user_icon_image.resize((50, 50))  # Ajusta el tamaño del icono del usuario

bot_icon_image = Image.open("/mount/src/streamlit-ia/icons/logo-ia.png")  # Imagen del icono de RASGAEL
bot_icon_image = bot_icon_image.resize((50, 50))  # Ajusta el tamaño del icono de RASGAEL

# Agrega el CSS para ajustar el tamaño de las imágenes en dispositivos móviles
st.markdown("""
  <style>
    @media only screen and (max-width: 768px) {
      img {
        zoom: 0.2; /* Reduce el tamaño de la imagen al 20% */
      }
      .css-1v3fvcr {
        flex-direction: row;
      }
      .css-1v3fvcr > div {
        margin: 0;
        padding: 0;
      }
    }
  </style>
""", unsafe_allow_html=True)

def get_ia_response(messages):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
    )
    
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

def chat():
    col1, col2 = st.columns([1, 0.1])
    
    # Título con imagen de logo a la derecha
    with col1:
        st.title("Chatea con RASGAEL")
    with col2:
        st.image(logo_image, use_column_width=True)
    
    st.write("Bienvenido al chat con IA! Escribe 'salir' para terminar la conversación")
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    def submit():
        user_input = st.session_state.user_input
        if user_input.lower() == 'salir':
            st.write("Gracias por chatear! ¡Adiós!")
            st.stop()
            
        st.session_state['messages'].append({"role": "user", "content": user_input})
        
        with st.spinner("Obteniendo respuesta..."):
            ia_response = get_ia_response(st.session_state['messages'])
            st.session_state['messages'].append({"role": "assistant", "content": ia_response})
        
        st.session_state.user_input = ""  # Limpiar el campo de entrada
    
    # Mostrar mensajes previos con iconos
    for message in st.session_state['messages']:
        col1, col2 = st.columns([0.1, 2])
        if message["role"] == "user":
            with col1:
                st.image(user_icon_image, use_column_width=True)
            with col2:
                st.write(f"**TU:** {message['content']}")
                # st.markdown("<hr style='border-top: 1px solid #ccc'>", unsafe_allow_html=True)
        else:
            st.markdown("<hr style='border-top: 1px solid #ccc'>", unsafe_allow_html=True)
            with col1:
                st.image(bot_icon_image, use_column_width=True)
            with col2:
                st.write(f"**RASGAEL:** {message['content']}")
    
    # Crear el formulario
    with st.form(key='chat_form', clear_on_submit=True):
        st.text_input("Tu:", key="user_input")
        submit_button = st.form_submit_button(label='Enviar', on_click=submit)

if __name__ == "__main__":
    chat()
