from fastapi import FastAPI, Depends, HTTPException, status, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import httpx
import json
from pathlib import Path
import os
from contextlib import asynccontextmanager

from database import get_db
from models import (
    ContentPage, Banner, CatalogCategory, CatalogItem, Service,
    Contact, Request as RequestModel
)
from email_service import send_request_email   # только один раз

# ============ LIFESPAN ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Запуск приложения...")
    await auto_restore_schema()
    yield
    print("👋 Остановка приложения...")

# ============ СОЗДАНИЕ ПРИЛОЖЕНИЯ ============
app = FastAPI(title="TechNo API", version="1.0.0", lifespan=lifespan)

# ============ CORS (добавлены реальные адреса сервера) ============
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8888",
        "http://5.42.113.201:8888",
        "http://5.42.113.201"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ СТАТИКА ============
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ============ ШАБЛОНЫ ============
templates = Jinja2Templates(directory="app/templates")

# ============ ФИЛЬТР ДЛЯ JSON ============
def from_json(value):
    try:
        return json.loads(value) if value else []
    except:
        return []

templates.env.filters['from_json'] = from_json

# ============ ФРОНТЕНД (все страницы) ============
@app.get("/", response_class=HTMLResponse)
async def index(request: FastAPIRequest):
    return templates.TemplateResponse("app/index.html", {"request": request})

@app.get("/services.html", response_class=HTMLResponse)
async def services_page(request: FastAPIRequest, client: httpx.AsyncClient = Depends(get_db)):
    try:
        resp_services = await client.get("/items/services", params={"sort": "position"})
        if resp_services.status_code == 200:
            services = resp_services.json().get("data", [])
            print(f"✅ Получено {len(services)} услуг из Directus")
        else:
            services = []
            print(f"❌ Ошибка получения услуг: {resp_services.status_code}")
        return templates.TemplateResponse("app/services.html", {"request": request, "services": services})
    except Exception as e:
        print(f"❌ Исключение в services_page: {e}")
        return templates.TemplateResponse("app/services.html", {"request": request, "services": []})

@app.get("/catalog.html", response_class=HTMLResponse)
async def catalog_page(request: FastAPIRequest, client: httpx.AsyncClient = Depends(get_db)):
    try:
        resp_items = await client.get("/items/catalog_items", params={
            "filter": '{"category_id": {"_eq": 1}}',
            "sort": "position"
        })
        if resp_items.status_code == 200:
            catalog_items = resp_items.json().get("data", [])
            print(f"✅ Получено {len(catalog_items)} товаров для Подписок")
        else:
            catalog_items = []
            print(f"❌ Ошибка получения товаров: {resp_items.status_code}")
        return templates.TemplateResponse("app/catalog.html", {"request": request, "catalog_items": catalog_items})
    except Exception as e:
        print(f"❌ Ошибка в catalog_page: {e}")
        return templates.TemplateResponse("app/catalog.html", {"request": request, "catalog_items": []})

@app.get("/catalog_printers.html", response_class=HTMLResponse)
async def catalog_printers_page(request: FastAPIRequest, client: httpx.AsyncClient = Depends(get_db)):
    try:
        resp_items = await client.get("/items/catalog_items", params={
            "filter": '{"category_id": {"_eq": 2}}',
            "sort": "position"
        })
        if resp_items.status_code == 200:
            catalog_items = resp_items.json().get("data", [])
            print(f"✅ Получено {len(catalog_items)} товаров для Принтеров")
        else:
            catalog_items = []
            print(f"❌ Ошибка получения товаров: {resp_items.status_code}")
        return templates.TemplateResponse("app/catalog_printers.html", {"request": request, "catalog_items": catalog_items})
    except Exception as e:
        print(f"❌ Ошибка в catalog_printers_page: {e}")
        return templates.TemplateResponse("app/catalog_printers.html", {"request": request, "catalog_items": []})

@app.get("/about.html", response_class=HTMLResponse)
async def about_page(request: FastAPIRequest, client: httpx.AsyncClient = Depends(get_db)):
    try:
        resp = await client.get("/items/about_content", params={"limit": 1})
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("data", [])
            about = items[0] if items else {}
            print(f"✅ Получен контент о компании")
        else:
            about = {}
            print(f"❌ Ошибка: {resp.status_code}")
        return templates.TemplateResponse("app/about.html", {"request": request, "about": about})
    except Exception as e:
        print(f"❌ Ошибка в about_page: {e}")
        return templates.TemplateResponse("app/about.html", {"request": request, "about": {}})

@app.get("/cases.html", response_class=HTMLResponse)
async def cases_page(request: FastAPIRequest, client: httpx.AsyncClient = Depends(get_db)):
    try:
        resp = await client.get("/items/cases", params={"sort": "position"})
        if resp.status_code == 200:
            cases = resp.json().get("data", [])
            print(f"✅ Получено {len(cases)} кейсов")
        else:
            cases = []
        return templates.TemplateResponse("app/cases.html", {"request": request, "cases": cases})
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return templates.TemplateResponse("app/cases.html", {"request": request, "cases": []})

@app.get("/contacts.html", response_class=HTMLResponse)
async def contacts_page(request: FastAPIRequest):
    return templates.TemplateResponse("app/contacts.html", {"request": request})

@app.get("/order.html", response_class=HTMLResponse)
async def order_page(request: FastAPIRequest):
    return templates.TemplateResponse("app/order.html", {"request": request})

# ============ ТЕСТОВЫЙ ЭНДПОИНТ ============
@app.get("/test-directus")
async def test_directus(client: httpx.AsyncClient = Depends(get_db)):
    try:
        info_resp = await client.get("/server/info")
        return {"directus_available": info_resp.status_code == 200}
    except Exception as e:
        return {"error": str(e)}

# ============ АВТО-СОЗДАНИЕ СХЕМЫ ============
async def auto_restore_schema():
    schema_path = Path("directus_schema.json")
    if not schema_path.exists():
        print("⚠️ directus_schema.json not found")
        return
    try:
        async for client in get_db():
            try:
                resp = await client.get("/server/info", timeout=5.0)
                if resp.status_code != 200:
                    print(f"❌ Directus unavailable: {resp.status_code}")
                    return
                print("✅ Directus доступен, проверяем схему...")
                resp = await client.get("/collections", timeout=5.0)
                if resp.status_code != 200:
                    print("❌ Не удалось получить список коллекций")
                    return
                existing_collections = [c["collection"] for c in resp.json().get("data", [])]
                with open(schema_path, "r", encoding="utf-8") as f:
                    schema_data = json.load(f)
                for collection_info in schema_data.get("collections", []):
                    collection_name = collection_info["collection"]
                    if collection_name not in existing_collections:
                        print(f"🔄 Создаю коллекцию: {collection_name}")
                        create_data = {
                            "collection": collection_name,
                            "schema": collection_info.get("schema", {})
                        }
                        await client.post("/collections", json=create_data)
                        for field in collection_info.get("fields", []):
                            if field["field"] != "id":
                                await client.post(f"/fields/{collection_name}", json=field)
                        print(f"   ✅ Коллекция {collection_name} создана")
                    else:
                        print(f"📁 Коллекция уже существует: {collection_name}")
                return
            except httpx.TimeoutException:
                print("⚠️ Таймаут подключения к Directus (5 сек)")
                return
            except httpx.ConnectError:
                print("⚠️ Не удалось подключиться к Directus (ошибка соединения)")
                return
            except Exception as e:
                print(f"⚠️ Ошибка при проверке схемы: {e}")
                return
    except Exception as e:
        print(f"⚠️ Критическая ошибка: {e}")
        return

# ============ API ЭНДПОИНТЫ ============
@app.get("/api/content-pages", response_model=List[ContentPage])
async def get_content_pages(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/content_pages")
    data = response.json()
    return data.get("data", [])

@app.get("/api/content-pages/{page_id}", response_model=ContentPage)
async def get_content_page(page_id: int, client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get(f"/items/content_pages/{page_id}")
    data = response.json()
    if not data.get("data"):
        raise HTTPException(status_code=404, detail="Page not found")
    return data["data"]

@app.get("/api/banners", response_model=List[Banner])
async def get_banners(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/banners", params={
        "filter": '{"is_active": {"_eq": true}}',
        "sort": "position"
    })
    data = response.json()
    return data.get("data", [])

@app.post("/api/banners", status_code=status.HTTP_201_CREATED)
async def create_banner(banner: Banner, client: httpx.AsyncClient = Depends(get_db)):
    response = await client.post("/items/banners", json=banner.dict(exclude_unset=True))
    data = response.json()
    return data.get("data")

@app.get("/api/services", response_model=List[Service])
async def get_services(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/services")
    data = response.json()
    return data.get("data", [])

@app.get("/api/services/{service_id}", response_model=Service)
async def get_service(service_id: int, client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get(f"/items/services/{service_id}")
    data = response.json()
    if not data.get("data"):
        raise HTTPException(status_code=404, detail="Service not found")
    return data["data"]

@app.get("/api/contacts", response_model=List[Contact])
async def get_contacts(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/contacts", params={"sort": "sort_order"})
    data = response.json()
    return data.get("data", [])

@app.get("/api/seo/{page_id}")
async def get_seo(page_id: int, client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/seo", params={
        "filter": f'{{"page_id": {{"_eq": {page_id}}}}}',
        "limit": 1
    })
    data = response.json()
    if data.get("data"):
        return data["data"][0]
    return None

@app.post("/api/requests", status_code=status.HTTP_201_CREATED)
async def create_request(request_data: RequestModel, client: httpx.AsyncClient = Depends(get_db)):
    print("📬 Получена заявка:", request_data.dict())
    # Сохраняем в Directus
    response = await client.post("/items/requests", json=request_data.dict(exclude_unset=True))
    data = response.json()
    print("💾 Сохранено в Directus, id =", data.get("data", {}).get("id"))
    # Отправляем email
    email_result = await send_request_email(request_data.dict())
    print("📧 Результат отправки email:", email_result)
    return {"message": "Заявка отправлена", "id": data.get("data", {}).get("id")}

@app.get("/api/requests", response_model=List[RequestModel])
async def get_requests(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/requests", params={"sort": "-created_at"})
    data = response.json()
    return data.get("data", [])

# API КАТАЛОГА
@app.get("/api/catalog-categories", response_model=List[CatalogCategory])
async def get_catalog_categories(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/catalog_categories", params={"sort": "position"})
    data = response.json()
    return data.get("data", [])

@app.get("/api/privacy-policy", response_model=PrivacyPolicy)
async def get_privacy_policy(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/privacy_policy", params={"limit": 1, "sort": "-updated_at"})
    data = response.json()
    items = data.get("data", [])
    if items:
        return items[0]
    return {
        "title": "Политика конфиденциальности",
        "content": "<p>Текст политики конфиденциальности...</p>"
    }

@app.get("/api/catalog-items", response_model=List[CatalogItem])
async def get_catalog_items(client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/catalog_items", params={"sort": "position"})
    data = response.json()
    return data.get("data", [])

@app.get("/api/catalog-items/by-category/{category_id}", response_model=List[CatalogItem])
async def get_catalog_items_by_category(category_id: int, client: httpx.AsyncClient = Depends(get_db)):
    response = await client.get("/items/catalog_items", params={
        "filter": f'{{"category_id": {{"_eq": {category_id}}}}}',
        "sort": "position"
    })
    data = response.json()
    return data.get("data", [])

@app.get("/api/prices")
async def get_prices_empty():
    return {"data": []}

# ============ СОГЛАСИЕ НА ОБРАБОТКУ ДАННЫХ ============
@app.get("/api/consent-text")
async def get_consent_text(client: httpx.AsyncClient = Depends(get_db)):
    try:
        response = await client.get("/items/consent_text", params={"limit": 1, "sort": "-updated_at"})
        if response.status_code == 200:
            data = response.json()
            items = data.get("data", [])
            if items:
                return items[0]
        return {
            "title": "Согласие на обработку персональных данных",
            "content": "<p>Я даю согласие на обработку моих персональных данных: ФИО, телефон, email. Данные используются только для связи со мной и не передаются третьим лицам.</p>",
            "checkbox_text": "Я даю согласие на обработку <a href='#' class='consent-link' onclick='openConsentModal(); return false;'>персональных данных</a>"
        }
    except Exception as e:
        print(f"Ошибка: {e}")
        return {
            "title": "Согласие на обработку персональных данных",
            "content": "<p>Не удалось загрузить текст</p>",
            "checkbox_text": "Я даю согласие на обработку <a href='#' class='consent-link' onclick='openConsentModal(); return false;'>персональных данных</a>"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
