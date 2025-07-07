from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app.auth import get_drive_service

FOLDER_ID = "your-folder-id-here"

def upload_to_drive(file_path: str):
    service = get_drive_service()
    file_metadata = {
        "name": file_path.split("/")[-1],
        "parents": [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype="audio/wav")
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"📁 Uploaded to Drive with ID: {file.get('id')}")
