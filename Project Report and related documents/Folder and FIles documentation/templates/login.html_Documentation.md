# HTML Template: login.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\login.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Login - School Activity Booking{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow-lg border-0">
                <div class="card-body p-5">
                    <h2 class="card-title mb-4 text-center text-primary">Parent Login</h2>

                    {% if error %}
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        {{ error }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    {% endif %}

                    <form method="POST" action="{{ url_for('login') }}">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />

                        <div class="mb-3">
                            <label for="email" class="form-label">Email address</label>
                            <input type="email" class="form-control form-control-lg" id="email" name="email" required>
                        </div>

                        <div class="mb-4">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control form-control-lg" id="password" name="password"
                                required>
                            <div class="text-end mt-2">
                                <a href="{{ url_for('forgot_password') }}" class="text-decoration-none small">Forgot
                                    Password?</a>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary-custom btn-lg w-100 mb-3">Login</button>
                    </form>

                    <p class="text-center text-muted">
                        Don't have an account? <a href="/register" class="text-decoration-none">Register here</a>
                    </p>

                    <hr class="my-4">
                    <div class="text-center">
                        <a href="/admin/login" class="text-secondary small me-3">Admin Login</a>
                        <a href="/tutor/login" class="text-secondary small">Tutor Login</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
