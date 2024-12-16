import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

import numpy as np
from PIL import Image
from appointment import book_appointment
from tensorflow.keras.models import load_model
import gdown 
# import cv2


@st.cache_resource  # Cache to avoid re-downloading on every run
def load_remote_model():
    file_id = "1a7gwpStIqHJRUCDtI9Jw6m_Qzma_WFHN"  # Replace with your file ID
    url = f"https://drive.google.com/uc?id={file_id}"
    output_file = "brain_tumor_cnn_model_1.h5"
    gdown.download(url, output_file, quiet=False)
    return load_model(output_file)

# Function to preprocess the image
def preprocess_image(image):
    image = np.array(image)  # Convert the image to a NumPy array
    # image = cv2.resize(image, (128, 128))  # Resize to 128x128
    image = image / 255.0  # Normalize pixel values
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image





uploaded_file = './mental_health_diagnosis_treatment_.csv'




data = pd.read_csv(uploaded_file)
st.set_page_config(page_title="Brain Diagnosis & Appointment", page_icon="🩺", layout="wide")
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .main {
            padding: 20px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)
# Streamlit app setup
st.title("Mental Health Diagnosis and Treatment Analysis")
st.write("This app provides insights into the mental health diagnosis dataset.")
with st.sidebar:
    menu = option_menu('Mental Health Diagnosis and Treatment Analysis',
                              ['Overview','Statistics',
                               'Visualizations','Tumor detection'],
                              icons=['dashboard','activity','heart','person','line-chart'],
                              default_index=0)

if menu == "Overview":
    st.header("Dataset Overview")
    st.write("Here are the first few rows of the dataset:")
    st.dataframe(data.head(20))

elif menu == "Statistics":
    st.header("Descriptive Statistics")
    st.write("The following table shows key statistical measures:")
    st.write(data.describe())


elif menu == "Visualizations":
    st.header("Data Visualizations")

    # Additional Visualizations
    st.subheader("Distributions of Key Columns")
    columns_to_plot = [ 'Age', 'Symptom Severity (1-10)', 'Mood Score (1-10)', 'Sleep Quality (1-10)',
                       'Physical Activity (hrs/week)', 'Treatment Duration (weeks)', 'Stress Level (1-10)',
                       'Treatment Progress (1-10)', 'Adherence to Treatment (%)']

    plt.figure(figsize=(15, 10))
    for i, column in enumerate(columns_to_plot, 1):
        plt.subplot(3, 4, i)
        sns.histplot(data[column], kde=True, bins=30)
        plt.title(f'Distribution of {column}')

    plt.tight_layout()
    st.pyplot(plt)

    # Select a column for visualization
    columns = data.columns[1:]
    selected_column = st.selectbox("Select a column to visualize", columns)

    if data[selected_column].dtype in ['int64', 'float64']:
        st.subheader(f"Distribution of {selected_column}")
        fig, ax = plt.subplots()
        sns.histplot(data[selected_column], kde=True, ax=ax)
        st.pyplot(fig)

    elif data[selected_column].dtype == 'object':
        st.subheader(f"Counts of {selected_column}")
        fig, ax = plt.subplots()
        data[selected_column].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    else:
        st.write("Visualization for this data type is not supported.")

elif menu == "Tumor detection":
    model = load_remote_model()
    st.title("🧠 Brain Tumor Detection & Appointment Booking App")
    st.write("🔍 Choose an option below to either detect a brain tumor or book an appointment for consultation.")

    # Sidebar for feature selection
    option = st.radio("Select an option",
                    ("🧠 Brain Tumor Detection", "📅 Book an Appointment"))

    if option == "🧠 Brain Tumor Detection":
        st.subheader(
            "🔬 Upload an MRI image to check for the presence of a brain tumor.")
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
    elif option == "📅 Book an Appointment":
        book_appointment()