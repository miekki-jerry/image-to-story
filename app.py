import streamlit as st
from PIL import Image
import requests
import os

# Import your functions
from main import img2text, generate_story, text2speech

st.title('Image to Story Generator')

# Switch between Hugging Face and Replicate model
use_hf = st.selectbox('Select Model', ['Hugging Face', 'Replicate'])

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    
    if st.button('Generate Story'):
        with st.spinner('Generating...'):
            scenario = img2text(image, use_hf=(use_hf == 'Hugging Face'))
            
            # Show image caption
            with st.expander('Show image caption'):
                st.write(scenario)

            story = generate_story(scenario)
            text2speech(story)
            st.success('Story generated!')

            with st.expander('Show image story'):
                st.write(story)

            st.audio('audio.flac')
