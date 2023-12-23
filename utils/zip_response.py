import zipfile, os

def zip_response(archive_name: str, files: list):
    # Create a new zip file
    with zipfile.ZipFile(archive_name, 'w') as zipf:
    # Add specific files to the zip file
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))
    return archive_name
