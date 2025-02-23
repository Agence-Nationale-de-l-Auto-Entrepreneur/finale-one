import pandas as pd

def merge_excel_files(final_suggested_path, preprocessed_path, output_path):
    # Load the Excel files
    final_suggested_df = pd.read_excel(final_suggested_path)
    preprocessed_df = pd.read_excel(preprocessed_path)
    
    # Ensure 'code_pro' column exists
    if "code_pro" not in final_suggested_df.columns or "code_pro" not in preprocessed_df.columns:
        raise ValueError("Both input files must have a 'code_pro' column.")

    # Create a new DataFrame to store results
    merged_df = preprocessed_df.copy()
    
    # Assign machine_decision and human_decision columns
    merged_df["machine_decision"] = merged_df["code_pro"].apply(
        lambda x: "accepted" if x in final_suggested_df["code_pro"].values else "not accepted"
    )
    merged_df["human_decision"] = "not decided"

    # Ensure accepted ones appear at the top in the same order as in final_suggested_df
    merged_df["order"] = merged_df["code_pro"].apply(
        lambda x: final_suggested_df["code_pro"].tolist().index(x) if x in final_suggested_df["code_pro"].values else float('inf')
    )
    
    # Sort based on 'order' column
    sorted_df = merged_df.sort_values(by="order").drop(columns=["order"])
    sorted_df.drop(columns=['Unnamed: 0'], inplace=True)
    
    # Save the result to an Excel file
    sorted_df.to_excel(output_path, index=False)
    
# Example usage
merge_excel_files("../../data/final/final_suggested_activities.xlsx", "../../data/raw/preprocessed_propositions.xlsx", "../../data/final/merged_output.xlsx")