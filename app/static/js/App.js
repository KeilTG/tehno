// ----------- Пример работы с апи -----------

import React, { useEffect, useState } from 'react';
import { api } from './api';

function App() {
    const [services, setServices] = useState([]);
    const [contacts, setContacts] = useState([]);

    useEffect(() => {
        // Загружаем услуги
        api.getServices().then(setServices);
        // Загружаем контакты
        api.getContacts().then(setContacts);
    }, []);

    return (
        <div>
            <h1>Услуги</h1>
            {services.map(service => (
                <div key={service.id}>
                    <h3>{service.name}</h3>
                    <p>{service.description}</p>
                </div>
            ))}
            
            <h2>Контакты</h2>
            {contacts.map(contact => (
                <div key={contact.id}>
                    {contact.contact_type}: {contact.contact_value}
                </div>
            ))}
        </div>
    );
}

export default App;