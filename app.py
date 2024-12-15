import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

# Load the dataset
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
                               'Visualizations',],
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
