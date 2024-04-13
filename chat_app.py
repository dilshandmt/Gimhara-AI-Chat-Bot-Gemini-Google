import io
import streamlit as st
from config import init_genai
import PIL


def send_chat_message(chat, message):
    chat_response = chat.send_message(message, stream=True)
    chat_response.resolve()
    return chat_response.text


# Initialize Generative Model
model = init_genai('gemini-pro')
chat = model.start_chat(history=[])

st.set_page_config(page_title="Gemini-ChatBot", layout='wide')

st.title('Gimhara-ChatBot')
st.markdown("""
Welcome to Gmhara-ChatBot! This interactive chatbot is powered by Google's generative AI.
Feel free to ask anything and enjoy the conversation!
""")

# Using "with" notation
with st.sidebar:
    st.title('Type of input:')
    add_radio = st.radio(
        "Type of input",
        ("Text ✏", "Image 📷"),
        key='input_param',
        label_visibility='collapsed'
    )

# Initialize previous_input_type in session_state if it doesn't exist
if "previous_input_type" not in st.session_state:
    st.session_state.previous_input_type = None

# Check if the input type has changed
if st.session_state.previous_input_type != add_radio:
    # Clear the messages
    st.session_state.messages = []
    # Update previous_input_type
    st.session_state.previous_input_type = add_radio

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])

if add_radio == 'Text ✏':
    model = init_genai("gemini-pro")
    prompt = st.chat_input("Ask anything")

    if prompt:
        message = prompt
        st.session_state.messages.append({
            "role": "user",
            "parts": [message],
        })
        with st.chat_message("user"):
            st.markdown(prompt)
        response = model.generate_content(st.session_state.messages)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(response.text)
        st.session_state.messages.append({
            "role": "model",
            "parts": [response.text],
        })

elif add_radio == 'Image 📷':
    # st.warning("Please upload an image then ask question!", icon="🤖")
    model = init_genai("gemini-pro-vision")

    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    prompt = st.chat_input("Ask anything")

    if image and prompt:
        st.session_state.messages = []
        # save image to buffer
        buffer = io.BytesIO()
        PIL.Image.open(image).save(buffer, format="JPEG")
        image_input = PIL.Image.open(buffer)
        st.session_state.messages.append({
            "role": "user",
            "parts": [image_input],
        })
        with st.chat_message("user"):
            st.image(image_input, width=300)
            st.markdown(prompt)
        response = model.generate_content(st.session_state.messages)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(response.text)
        st.session_state.messages.append({
            "role": "model",
            "parts": [response.text],
        })
