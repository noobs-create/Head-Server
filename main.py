# import uvicorn

# from fastapi import FastAPI

# import config


# app = FastAPI()


# uvicorn.run(
#     app=app,
#     host=str(config.host),
#     port=int(config.port)
# )

from skinpy import Skin
from PIL import Image
from providers import geyser, mojang

import requests
import os
import tempfile

tmp = os.path.join(tempfile.gettempdir(), "HeadServer", "work")

url = "http://skinsystem.ely.by/skins/PrayoadMii.png"

response = requests.get(url=url, timeout=10)
response.raise_for_status()

with tempfile.NamedTemporaryFile(suffix=".png") as file:
    file.write(response.content)
    file.flush()

    skin = Skin.from_path(file.name)

    face = skin.head.front.image_color

    image = Image.fromarray(face, "RGBA")
    image = image.rotate(-90, expand=True)
    image = image.resize((128, 128), Image.Resampling.NEAREST)

    image.save("head.png")