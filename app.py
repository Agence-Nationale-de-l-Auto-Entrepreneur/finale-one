import streamlit as st
import pandas as pd
import os
import subprocess

# Local Save Directory
SAVE_DIR = "./backend/Hakathon/data/raw/"
os.makedirs(SAVE_DIR, exist_ok=True)

st.set_page_config(page_title="Excel File Processor", layout="wide")
st.title("📊 Advanced Excel File Processor")

# Function to start backend pipeline (without any API)
def run_pipeline():
    # Run the pipeline manager script (backend/hakathon/src/components/pipeline_manager.py)
    command = ["python", "backend/hakathon/src/components/pipeline_manager.py"]
    
    # Print the command for debugging
    st.write(f"Running command: {' '.join(command)}")
    
    try:
        # Use subprocess.run() instead of Popen for blocking call
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # If execution is successful, print the output
        st.success("✅ Processing completed successfully!")
        st.text(result.stdout)  # Show the stdout from the script

    except subprocess.CalledProcessError as e:
        # If there is an error, show the stderr
        st.error(f"❌ Processing failed! Error: {e}")
        st.text(e.stderr)

# File Upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    st.write("Saving file locally...")
    
    # This ensures the file is always saved as 'preprocessed_propositions.xlsx'
    file_path = os.path.join(SAVE_DIR, "preprocessed_propositions.xlsx")

    # Save the uploaded file with the desired name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File saved locally!")

    # Display file details
    st.subheader("File Details")
    df = pd.read_excel(file_path)
    st.dataframe(df)

    # Provide options for further processing
    if st.button("Process Data"):
        # Show a spinner while the pipeline is running
        with st.spinner("🔄 Running the pipeline... Please wait..."):
            run_pipeline()  # Wait for the pipeline to complete before continuing
        st.success("✅ Pipeline execution complete!")
