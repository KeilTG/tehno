import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.yandex.ru")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")
SMTP_TO = os.getenv("SMTP_TO")

async def send_request_email(request_data: dict):
    """Отправляет заявку на email"""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_FROM
        msg["To"] = SMTP_TO
        msg["Subject"] = f"Новая заявка от {request_data.get('client_name')}"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #0a2463;">Новая заявка с сайта ТехноСервис</h2>
            <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
                <tr style="background: #f5f5f5;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Имя:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{request_data.get('client_name')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Телефон:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{request_data.get('client_phone')}</td>
                </tr>
                <tr style="background: #f5f5f5;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Email:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{request_data.get('client_email')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Сообщение:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{request_data.get('message', '—')}</td>
                </tr>
                <tr style="background: #f5f5f5;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Услуга/Товар ID:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{request_data.get('service_id', 'Не указан')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Дата:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{request_data.get('created_at') or 'Сейчас'}</td>
                </tr>
            </table>
            <p style="margin-top: 20px; color: #666; font-size: 12px;">
                Письмо сгенерировано автоматически с сайта ТехноСервис.
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Письмо отправлено на {SMTP_TO}")
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки письма: {e}")
        return False