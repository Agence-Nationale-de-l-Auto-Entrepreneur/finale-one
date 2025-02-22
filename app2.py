import streamlit as st
import pandas as pd
import subprocess
import os
from backend.Hakathon.src.components.pipeline_manager import PipelineManager

pipeline = PipelineManager()

st.title("Data Processing Pipeline")

# File uploader for user input
data_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if st.button("Run Pipeline"):
    if data_file is None:
        st.error("Please upload a data file before running the pipeline.")
    else:
        with st.spinner("Processing... Please wait."):
            st.write("🚀 Running pipeline...")
            
            logs = []
            processed_data = []  # To store pipeline results
            
            # Read user data
            try:
                if data_file.name.endswith(".csv"):
                    user_df = pd.read_csv(data_file)
                else:
                    user_df = pd.read_excel(data_file)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                st.stop()
            
            for step in pipeline.steps:
                logs.append(f"Running: {step}")
                try:
                    result = subprocess.run(["python", step], capture_output=True, text=True, check=True)
                    logs.append(f"✅ {step} executed successfully!")
                    
                    output_file = f"output_{step}.csv"
                    if os.path.exists(output_file):
                        df = pd.read_csv(output_file)
                        processed_data.append(df)
                    else:
                        logs.append(f"⚠️ No output file found for {step}.")
                except subprocess.CalledProcessError as e:
                    logs.append(f"❌ Error in {step}: {e.stderr}")
            
            st.success("Pipeline execution completed!")
            
            if processed_data:
                final_df = pd.concat(processed_data, ignore_index=True)
                final_df["Status"] = "Accepted"
                
                # Merge for accurate matching
                user_df = user_df.merge(final_df, how="left", indicator=True)
                user_df["Status"] = user_df["_merge"].apply(lambda x: "Accepted" if x == "both" else "Rejected")
                user_df.drop(columns=["_merge"], inplace=True)
            else:
                user_df["Status"] = "Rejected"
            
            # Display results
            st.subheader("Pipeline Output")
            st.dataframe(user_df)
            
            # Show logs
            with st.expander("Show Logs"):
                st.text("\n".join(logs))
