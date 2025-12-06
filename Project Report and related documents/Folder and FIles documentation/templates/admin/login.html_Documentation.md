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
**Path**: `templates\admin\login.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Admin Login{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center min-vh-75 align-items-center">
        <div class="col-md-5">
            <div class="glass-card p-5">
                <div class="text-center mb-4">
                    <i class="fas fa-user-shield fa-3x icon-gold mb-3"></i>
                    <h2 class="fw-bold" style="color: white;">Admin Access</h2>
                    <p class="text-light opacity-75">Restricted Area</p>
                </div>

                {% if error %}
                <div class="alert alert-danger" role="alert">
                    {{ error }}
                </div>
                {% endif %}

                <form method="POST" action="{{ url_for('admin_login') }}">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                    <div class="mb-3">
                        <label for="email" class="form-label text-light">Email Address</label>
                        <input type="email" class="form-control rounded-pill" id="email" name="email" required>
                    </div>
                    <div class="mb-4">
                        <label for="password" class="form-label text-light">Password</label>
                        <input type="password" class="form-control rounded-pill" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary-custom w-100 rounded-pill">Login</button>
                </form>

                <div class="text-center mt-4">
                    <a href="{{ url_for('index') }}" class="text-decoration-none text-light opacity-50">Return to
                        Portal</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
