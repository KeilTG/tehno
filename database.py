import httpx
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("DIRECTUS_URL", "http://localhost:8055")
TOKEN = os.getenv("DIRECTUS_TOKEN")

async def get_db():
    async with httpx.AsyncClient(
        base_url=URL,
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=30.0
    ) as client:
        yield client    