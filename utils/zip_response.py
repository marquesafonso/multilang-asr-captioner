import zipfile, os

def zip_response(temp_zip_file: str, files: list):
    with zipfile.ZipFile(temp_zip_file, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))
    with open(temp_zip_file, 'rb') as zip_file:
        zip_bytes = zip_file.read()
    return zip_bytes
