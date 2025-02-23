import requests
import subprocess
import os

url = "http://127.0.0.1:5000/read"  # Your API endpoint

response = requests.get(url)

if response.status_code == 200:
    # Get the filename from the Content-Disposition header
    content_disposition = response.headers.get("Content-Disposition")
    filename = "output.xlsx"  # Default filename

    if content_disposition:
        parts = content_disposition.split("filename=")
        if len(parts) > 1:
            filename = parts[1].strip()

    # Save the Excel file
    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"File saved as {filename}")

    # Run pipeline.py after saving the file
    pipeline_path = os.path.join("Hakathon", "src", "components", "pipeline_manager.py")
    subprocess.run(["python", pipeline_path], check=True)

else:
    print(f"Failed to download file. Status code: {response.status_code}")
