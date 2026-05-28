from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 1. Контент страниц
class ContentPage(BaseModel):
    id: Optional[int] = None
    page_name: str
    title: str
    content: str
    created_at: Optional[datetime] = None

# 2. Баннеры
class Banner(BaseModel):
    id: Optional[int] = None
    page_id: int
    image_url: str
    title: Optional[str] = None
    link: Optional[str] = None
    position: Optional[int] = 0
    is_active: Optional[bool] = True

# 3. Категории каталога (НОВЫЕ, вместо ServiceCategories)
class CatalogCategory(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    position: Optional[int] = 0

# 4. Каталог товаров/услуг (НОВЫЙ)
class CatalogItem(BaseModel):
    id: Optional[int] = None
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    position: Optional[int] = 0

# 5. Услуги (старые, если нужны)
class Service(BaseModel):
    id: Optional[int] = None
    category_id: int
    name: str                           
    description: Optional[str] = None   
    icon: Optional[str] = None          
    image_url: Optional[str] = None    
    price: Optional[float] = None       
    position: Optional[int] = 0  

# 6. Цены (можно удалить или оставить)
class Price(BaseModel):
    id: Optional[int] = None
    service_id: int
    price_name: str
    amount: float
    currency: Optional[str] = "RUB"
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

# 7. Контакты
class Contact(BaseModel):
    id: Optional[int] = None
    contact_type: str
    contact_value: str
    label: Optional[str] = None
    sort_order: Optional[int] = 0

# 8. SEO
class SEO(BaseModel):
    id: Optional[int] = None
    page_id: int
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    url_slug: str

# 9. Заявки
class Request(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    service_id: Optional[int] = None
    client_name: str
    client_phone: str
    client_email: str
    message: Optional[str] = None
    status: Optional[str] = "new"
    created_at: Optional[datetime] = None

# 10. Роли
class Role(BaseModel):
    id: Optional[int] = None
    role_name: str

# 11. Пользователи
class User(BaseModel):
    id: Optional[int] = None
    role_id: int
    username: str
    email: str
    password_hash: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None

# 13. О компании
class AboutContent(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None  
    image_url: Optional[str] = None
    updated_at: Optional[datetime] = None
# 14. Кейсы
class Case(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    position: Optional[int] = 0
# 15. Политика конфиденциальности
class PrivacyPolicy(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    updated_at: Optional[datetime] = None