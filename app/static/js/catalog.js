document.addEventListener('DOMContentLoaded', function() {
    const catalogSection = document.querySelector('.catalog-section');
    if (!catalogSection) {
        return;
    }

    const addToCartButtons = document.querySelectorAll('.catalog-card__button');
    if (addToCartButtons.length) {
        addToCartButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                if (window.TechnoServiceCart && window.TechnoServiceCart.addFromCard) {
                    window.TechnoServiceCart.addFromCard(this);
                    window.TechnoServiceCart.openCart();
                }
                
                const textSpan = this.querySelector('.catalog-card__button-text');
                if (textSpan) {
                    const originalText = textSpan.textContent;
                    textSpan.textContent = 'Добавлено!';
                    this.style.background = '#00c950';
                    setTimeout(() => {
                        textSpan.textContent = originalText;
                        this.style.background = '#00c2d2';
                    }, 2000);
                }
            });
        });
    }

    const body = document.body;
    const modalOverlays = document.querySelectorAll('.catalog-modal-overlay');

    function openModalById(productId) {
        const modal = document.querySelector(`.catalog-modal-overlay[data-modal-id="${productId}"]`);
        if (!modal) return;
        modal.classList.add('catalog-modal-overlay--visible');
        body.classList.add('catalog-modal-open');
    }

    function closeModal(modal) {
        modal.classList.remove('catalog-modal-overlay--visible');
        const anyOpen = document.querySelector('.catalog-modal-overlay.catalog-modal-overlay--visible');
        if (!anyOpen) {
            body.classList.remove('catalog-modal-open');
        }
    }

    const catalogCards = document.querySelectorAll('.catalog-card');
    catalogCards.forEach(card => {
        card.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            if (!productId) return;
            openModalById(productId);
        });
    });

    modalOverlays.forEach(overlay => {
        const addBtn = overlay.querySelector('.catalog-modal__btn-primary');
        if (addBtn) {
            addBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const modalId = overlay.getAttribute('data-modal-id');
                const card = document.querySelector(`.catalog-card[data-product-id="${modalId}"]`);
                if (card && window.TechnoServiceCart && window.TechnoServiceCart.addFromCard) {
                    const cardButton = card.querySelector('.catalog-card__button');
                    if (cardButton) {
                        window.TechnoServiceCart.addFromCard(cardButton);
                        window.TechnoServiceCart.openCart();
                        closeModal(overlay);
                    }
                }
            });
        }
    });

    modalOverlays.forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closeModal(overlay);
            }
        });

        const closeButtons = overlay.querySelectorAll('[data-modal-close]');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                closeModal(overlay);
            });
        });
    });

    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        const catalogCardsGsap = document.querySelectorAll('.catalog-card');
        catalogCardsGsap.forEach((card, index) => {
            gsap.fromTo(card, 
                { opacity: 0, y: 30 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.6,
                    delay: index * 0.1,
                    scrollTrigger: {
                        trigger: card,
                        start: 'top 85%',
                        toggleActions: 'play none none none'
                    }
                }
            );
        });
    }
});