from flask import Flask, request, jsonify
from config import supabase
from services import process_xls_file

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_xls():
    file = request.files['file']
    if file:
        result = process_xls_file(file)
        return jsonify({"message": "File processed", "data": result})
    return jsonify({"error": "No file uploaded"}), 400

