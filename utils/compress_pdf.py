import os
import time
import uuid
from pylovepdf.tools.compress import Compress
import requests

def compress_pdf(input_pdf):
    # Initialize the Compress object with your public key and proxies (empty if not using a proxy)
    t = Compress('project_public_d3eacfc89109a24a513fbb30772f1002_-jfiP41f31189c3bb504f39fbf8819b50b4e6', proxies={}, verify_ssl=True)
    
    # Add the file to be compressed
    t.add_file(input_pdf)
    
    # Set the output folder in your GitHub repository
    repo_url = 'https://api.github.com/repos/bharatmangal/generator.ai/contents/PATH'
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    # Execute the compression
    t.execute()
    
    # Optionally, wait for the compression to finish (you might need to check for the file's presence)
    time.sleep(2)  # This is to make sure the download has finished (adjust if necessary)

    # Get the list of files in the output folder (repo directory)
    response = requests.get(repo_url, headers=headers)
    files_in_folder = response.json()

    # Find the compressed file in the repo
    compressed_file_path = None
    for file_info in files_in_folder:
        if file_info['name'].startswith('assignment') and file_info['name'].endswith('.pdf'):
            compressed_file_path = file_info['download_url']  # Get the URL to download the file
            break  # Stop after finding the first matching file
    
    if not compressed_file_path:
        print("Error: Compressed file starting with 'assignment' not found!")
        return
    
    # Generate a unique filename for the new file
    timestamp = time.strftime("%m-%d-%Y-%H-%M-%S")
    new_compressed_file_name = f"compressed_assignment_{timestamp}.pdf"  # Overwrite the existing file
    new_compressed_file_path = os.path.join('https://github.com/USERNAME/REPOSITORY/contents/PATH', new_compressed_file_name)

    # Rename the file
    response = requests.put(repo_url + f'/{compressed_file_path.split("/")[-1]}', json={'path': new_compressed_file_name}, headers=headers)
    if response.status_code != 200:
        print("Error: Could not rename file.")
        return

    # Clean up by deleting the current task
    t.delete_current_task()

    return new_compressed_file_path
