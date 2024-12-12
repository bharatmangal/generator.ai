import os
import time
import base64
from pylovepdf.tools.compress import Compress
import requests

def compress_pdf(input_pdf):
    # Fetch the compression key from environment variables
    compress_key = os.getenv("COMPRESS_API")
    if not compress_key:
        print("Error: COMPRESS_KEY not set in environment variables.")
        return

    # Initialize the Compress object
    t = Compress(compress_key, proxies={}, verify_ssl=True)
    t.add_file(input_pdf)
    t.execute()
    
    # Wait for compression to finish
    time.sleep(2)

    # Fetch the compressed file from the output
    output_folder = t.get_output_files()
    compressed_file_path = output_folder[0] if output_folder else None
    if not compressed_file_path:
        print("Error: No compressed file found!")
        return

    # GitHub repository details
    repo_url = 'https://api.github.com/repos/bharatmangal/generator.ai/contents/static/'
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not set in environment variables.")
        return

    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    # Prepare the file for upload
    with open(compressed_file_path, 'rb') as f:
        file_content = f.read()
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    # Generate a unique filename
    timestamp = time.strftime("%m-%d-%Y-%H-%M-%S")
    new_file_name = f"compressed_assignment_{timestamp}.pdf"

    # Upload the file to GitHub
    payload = {
        'message': f'Upload compressed file {new_file_name}',
        'content': encoded_content,
    }

    upload_url = f"{repo_url}{new_file_name}"
    response = requests.put(upload_url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"File uploaded successfully: {new_file_name}")
        return response.json().get('content', {}).get('download_url')
    elif response.status_code == 422:
        print("Error: File already exists.")
    else:
        print(f"Error: Failed to upload file. Status Code: {response.status_code}")
        print(response.json())

    return None
