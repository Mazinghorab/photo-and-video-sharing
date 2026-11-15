from dotenv import load_dotenv
from imagekitio import ImageKit
import urllib.request
import os

load_dotenv()

imagekit = ImageKit(private_key=os.environ["IMAGEKIT_PRIVATE_KEY"])
URL_ENDPOINT = os.environ["IMAGEKIT_URL"]

def get_transformed_url(image_path):
  url = imagekit.helper.build_url(
      url_endpoint=URL_ENDPOINT,
      src=image_path,
      transformation=[{"width": 800, "height": 600}]
  )
  return url

def upload_image_from_url(target_url: str, file_name: str):
  with urllib.request.urlopen(target_url) as resp:
    image = resp.read()
    response = imagekit.files.upload(
      file=image,
      file_name=file_name,
      folder="/uploads",
      tags=["backend-upload"]
  )
  return response.url
