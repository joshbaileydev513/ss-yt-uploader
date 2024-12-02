from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os

# Authenticate and build the API client
def get_authenticated_service():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    credentials = None

    # Load existing credentials
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # Refresh or request new credentials
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            credentials = flow.run_console()

        # Save credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

# Upload video
def upload_video(file, title, description, tags):
    try:
        youtube = get_authenticated_service()
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22",  # Category 22 = "People & Blogs"
                },
                "status": {"privacyStatus": "public"},
            },
            media_body=MediaFileUpload(file, chunksize=-1, resumable=True),
        )
        response = request.execute()
        print(f"Video uploaded: {response['id']}")
    except HttpError as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    upload_video("path_to_video.mp4", "Relaxing Rain Sounds", "Enjoy calming rain with soothing visuals.", ["relaxation", "rain", "ASMR"])
