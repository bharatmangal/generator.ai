from pylovepdf.tools.compress import Compress
import os
import shutil
import time

c_token = os.getenv('COMPRESS_API')

def compress_pdf(input_pdf):
    # Ensure the static directory exists
    static_path = "./static"
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    # Initialize the Compress object with your API token
    t = Compress(c_token, proxies={}, verify_ssl=True)
    
    # Add the file to be compressed
    t.add_file(input_pdf)
    
    # Set the output folder to a temporary directory
    t.set_output_folder('/tmp')

    # Execute the compression
    t.execute()
    
    # Download the compressed file
    t.download()

    # Allow time for download to finish
    time.sleep(2)

    # Locate the compressed file in the temporary output folder
    files_in_folder = os.listdir('/tmp')
    compressed_file_path = None
    
    for file_name in files_in_folder:
        if file_name.startswith('assignment') and file_name.endswith('.pdf'):
            compressed_file_path = os.path.join('/tmp', file_name)
            break
    
    if not compressed_file_path:
        raise FileNotFoundError("Error: Compressed file starting with 'assignment' not found!")

    # Create a unique filename for the compressed file
    timestamp = time.strftime("%m-%d-%Y-%H-%M-%S")
    new_compressed_file_name = f"compressed_assignment_{timestamp}.pdf"
    new_compressed_file_path = os.path.join(static_path, new_compressed_file_name)

    # Move the file from /tmp to the static folder
    shutil.move(compressed_file_path, new_compressed_file_path)

    # Clean up the task on the LovePDF API
    t.delete_current_task()

    return new_compressed_file_path
