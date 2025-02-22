import streamlit as st
import pandas as pd
from backend.Hakathon.src.components.pipeline_manager import PipelineManager
import subprocess

pipeline = PipelineManager()

st.title("Data Processing Pipeline")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv"]) 
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["State"] = "Pending"
    st.write("### Uploaded Dataset:")
    st.dataframe(df)
    
    if st.button("Run Pipeline"):
        with st.spinner("Processing... Please wait."):
            st.write("🚀 Running pipeline...")
            
            logs = []
            accepted_rows = set()  # Store accepted row indices
            
            for step in pipeline.steps:
                logs.append(f"Running: {step}")
                result = subprocess.run(["python", step], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logs.append(f"✅ {step} executed successfully!")
                    accepted_rows.update(df.index)  # Example: Accept all rows (modify as needed)
                else:
                    logs.append(f"❌ Error in {step}: {result.stderr}")
            
            df["State"] = df.index.map(lambda i: "Accepted" if i in accepted_rows else "Rejected")
            
            st.success("Pipeline execution completed!")
            st.write("### Processed Dataset:")
            st.dataframe(df)
            
            with st.expander("Show Logs"):
                st.text("\n".join(logs))
