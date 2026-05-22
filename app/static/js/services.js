setTimeout(function() {
    fetch('/api/prices')
        .then(response => response.json())
        .then(data => {
            const containers = document.querySelectorAll('.price-container');
            containers.forEach(container => {
                const serviceId = parseInt(container.getAttribute('data-service-id'));
                const prices = data.filter(p => p.service_id === serviceId);
                if (prices.length) {
                    container.innerHTML = prices.map(p => `
                        <div class="price-item">
                            <span class="price-name">${p.price_name}</span>
                            <span class="price-amount">${p.amount.toLocaleString('ru-RU')} ${p.currency}</span>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = '<div class="price-placeholder">Цена по запросу</div>';
                }
            });
        })
        .catch(err => console.error('Ошибка загрузки цен:', err));
}, 100);