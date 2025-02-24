import streamlit as st
import pandas as pd
import os
import subprocess
from pipeline_manager import PipelineManager

# Local Save Directory
SAVE_DIR = "../../data/raw/"
FINAL_FILE_PATH = "../../data/final/merged_output.xlsx"
os.makedirs(SAVE_DIR, exist_ok=True)

# Configure Streamlit Page
st.set_page_config(
    page_title="Excel Processing - Agence Nationale de l'Auto-Entrepreneur",
    layout="wide",
    page_icon="📂"
)

# Custom Styling
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #1E3A8A;
            text-align: center;
        }
        .subheader {
            font-size: 22px;
            color: #374151;
            text-align: center;
        }
        .button {
            background-color: #1E40AF !important;
            color: white !important;
            font-size: 18px !important;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<p class='title'>📊 Agence Nationale de l'Auto-Entrepreneur</p>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Suggested Activities Filtering System</p>", unsafe_allow_html=True)

# Initialize PipelineManager
pipeline = PipelineManager()

# Function to run the processing pipeline
def run_pipeline():
    logs = []
    with st.spinner("Processing... Please wait..."):
        st.subheader("🚀 Running Data Processing Pipeline...")

        for step in pipeline.steps:
            logs.append(f"Running: {step}")
            result = subprocess.run(["python", step], capture_output=True, text=True)
            if result.returncode == 0:
                logs.append(f"✅ {step} executed successfully!")
            else:
                logs.append(f"❌ Error in {step}: {result.stderr}")
                st.error(f"Error in {step}: {result.stderr}")

        st.success("✅ Processing Completed!")

        # Show logs in an expandable section
        with st.expander("📜 View Processing Logs", expanded=False):
            st.text("\n".join(logs))



            # Provide Download Button
        with open(FINAL_FILE_PATH, "rb") as f:
                st.download_button(
                    label="📥 Download Final Processed File",
                    data=f,
                    file_name="merged_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_final"
                )

# File Upload Section
st.subheader("📤 Upload Your Excel File for Processing")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Save file locally
    file_path = os.path.join(SAVE_DIR, "preprocessed_propositions.xlsx")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded file preview
    df = pd.read_excel(file_path)
    st.subheader("📄 Uploaded File Preview")
    st.dataframe(df)

    # Process Button
    if st.button("🚀 Process Data", key="process_button"):
        run_pipeline()
