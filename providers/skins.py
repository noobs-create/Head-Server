import requests

from libs import console
from providers.geyser import resolve_geyser_url
from providers.mojang import resolve_mojang_url

import config


def resolve_skin_url(username: str):
    console.log(f"Resolving Skin For: {username}")

    providers = [config.default] + config.fallbacks

    for provider in providers:
        try:
            if username.startswith(str(config.bedrock_prefix)):
                console.info(f"{str(username)} Might Be A Bedrock Player! Threating Them!")

                skin_url = resolve_geyser_url(username.removeprefix(str(config.bedrock_prefix)))

                if skin_url is None:
                    continue

                return skin_url

            if provider.lower() == "bedrock":
                skin_url = resolve_geyser_url(username.removeprefix(str(config.bedrock_prefix)))

                if skin_url is None:
                    continue

                return skin_url
            
            if provider.lower() == "mojang":
                skin_url = resolve_mojang_url(username)

                if skin_url is None:
                    continue

                return skin_url

            skin_url = provider.replace(
                "{username}",
                username
            )

            response = requests.get(
                skin_url,
                timeout=10,
                headers={
                    "User-Agent": config.user_agent
                }
            )

            response.raise_for_status()

            return skin_url

        except Exception as e:
            console.warn(
                f"Skin Provider Failed For {str(provider)} Got {str(e)}"
            )

            continue

    console.warn(
        f"Could Not Find A Skin For {str(username)}"
    )

    return None