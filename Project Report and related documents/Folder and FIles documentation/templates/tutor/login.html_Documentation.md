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
**Path**: `templates\tutor\login.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Tutor Login{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card shadow-lg border-0">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="fas fa-chalkboard-teacher fa-3x text-secondary mb-3"></i>
                        <h2 class="card-title text-primary">Tutor Portal</h2>
                        <p class="text-muted">Access your class rosters and attendance</p>
                    </div>

                    {% if error %}
                    <div class="alert alert-danger" role="alert">
                        {{ error }}
                    </div>
                    {% endif %}

                    <form method="POST" action="{{ url_for('tutor_login') }}">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <div class="mb-3">
                            <label for="email" class="form-label">Email Address</label>
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

                        <button type="submit" class="btn btn-secondary btn-lg w-100 mb-3">Login</button>
                    </form>

                    <div class="text-center mb-3">
                        <p class="text-muted mb-2">Don't have an account?</p>
                        <a href="{{ url_for('tutor_register') }}" class="btn btn-outline-primary">
                            <i class="fas fa-user-plus me-2"></i>Apply to Become a Tutor
                        </a>
                    </div>

                    <div class="text-center mt-3">
                        <a href="{{ url_for('portal_home') }}" class="text-muted text-decoration-none"><i
                                class="fas fa-arrow-left me-1"></i> Back to Portal</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
