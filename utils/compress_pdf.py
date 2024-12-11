from pylovepdf.tools.compress import Compress
import os
import time

c_token = os.getenv('COMPRESS_API')
def compress_pdf(input_pdf):
    # Initialize the Compress object with your public key and proxies (empty if not using a proxy)
    t = Compress(c_token, proxies={}, verify_ssl=True)
    
    # Add the file to be compressed
    t.add_file(input_pdf)
    
    t.set_output_folder('./static')

    # Execute the compression
    t.execute()
    
    # Optionally, download the compressed PDF (can be skipped in backend usage)
    t.download()

    # Give some time to ensure the file has been downloaded/created
    time.sleep(2)  # This is to make sure the download has finished (adjust if necessary)

    # Get the list of files in the output folder
    output_folder = './static'
    files_in_folder = os.listdir(output_folder)
    
    # Initialize a variable to store the path of the compressed file
    compressed_file_path = None
    
    # Iterate through the files to find one that starts with "assignment" and ends with ".pdf"
    for file_name in files_in_folder:
        if file_name.startswith('assignment') and file_name.endswith('.pdf'):
            compressed_file_path = os.path.join(output_folder, file_name)
            break  # Stop after finding the first matching file
    
    if not compressed_file_path:
        print("Error: Compressed file starting with 'assignment' not found!")
        return
    
    # Define the new name for the compressed file
    new_compressed_file_path = os.path.join(output_folder, 'compressed_assignment.pdf')

    # Rename the file to compressed_assignment.pdf
    os.rename(compressed_file_path, new_compressed_file_path)

    # Clean up by deleting the current task
    t.delete_current_task()
