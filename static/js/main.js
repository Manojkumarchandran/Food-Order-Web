/* ============================================
   FOODORDER - Main JavaScript
============================================ */

const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

// ---- TOAST NOTIFICATIONS ----
function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `app-toast ${type}`;
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  toast.innerHTML = `<span>${icons[type] || '🔔'}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideInRight 0.4s ease reverse';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

// ---- ADD TO CART (AJAX) ----
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-add-to-cart]');
  if (!btn) return;

  const itemId = btn.dataset.addToCart;
  btn.disabled = true;
  btn.textContent = '⌛';

  try {
    const res = await fetch(`/cart/add/${itemId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'X-Requested-With': 'XMLHttpRequest',
      }
    });

    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      updateCartBadge(data.cart_count);
      animateCartIcon();
    }
  } catch (err) {
    showToast('Failed to add item. Please try again.', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '+';
  }
});

// ---- UPDATE CART QUANTITY ----
async function updateQuantity(cartItemId, quantity) {
  try {
    const res = await fetch(`/cart/update/${cartItemId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF_TOKEN,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify({ quantity })
    });

    const data = await res.json();
    if (data.success) {
      updateCartBadge(data.cart_count);
      updateCartTotals(data);
      if (quantity <= 0) {
        document.querySelector(`[data-cart-item="${cartItemId}"]`)?.remove();
      }
    }
  } catch (err) {
    showToast('Failed to update cart.', 'error');
  }
}

// ---- REMOVE FROM CART ----
async function removeFromCart(cartItemId) {
  try {
    const res = await fetch(`/cart/remove/${cartItemId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'X-Requested-With': 'XMLHttpRequest',
      }
    });

    const data = await res.json();
    if (data.success) {
      const row = document.querySelector(`[data-cart-item="${cartItemId}"]`);
      row && (row.style.animation = 'slideInRight 0.3s reverse', setTimeout(() => row.remove(), 300));
      updateCartBadge(data.cart_count);
      updateCartTotals(data);
      showToast('Item removed from cart', 'info');
      if (data.cart_count === 0) setTimeout(() => location.reload(), 500);
    }
  } catch (err) {
    showToast('Failed to remove item.', 'error');
  }
}

// ---- CART BADGE UPDATE ----
function updateCartBadge(count) {
  document.querySelectorAll('.cart-count').forEach(el => {
    el.textContent = count;
    el.style.display = count > 0 ? 'flex' : 'none';
  });
}

function animateCartIcon() {
  const cartIcon = document.querySelector('.cart-icon-link');
  if (!cartIcon) return;
  cartIcon.classList.add('cart-bump');
  setTimeout(() => cartIcon.classList.remove('cart-bump'), 400);
}

function updateCartTotals(data) {
  const totalEl = document.querySelector('.cart-total-price');
  if (totalEl) {
    totalEl.textContent = `$${parseFloat(data.cart_total).toFixed(2)}`;
  }
  // Update order summary fields
  const subtotalEl = document.querySelector('[data-subtotal]');
  if (subtotalEl && data.cart_total) {
    subtotalEl.textContent = `$${parseFloat(data.cart_total).toFixed(2)}`;
  }
}

// ---- QUANTITY CONTROLS ON CART PAGE ----
document.addEventListener('click', (e) => {
  const increaseBtn = e.target.closest('[data-increase]');
  const decreaseBtn = e.target.closest('[data-decrease]');
  const removeBtn = e.target.closest('[data-remove-item]');

  if (increaseBtn) {
    const itemId = increaseBtn.dataset.increase;
    const qtyEl = document.querySelector(`[data-qty="${itemId}"]`);
    const newQty = parseInt(qtyEl.textContent) + 1;
    qtyEl.textContent = newQty;
    updateQuantity(itemId, newQty);
  }

  if (decreaseBtn) {
    const itemId = decreaseBtn.dataset.decrease;
    const qtyEl = document.querySelector(`[data-qty="${itemId}"]`);
    const newQty = parseInt(qtyEl.textContent) - 1;
    if (newQty <= 0) {
      removeFromCart(itemId);
    } else {
      qtyEl.textContent = newQty;
      updateQuantity(itemId, newQty);
    }
  }

  if (removeBtn) {
    const itemId = removeBtn.dataset.removeItem;
    removeFromCart(itemId);
  }
});

// ---- STAR RATING UI ----
function initStarRating() {
  const stars = document.querySelectorAll('.star-rating label');
  stars.forEach(star => {
    star.addEventListener('mouseenter', function() {
      const val = this.dataset.value;
      stars.forEach(s => {
        s.classList.toggle('hovered', parseInt(s.dataset.value) <= parseInt(val));
      });
    });
    star.addEventListener('mouseleave', () => {
      stars.forEach(s => s.classList.remove('hovered'));
    });
  });
}

// ---- HERO SEARCH ----
function initHeroSearch() {
  const heroSearchInput = document.querySelector('.hero-search input');
  const heroSearchBtn = document.querySelector('.hero-search button');

  if (heroSearchBtn) {
    heroSearchBtn.addEventListener('click', () => {
      const q = heroSearchInput.value.trim();
      if (q) window.location.href = `/menu/?q=${encodeURIComponent(q)}`;
    });
  }

  heroSearchInput?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const q = heroSearchInput.value.trim();
      if (q) window.location.href = `/menu/?q=${encodeURIComponent(q)}`;
    }
  });
}

// ---- FADE IN ELEMENTS ON SCROLL ----
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.food-card, .section-title, .category-pill').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });
}

// ---- AUTO DISMISS DJANGO MESSAGES ----
function initMessages() {
  document.querySelectorAll('.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap?.Alert?.getInstance(alert);
      bsAlert?.close() || alert.remove();
    }, 4000);
  });
}

// ---- ORDER TRACKER AUTO REFRESH ----
function initOrderTracker() {
  const tracker = document.querySelector('.order-tracker[data-order-id]');
  if (!tracker) return;

  const orderId = tracker.dataset.orderId;
  // Poll for status updates every 30 seconds
  setInterval(async () => {
    try {
      const res = await fetch(`/orders/${orderId}/`);
      // Could parse updated status from response
    } catch (err) {}
  }, 30000);
}

// ---- CHECKOUT FORM VALIDATION ----
function initCheckout() {
  const checkoutForm = document.querySelector('#checkout-form');
  if (!checkoutForm) return;

  checkoutForm.addEventListener('submit', (e) => {
    const phone = checkoutForm.querySelector('[name="phone"]');
    const address = checkoutForm.querySelector('[name="delivery_address"]');
    if (!phone.value.trim() || !address.value.trim()) {
      e.preventDefault();
      showToast('Please fill in all required fields.', 'error');
    }
  });
}

// ---- INIT ----
document.addEventListener('DOMContentLoaded', () => {
  initHeroSearch();
  initScrollAnimations();
  initMessages();
  initStarRating();
  initOrderTracker();
  initCheckout();
});
