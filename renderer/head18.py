import requests

from skinpy import Skin
from PIL import Image
from io import BytesIO

import config

def normalize_skin(image: Image.Image):
    image = image.convert("RGBA")

    if image.size == (64, 32):
        upgraded = Image.new(
            "RGBA",
            (64, 64),
            (0, 0, 0, 0)
        )

        upgraded.paste(image, (0, 0))

        return upgraded

    return image


def render_head(skin_url: str, size: int = 128):
    response = requests.get(
        url=skin_url,
        timeout=10,
        headers={
            "User-Agent": config.user_agent
        }
    )

    response.raise_for_status()

    image = Image.open(BytesIO(response.content)).convert("RGBA")
    image = normalize_skin(image)

    skin = Skin.from_image(image)
    face = skin.head.front.image_color

    image = Image.fromarray(face, "RGBA")
    image = image.rotate(-90, expand=True)
    image = image.resize((size, size), Image.Resampling.NEAREST)
    
    output = BytesIO()

    image.save(output, format="PNG")

    return output.getvalue()