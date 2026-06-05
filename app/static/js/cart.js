document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const overlay = document.querySelector('[data-cart-overlay]');
    if (!overlay) {
        return;
    }

    const itemsContainer = overlay.querySelector('[data-cart-items]');
    const emptyBlock = overlay.querySelector('[data-cart-empty]');
    const footer = overlay.querySelector('[data-cart-footer]');
    const totalEl = overlay.querySelector('[data-cart-total]');

    const STORAGE_KEY = 'ts_cart';

    function loadCart() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            return raw ? JSON.parse(raw) : [];
        } catch (e) {
            console.warn('Failed to load cart:', e);
            return [];
        }
    }

    function saveCart(items) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    }

    function formatPrice(value) {
        if (isNaN(value)) return '0';
        return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    }

    function getTotal(items) {
        return items.reduce((sum, item) => sum + item.price * item.qty, 0);
    }

    function getCount(items) {
        return items.reduce((sum, item) => sum + item.qty, 0);
    }

    function updateCartCounter() {
        const items = loadCart();
        const count = getCount(items);
        document.querySelectorAll('[data-cart-count]').forEach(el => {
            if (!el) return;
            if (count > 0) {
                el.textContent = count;
                el.classList.add('basket-btn__counter--visible');
            } else {
                el.textContent = '';
                el.classList.remove('basket-btn__counter--visible');
            }
        });
    }

    function renderCart() {
        const items = loadCart();
        itemsContainer.innerHTML = '';

        if (!items.length) {
            emptyBlock.style.display = 'flex';
            footer.style.display = 'none';
            totalEl.textContent = '0 ₽';
            updateCartCounter();
            return;
        }

        emptyBlock.style.display = 'none';
        footer.style.display = 'block';

        items.forEach(item => {
            const row = document.createElement('div');
            row.className = 'cart-item';
            row.dataset.id = item.id;
            row.innerHTML = `
                <div class="cart-item__image-wrapper">
                    <img src="${item.image || '/static/img/placeholder.png'}" alt="${item.title}" class="cart-item__image">
                </div>
                <div class="cart-item__main">
                    <div class="cart-item__row-top">
                        <div>
                            <div class="cart-item__title">${item.title}</div>
                            <div class="cart-item__subtitle">${item.subtitle || 'Подписка'}</div>
                        </div>
                        <button type="button" class="cart-item__remove" data-cart-remove>Удалить</button>
                    </div>
                    <div class="cart-item__row-bottom">
                        <div class="cart-item__counter">
                            <button type="button" class="cart-item__counter-btn" data-cart-dec>-</button>
                            <span class="cart-item__qty">${item.qty}</span>
                            <button type="button" class="cart-item__counter-btn" data-cart-inc>+</button>
                        </div>
                        <div class="cart-item__price">${formatPrice(item.price)} ₽/мес</div>
                    </div>
                </div>
            `;
            itemsContainer.appendChild(row);
        });

        const total = getTotal(items);
        totalEl.textContent = `${formatPrice(total)} ₽`;
        updateCartCounter();
    }

    function openCart() {
        const items = loadCart();
        if (!items.length) {
            if (window.showEmptyCartModal) {
                window.showEmptyCartModal();
            }
            return;
        }
        overlay.classList.add('cart-overlay--visible');
        body.classList.add('cart-open');
        renderCart();
    }

    function closeCart() {
        overlay.classList.remove('cart-overlay--visible');
        body.classList.remove('cart-open');
    }

    function addItemFromCard(button) {
        const card = button.closest('.catalog-card');
        if (!card) return;

        const id = card.getAttribute('data-product-id');
        const title = card.querySelector('.catalog-card__title')?.textContent.trim() || '';
        const priceText = card.querySelector('.catalog-card__price-value')?.textContent || '0';
        const imageEl = card.querySelector('.catalog-card__image');
        const image = imageEl ? imageEl.getAttribute('src') : '/static/img/placeholder.png';
        const numericPrice = parseInt(priceText.replace(/\D/g, ''), 10) || 0;

        let items = loadCart();
        const existing = items.find(it => it.id === id);
        if (existing) {
            existing.qty += 1;
        } else {
            items.push({
                id,
                title,
                price: numericPrice,
                qty: 1,
                image,
                subtitle: 'Подписка'
            });
        }
        saveCart(items);
        renderCart();
        updateCartCounter();
        return items;
    }

    window.TechnoServiceCart = {
        addFromCard: addItemFromCard,
        openCart: openCart,
        updateCounter: updateCartCounter
    };

    document.querySelectorAll('[data-cart-open]').forEach(btn => {
        btn.addEventListener('click', function () {
            openCart();
        });
    });
    
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay || e.target.closest('[data-cart-close]')) {
            closeCart();
        }
    });

    const catalogUrl = body.dataset.catalogUrl;
    const orderUrl = body.dataset.orderUrl;
    const goCatalogBtn = overlay.querySelector('[data-cart-go-catalog]');
    if (goCatalogBtn && catalogUrl) {
        goCatalogBtn.addEventListener('click', function () {
            window.location.href = catalogUrl;
        });
    }

    const checkoutBtn = overlay.querySelector('[data-cart-checkout]');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function () {
            const items = loadCart();
            if (!items.length) return;
            window.location.href = '/contacts.html#audit-form';
        });
    }

    itemsContainer.addEventListener('click', function (e) {
        const row = e.target.closest('.cart-item');
        if (!row) return;
        const id = row.dataset.id;
        let items = loadCart();
        const item = items.find(it => it.id === id);
        if (!item) return;

        if (e.target.matches('[data-cart-remove]')) {
            items = items.filter(it => it.id !== id);
        } else if (e.target.matches('[data-cart-inc]')) {
            item.qty += 1;
        } else if (e.target.matches('[data-cart-dec]')) {
            item.qty -= 1;
            if (item.qty <= 0) {
                items = items.filter(it => it.id !== id);
            }
        } else {
            return;
        }

        saveCart(items);
        renderCart();
        updateCartCounter();
    });

    document.addEventListener('click', function (e) {
        const button = e.target.closest('.catalog-card__button');
        if (!button) return;
        addItemFromCard(button);
    });

    updateCartCounter();
});