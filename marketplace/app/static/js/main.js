// ===== Navigation Toggle =====
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!navToggle.contains(event.target) && !navMenu.contains(event.target)) {
                navMenu.classList.remove('active');
            }
        });
    }

    // Mobile dropdown toggle
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                this.closest('.nav-dropdown').classList.toggle('active');
            }
        });
    });
});

// ===== Auto-dismiss alerts =====
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// ===== Cart Quantity Update =====
function updateCartQuantity(itemId, change) {
    const input = document.querySelector(`#qty-${itemId}`);
    if (!input) return;

    let newQty = parseInt(input.value) + change;
    if (newQty < 1) newQty = 1;

    const maxQty = parseInt(input.getAttribute('max'));
    if (maxQty && newQty > maxQty) newQty = maxQty;

    input.value = newQty;
    document.getElementById(`update-form-${itemId}`).submit();
}

// ===== Image Gallery =====
function changeMainImage(src) {
    const mainImage = document.getElementById('mainProductImage');
    if (mainImage) {
        mainImage.src = src;
    }
    // Update active thumbnail
    document.querySelectorAll('.product-thumb').forEach(thumb => {
        thumb.classList.remove('active');
        if (thumb.querySelector('img').src === src) {
            thumb.classList.add('active');
        }
    });
}

// ===== Become Seller =====
function becomeSeller(event) {
    if (event) event.preventDefault();
    const form = document.getElementById('becomeSellerForm');
    if (form) {
        // Check if user is logged in
        fetch('/auth/profile', { method: 'HEAD' })
            .then(response => {
                if (response.ok) {
                    form.submit();
                } else {
                    window.location.href = '/auth/login?next=/auth/become-seller';
                }
            })
            .catch(() => {
                window.location.href = '/auth/login';
            });
    }
}

// ===== Add to Cart =====
function addToCart(productId, quantity) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/cart/add/${productId}`;

    if (quantity) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'quantity';
        input.value = quantity;
        form.appendChild(input);
    }

    document.body.appendChild(form);
    form.submit();
}

// ===== Search Form Submission =====
function submitSearch() {
    document.getElementById('searchForm').submit();
}

// ===== Price Range Formatter =====
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

// ===== Preview Image Before Upload =====
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// ===== Confirm Delete =====
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item? This action cannot be undone.');
}

