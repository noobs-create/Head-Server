from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, RedirectResponse, FileResponse

from skinpy import Skin
from PIL import Image
from providers import skins

import requests
from io import BytesIO
import uvicorn

import config


app = FastAPI(
    title="Head Server",
    description="The All-In-One Minecraft Head/Face Skin Server!",
    version="0.1.0"
)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")

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


@app.get("/{username}.png")
def get_head(username: str, mode: str = Query(default=None)):
    skin_mode = (
        mode
        if mode is not None
        else config.default_skin_mode
    ).lower()

    if skin_mode not in (
        "head",
        "head-1-8"
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported skin mode: {skin_mode}"
        )

    skin_url = skins.resolve_skin_url(
        username
    )

    if skin_url is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find skin for {username}"
        )

    try:
        image = render_head(
            skin_url
        )

        return Response(
            content=image,
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=300"
            }
        )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to download skin: {e}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to render skin: {e}"
        )


@app.get("/{username}")
def get_redirect(username: str, just_redirect: bool = False):
    if not just_redirect:
        return get_head(username=username)

    skin_url = skins.resolve_skin_url(username)

    if skin_url is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find skin for {username}"
        )

    return RedirectResponse(
        url=skin_url,
        status_code=301
    )


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=str(config.host),
        port=int(config.port)
    )