import { api } from './api.js';

document.addEventListener('DOMContentLoaded', async function () {
    const contactsSection = document.querySelector('.contacts-main');
    if (contactsSection) {
        console.log('Страница "Контакты" загружена');
    }

    // Загрузка контактов из Directus
    const contactsContainer = document.getElementById('contacts-container');
    if (contactsContainer) {
        try {
            const contacts = await api.getContacts();
            
            if (!contacts.length) {
                contactsContainer.innerHTML = '<p>Контакты не найдены</p>';
                return;
            }

            let phone = '', email = '', address = '';
            
            contacts.forEach(contact => {
                if (contact.contact_type === 'phone') {
                    phone = contact.contact_value;
                } else if (contact.contact_type === 'email') {
                    email = contact.contact_value;
                } else if (contact.contact_type === 'address') {
                    address = contact.contact_value;
                }
            });

            contactsContainer.innerHTML = `
                <article class="contacts-card card-hover">
                    <div class="contacts-card__icon"><img src="/static/img/svg/contact-1.svg" alt="Телефон"></div>
                    <h2 class="contacts-card__title">Телефон</h2>
                    <p class="contacts-card__value">${phone || 'Не указан'}</p>
                    <p class="contacts-card__note">Звоните в любое время</p>
                </article>
                <article class="contacts-card card-hover">
                    <div class="contacts-card__icon"><img src="/static/img/svg/contact-2.svg" alt="Email"></div>
                    <h2 class="contacts-card__title">Email</h2>
                    <p class="contacts-card__value">${email || 'Не указан'}</p>
                    <p class="contacts-card__note">Ответим в течение часа</p>
                </article>
                <article class="contacts-card card-hover">
                    <div class="contacts-card__icon"><img src="/static/img/svg/contact-3.svg" alt="Адрес"></div>
                    <h2 class="contacts-card__title">Адрес</h2>
                    <p class="contacts-card__value">${address || 'Не указан'}</p>
                    <p class="contacts-card__note">Пн–Пт: 9:00 – 18:00</p>
                </article>
            `;
        } catch (err) {
            console.error('Ошибка загрузки контактов:', err);
            contactsContainer.innerHTML = '<p>Ошибка загрузки контактов</p>';
        }
    }

    // Обработка формы бесплатного аудита
    const auditForm = document.getElementById('audit-form-element');
    if (auditForm) {
        auditForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(auditForm);
            const data = {
                client_name: formData.get('client_name'),
                client_phone: formData.get('client_phone'),
                client_email: formData.get('client_email'),
                message: `Компания: ${formData.get('company') || ''}\nУслуга: ${formData.get('service') || ''}\nСообщение: ${formData.get('message') || ''}`
            };
            
            try {
                const result = await api.sendRequest(data);
                const msgDiv = document.getElementById('form-message');
                if (msgDiv) {
                    msgDiv.style.display = 'block';
                    msgDiv.textContent = result.message || 'Заявка отправлена!';
                    setTimeout(() => {
                        msgDiv.style.display = 'none';
                    }, 5000);
                }
                auditForm.reset();
            } catch (err) {
                alert('Ошибка при отправке: ' + err.message);
            }
        });
    }

    // Для страницы оформления заказа
    const orderItemsInput = document.querySelector('[data-order-cart-items]');
    if (orderItemsInput) {
        try {
            const raw = localStorage.getItem('ts_cart');
            orderItemsInput.value = raw || '[]';
        } catch (e) {
            orderItemsInput.value = '[]';
        }
    }
});