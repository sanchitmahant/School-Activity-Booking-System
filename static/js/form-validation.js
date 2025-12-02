/**
 * Professional Form Validation & UX Enhancements
 * Client-side validation with visual feedback
 */

// Real-time Email Validation
function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

// Real-time Phone Validation
function validatePhone(phone) {
    const regex = /^[0-9+\s-]{10,15}$/;
    return regex.test(phone);
}

// Password Strength Checker
function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;

    if (strength <= 2) return { level: 'weak', color: '#dc3545', text: 'Weak' };
    if (strength <= 4) return { level: 'medium', color: '#ffc107', text: 'Medium' };
    return { level: 'strong', color: '#28a745', text: 'Strong' };
}

// Add visual feedback to input fields
function addFieldFeedback(input, isValid, message = '') {
    const feedback = input.nextElementSibling;

    if (isValid) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.style.display = 'none';
        }
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = message;
            feedback.style.display = 'block';
        }
    }
}

// Initialize form validation on page load
document.addEventListener('DOMContentLoaded', function () {

    // Email fields validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function () {
            if (this.value) {
                const isValid = validateEmail(this.value);
                addFieldFeedback(this, isValid, 'Please enter a valid email address');
            }
        });

        input.addEventListener('input', function () {
            if (this.classList.contains('is-invalid') && validateEmail(this.value)) {
                addFieldFeedback(this, true);
            }
        });
    });

    // Phone fields validation
    const phoneInputs = document.querySelectorAll('input[name="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function () {
            if (this.value) {
                const isValid = validatePhone(this.value);
                addFieldFeedback(this, isValid, 'Please enter a valid phone number (10-15 digits)');
            }
        });
    });

    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"][name="password"]');
    passwordInputs.forEach(input => {
        // Create strength indicator
        const strengthDiv = document.createElement('div');
        strengthDiv.className = 'password-strength mt-2';
        strengthDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">Password Strength:</small>
                <small class="strength-text fw-bold">-</small>
            </div>
            <div class="progress" style="height: 4px;">
                <div class="progress-bar" role="progressbar" style="width: 0%"></div>
            </div>
        `;
        input.parentNode.insertBefore(strengthDiv, input.nextSibling);

        input.addEventListener('input', function () {
            const strength = checkPasswordStrength(this.value);
            const progressBar = strengthDiv.querySelector('.progress-bar');
            const strengthText = strengthDiv.querySelector('.strength-text');

            if (this.value.length > 0) {
                const widthMap = { weak: '33%', medium: '66%', strong: '100%' };
                progressBar.style.width = widthMap[strength.level];
                progressBar.style.backgroundColor = strength.color;
                strengthText.textContent = strength.text;
                strengthText.style.color = strength.color;
                strengthDiv.style.display = 'block';
            } else {
                strengthDiv.style.display = 'none';
            }
        });
    });

    // Password confirmation matching
    const confirmInputs = document.querySelectorAll('input[name="confirm_password"]');
    confirmInputs.forEach(input => {
        input.addEventListener('input', function () {
            const password = document.querySelector('input[name="password"]').value;
            if (this.value) {
                const isValid = this.value === password;
                addFieldFeedback(this, isValid, 'Passwords do not match');
            }
        });
    });

    // Required field indicators
    const requiredInputs = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredInputs.forEach(input => {
        // Add asterisk to labels
        const label = input.previousElementSibling;
        if (label && label.tagName === 'LABEL' && !label.querySelector('.text-danger')) {
            label.innerHTML += ' <span class="text-danger">*</span>';
        }

        // Validate on blur
        input.addEventListener('blur', function () {
            if (!this.value.trim()) {
                addFieldFeedback(this, false, 'This field is required');
            } else {
                if (!this.classList.contains('is-invalid')) {
                    addFieldFeedback(this, true);
                }
            }
        });
    });

    //Form submission validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    addFieldFeedback(field, false, 'This field is required');
                    isValid = false;
                }
            });

            // Email validation
            const emailField = form.querySelector('input[type="email"]');
            if (emailField && emailField.value && !validateEmail(emailField.value)) {
                addFieldFeedback(emailField, false, 'Please enter a valid email address');
                isValid = false;
            }

            // Password match validation
            const password = form.querySelector('input[name="password"]');
            const confirmPassword = form.querySelector('input[name="confirm_password"]');
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                addFieldFeedback(confirmPassword, false, 'Passwords do not match');
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = form.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }

                // Show toast notification
                showToast('Please fix the errors in the form', 'error');
            }
        });
    });
});

// Loading spinner for forms
function showFormLoading(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    }
}

// Toast notification function
function showToast(message, type = 'info') {
    const toast = document.createElement div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} border-0 show`;
    toast.setAttribute('role', 'alert');
    toast.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

// Add to all AJAX form submissions
document.addEventListener('submit', function (e) {
    if (e.target.tagName === 'FORM' && e.target.hasAttribute('data-ajax')) {
        e.preventDefault();
        showFormLoading(e.target);
    }
});
