#testing background removing, download button doesn't work, need to save via right mouse click

from rembg import remove
import cv2
import streamlit as st
import numpy as np
from PIL import Image
import io

def composite_transparent_image_over_background(image):
    background = np.ones_like(image, dtype=np.uint8) * 255  # Create a white background
    alpha_channel = image[:, :, 3]
    for channel in range(0, 3):  # For each RGB channel
        background[:, :, channel] = (image[:, :, channel] * (alpha_channel / 255.0) +
                                      background[:, :, channel] * (1.0 - alpha_channel / 255.0))
    return background

# Streamlit app title
st.title("Background Remover")

# Upload image via Streamlit
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

# Process the uploaded image
if uploaded_image is not None:
    # Convert uploaded image to OpenCV format
    image_stream = io.BytesIO(uploaded_image.read())
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Show original image
    st.subheader("Original Image")
    st.image(image, channels="BGR", use_column_width=True)

    # Remove background
    output = remove(image)

    # Composite image over white background
    composited_image = composite_transparent_image_over_background(output)

    # Show processed image
    st.subheader("Processed Image")
    st.image(composited_image, channels="BGR", use_column_width=True)

    # Download processed image
    if st.button("Download Processed Image"):
        im_pil = Image.fromarray(composited_image, "RGB")
        img_buffer = io.BytesIO()
        im_pil.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        st.download_button(
            "Download Image",
            img_buffer,
            file_name="processed.png",
            mime="image/png",
        )
