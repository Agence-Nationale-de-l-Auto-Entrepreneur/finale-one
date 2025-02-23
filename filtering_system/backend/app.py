from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from config import supabase
import pandas as pd
import io

app = Flask(__name__)
CORS(app)  # ✅ Ensure CORS is enabled for frontend communication

@app.route('/read', methods=['GET'])
def read_data():
    response = supabase.table("current_activities").select("code_activity",  "name" , "ar_name_activity" , "field").execute()
    
    if response.data:
        df = pd.DataFrame(response.data)  # Convert JSON to DataFrame
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Activities")
        
        output.seek(0)  # Reset pointer to the beginning of the file
        
        return send_file(output, download_name="activities.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    return jsonify({"message": "No records found"}), 404

@app.route('/save', methods=['POST'])
def save_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    try:
        df = pd.read_excel(file)

        # Ensure the Excel file contains the correct columns
        expected_columns = ["code_activity", "ar_description", "name_activity" , "ar_name_activity" , "subfield" , "field" , "description"]
        if not all(col in df.columns for col in expected_columns):
            return jsonify({"error": f"Missing required columns {expected_columns}"}), 400

        inserted_rows = []
        failed_rows = []

        # Insert each row one by one
        for _, row in df.iterrows():
            row_data = row.to_dict()  # Convert row to dictionary

            try:
                response = supabase.table("current_activities").insert(row_data).execute()
                inserted_rows.append(row_data)
            except Exception as e:
                failed_rows.append({"row": row_data, "error": str(e)})

        return jsonify({
            "message": "Data processing complete",
            "inserted": inserted_rows,
            "failed": failed_rows
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        # Fetch any record to test connection
        response = supabase.table("current_activities").select("*").limit(1).execute()
        
        if response.data:
            return jsonify({"message": "Connected to Supabase!", "sample_data": response.data})
        else:
            return jsonify({"message": "Connected but no data found in table!"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
