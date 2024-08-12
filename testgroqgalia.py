from groq import Groq
import streamlit as st

# Inicializa el cliente de Groq
client = Groq(api_key="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")

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
    st.title("Chatea con RASGAEL")
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
    
    # Mostrar mensajes previos
    for message in st.session_state['messages']:
        role = "Tu" if message["role"] == "user" else "Rasgael"
        st.write(f"**{role}:** {message['content']}")
    
    # Crear el formulario
    with st.form(key='chat_form', clear_on_submit=True):
        st.text_input("Tu:", key="user_input")
        submit_button = st.form_submit_button(label='Enviar', on_click=submit)

if __name__ == "__main__":
    chat()
