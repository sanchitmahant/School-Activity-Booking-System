# HTML Template: reset_password.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\reset_password.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Reset Password - Greenwood International{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card shadow-lg border-0">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <div class="rounded-circle bg-light d-inline-flex align-items-center justify-content-center mb-3"
                            style="width: 60px; height: 60px;">
                            <i class="fas fa-key text-primary fa-2x"></i>
                        </div>
                        <h3 class="card-title fw-bold text-primary">Reset Password</h3>
                        <p class="text-muted small">Please enter your new password below.</p>
                    </div>

                    {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                    {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    {% endfor %}
                    {% endif %}
                    {% endwith %}

                    <form method="POST">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />

                        <div class="mb-3">
                            <label for="password" class="form-label fw-bold text-primary">New Password</label>
                            <div class="input-group">
                                <span class="input-group-text bg-light border-end-0"><i
                                        class="fas fa-lock text-muted"></i></span>
                                <input type="password" class="form-control form-control-lg border-start-0 ps-0"
                                    id="password" name="password" required>
                            </div>
                        </div>

                        <div class="mb-4">
                            <label for="confirm_password" class="form-label fw-bold text-primary">Confirm
                                Password</label>
                            <div class="input-group">
                                <span class="input-group-text bg-light border-end-0"><i
                                        class="fas fa-lock text-muted"></i></span>
                                <input type="password" class="form-control form-control-lg border-start-0 ps-0"
                                    id="confirm_password" name="confirm_password" required>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary-custom btn-lg w-100 mb-3">Reset Password</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
