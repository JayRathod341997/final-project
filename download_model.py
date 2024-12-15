# import tensorflow as tf
from tensorflow.keras.models import load_model
import gdown 
import streamlit as st

@st.cache_resource  # Cache to avoid re-downloading on every run
def load_remote_model():
    file_id = "1a7gwpStIqHJRUCDtI9Jw6m_Qzma_WFHN"  # Replace with your file ID
    url = f"https://drive.google.com/uc?id={file_id}"
    output_file = "brain_tumor_cnn_model_1.h5"
    gdown.download(url, output_file, quiet=False)
    return load_model(output_file)