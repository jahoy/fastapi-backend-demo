import requests
from utils.config import UPLOAD_PHOTO_URL


async def upload_image_to_server(file):
    result = requests.post(UPLOAD_PHOTO_URL, files={"image": file})
    print(result.json())
