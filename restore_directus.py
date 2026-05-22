import httpx
import json
import asyncio

TOKEN = "ISaWn1dBdoQ2OxTw7u-VWAc76OQ0ZLjP"
URL = "http://127.0.0.1:8055"

async def restore():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    async with httpx.AsyncClient(timeout=10) as client:
        # Проверка подключения
        resp = await client.get(f"{URL}/server/info", headers=headers)
        if resp.status_code != 200:
            print(f"Directus unavailable: {resp.status_code}")
            print(f"Error: {resp.text}")
            return
        print("Connected to Directus")
        
        # Загружаем схему
        with open("directus_schema.json", "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        for col in schema.get("collections", []):
            name = col["collection"]
            check = await client.get(f"{URL}/collections/{name}", headers=headers)
            
            if check.status_code == 404:
                # Создаём коллекцию
                create_data = {"collection": name}
                await client.post(f"{URL}/collections", headers=headers, json=create_data)
                print(f"Created collection: {name}")
                
                # Создаём поля
                for field in col.get("fields", []):
                    if field["field"] != "id":
                        await client.post(f"{URL}/fields/{name}", headers=headers, json=field)
                        print(f"  Added field: {field['field']}")
            else:
                print(f"Collection already exists: {name}")

asyncio.run(restore())