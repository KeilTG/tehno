// Инициализация общих скриптов сайта
document.addEventListener('DOMContentLoaded', function() {
    // Swiper на главной
    const swiperContainer = document.querySelector('.directions-swiper');
    if (swiperContainer) {
        // eslint-disable-next-line no-undef
        const directionsSwiper = new Swiper(swiperContainer, {
            autoplay: {
                delay: 10000,
                disableOnInteraction: false,
            },
            loop: true,
            effect: 'slide',
            speed: 800,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            breakpoints: {
                320: {
                    slidesPerView: 1,
                    spaceBetween: 20
                },
                768: {
                    slidesPerView: 1,
                    spaceBetween: 30
                },
                992: {
                    slidesPerView: 1,
                    spaceBetween: 40
                }
            }
        });
    }

    // Мобильное бургер-меню
    const burgerBtn = document.querySelector('.burger-btn');
    const mobileOverlay = document.querySelector('[data-mobile-menu-overlay]');

    if (burgerBtn && mobileOverlay) {
        const closeBtn = mobileOverlay.querySelector('[data-mobile-menu-close]');
        const links = mobileOverlay.querySelectorAll('a');

        function openMenu() {
            mobileOverlay.classList.add('mobile-menu-overlay--visible');
            document.body.classList.add('mobile-menu-open');
        }

        function closeMenu() {
            mobileOverlay.classList.remove('mobile-menu-overlay--visible');
            document.body.classList.remove('mobile-menu-open');
        }

        burgerBtn.addEventListener('click', openMenu);

        mobileOverlay.addEventListener('click', function (e) {
            if (e.target === mobileOverlay) {
                closeMenu();
            }
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', closeMenu);
        }

        links.forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }
});