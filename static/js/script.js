/**
 * School Activity Booking System - JavaScript
 * Client-side interactivity and validation
 */

// Utility Functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main') || document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    // Validate registration form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password.length < 8) {
                e.preventDefault();
                showAlert('Password must be at least 8 characters', 'warning');
                return false;
            }
            
            if (password !== confirmPassword) {
                e.preventDefault();
                showAlert('Passwords do not match', 'warning');
                return false;
            }
        });
    }

    // Initialize date pickers with minimum date as today
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        input.setAttribute('min', today);
    });

    // Add Bootstrap validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Debounce function for search/filter operations
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Loading spinner
function showSpinner(element, show = true) {
    if (show) {
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        element.disabled = true;
    } else {
        element.disabled = false;
    }
}

// API Helper Functions
async function fetchJSON(url, options = {}) {
    try {
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            ...options.headers
        };

        const response = await fetch(url, {
            ...options,
            headers
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
        throw error;
    }
}

// Booking Management
async function bookActivityAsync(activityId) {
    const childId = document.getElementById('bookingChild').value;
    const bookingDate = document.getElementById('bookingDate').value;

    if (!childId) {
        showAlert('Please select a child', 'warning');
        return;
    }

    if (!bookingDate) {
        showAlert('Please select a date', 'warning');
        return;
    }

    try {
        const formData = new FormData();
        formData.append('child_id', childId);
        formData.append('activity_id', activityId);
        formData.append('booking_date', bookingDate);

        const response = await fetch('/book_activity', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });

        const data = await response.json();

        if (data.success) {
            showAlert(data.message, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Error: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('Error booking activity', 'danger');
    }
}

async function cancelBookingAsync(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/cancel_booking/' + bookingId, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });

        const data = await response.json();

        if (data.success) {
            showAlert(data.message, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Error: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('Error cancelling booking', 'danger');
    }
}

async function addChildAsync() {
    const form = document.getElementById('addChildForm');
    const formData = new FormData(form);
    const name = formData.get('name');

    if (!name || name.trim() === '') {
        showAlert('Child name is required', 'warning');
        return;
    }

    try {
        const response = await fetch('/add_child', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });

        const data = await response.json();

        if (data.id) {
            showAlert('Child added successfully!', 'success');
            form.reset();
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Error: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('Error adding child', 'danger');
    }
}

// Activity Availability Checker
async function checkActivityAvailability(activityId, bookingDate) {
    try {
        const data = await fetchJSON('/api/check_availability', {
            method: 'POST',
            body: JSON.stringify({
                activity_id: activityId,
                booking_date: bookingDate
            })
        });

        if (data.available) {
            showAlert(`${data.spots_left} spots available`, 'success');
        } else {
            showAlert('This activity is fully booked for the selected date', 'warning');
        }

        return data.available;
    } catch (error) {
        return false;
    }
}

// Table sorting
function sortTable(table, column, order = 'asc') {
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    
    rows.sort((a, b) => {
        const aValue = a.cells[column].textContent;
        const bValue = b.cells[column].textContent;
        
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return order === 'asc' 
                ? parseFloat(aValue) - parseFloat(bValue)
                : parseFloat(bValue) - parseFloat(aValue);
        }
        
        return order === 'asc'
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });

    const tbody = table.querySelector('tbody');
    rows.forEach(row => tbody.appendChild(row));
}

// Local Storage helpers (for saving preferences)
function savePreference(key, value) {
    try {
        localStorage.setItem(`booking_system_${key}`, JSON.stringify(value));
    } catch (error) {
        console.warn('Could not save preference:', error);
    }
}

function getPreference(key, defaultValue = null) {
    try {
        const value = localStorage.getItem(`booking_system_${key}`);
        return value ? JSON.parse(value) : defaultValue;
    } catch (error) {
        console.warn('Could not retrieve preference:', error);
        return defaultValue;
    }
}

// Export functions for use in HTML
window.bookActivity = bookActivityAsync;
window.cancelBooking = cancelBookingAsync;
window.addChild = addChildAsync;
window.checkAvailability = checkActivityAvailability;
