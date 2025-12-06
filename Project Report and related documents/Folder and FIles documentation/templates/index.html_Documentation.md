# HTML Template: index.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\index.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Portal{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row min-vh-75 align-items-center justify-content-center">
        <div class="col-lg-8 text-center">
            <h1 class="display-4 fw-bold text-3d mb-4">Student & Parent Portal</h1>
            <p class="lead mb-5">Manage activities, track progress, and stay connected.</p>

            <div class="row g-4 justify-content-center">
                <div class="col-md-5">
                    <div class="glass-card p-5 h-100">
                        <i class="fas fa-user-shield fa-3x mb-4 icon-teal"></i>
                        <h3>Parents</h3>
                        <p class="mb-4">Book activities, view invoices, and manage your children's schedule.</p>
                        <a href="{{ url_for('login') }}" class="btn btn-primary w-100 rounded-pill">Login</a>
                        <a href="{{ url_for('register') }}"
                            class="btn btn-outline-light w-100 rounded-pill mt-2">Register</a>
                    </div>
                </div>
                <div class="col-md-5">
                    <div class="glass-card p-5 h-100">
                        <i class="fas fa-chalkboard-teacher fa-3x mb-4 icon-gold"></i>
                        <h3>Staff & Tutors</h3>
                        <p class="mb-4">Manage classes, take attendance, and view rosters.</p>
                        <div class="d-grid gap-2">
                            <a href="{{ url_for('tutor_login') }}" class="btn btn-secondary rounded-pill">Tutor
                                Login</a>
                            <a href="{{ url_for('admin_login') }}" class="btn btn-outline-secondary rounded-pill">Admin
                                Login</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
