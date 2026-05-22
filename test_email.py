import asyncio
from email_service import send_request_email

async def test():
    test_data = {
        "client_name": "Тест Тестович",
        "client_phone": "+7 (999) 123-45-67",
        "client_email": "test@example.com",
        "message": "Тестовое сообщение для проверки почты",
        "service_id": 1
    }
    
    result = await send_request_email(test_data)
    print("✅ Письмо отправлено!" if result else "❌ Ошибка отправки")

asyncio.run(test())