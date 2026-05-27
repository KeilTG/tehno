// Ждём загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
  const trigger  = document.getElementById('pp-trigger');
  const overlay  = document.getElementById('pp-overlay');
  const closeBtn = document.getElementById('pp-close-btn');

  // Проверяем что элементы существуют на странице
  if (!trigger || !overlay || !closeBtn) {
    return; // Если модалки нет на странице - выходим
  }

  function openModal() {
    overlay.classList.add('open');
    trigger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function closeModal() {
    overlay.classList.remove('open');
    trigger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    trigger.focus();
  }

  // Триггер — toggle
  trigger.addEventListener('click', function (e) {
    e.preventDefault();
    overlay.classList.contains('open') ? closeModal() : openModal();
  });

  // Кнопка ×
  closeBtn.addEventListener('click', closeModal);

  // Клик на фон
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });

  // Клавиша Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('open')) {
      closeModal();
    }
  });
});