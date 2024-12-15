import streamlit as st

import cv2
import numpy as np
from PIL import Image
from appointment import book_appointment
from download_model import load_remote_model


# Function to preprocess the image
def preprocess_image(image):
    image = np.array(image)  # Convert the image to a NumPy array
    image = cv2.resize(image, (128, 128))  # Resize to 128x128
    image = image / 255.0  # Normalize pixel values
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image



def upload_file_module(model):
    uploaded_file = st.file_uploader(
        "Choose an MRI image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded MRI Image", use_column_width=True)

        # Preprocess the image and make prediction
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction)

        # Display the result with emojis for visual feedback
        if predicted_class == 1:
            st.error(
                "⚠️ Tumor detected! Please consult a healthcare provider immediately. 🏥")
        else:
            st.success(
                "✅ No tumor detected. Keep up with regular health check-ups to stay healthy! 💪")

def tumor_detection_module():
    model = load_remote_model()
    st.title("🧠 Brain Tumor Detection & Appointment Booking App")
    st.write("🔍 Choose an option below to either detect a brain tumor or book an appointment for consultation.")

    # Sidebar for feature selection
    option = st.radio("Select an option",
                    ("🧠 Brain Tumor Detection", "📅 Book an Appointment"))

    if option == "🧠 Brain Tumor Detection":
        st.subheader(
            "🔬 Upload an MRI image to check for the presence of a brain tumor.")
        upload_file_module(model)
    elif option == "📅 Book an Appointment":
        book_appointment()