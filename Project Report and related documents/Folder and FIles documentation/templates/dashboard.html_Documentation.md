# HTML Template: dashboard.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\dashboard.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="container py-5">
    <!-- Welcome Section -->
    <div class="row mb-5">
        <div class="col-12">
            <div
                class="card bg-primary text-white p-4 d-flex flex-row justify-content-between align-items-center shadow-sm">
                <div>
                    <h2 class="mb-0 font-heading">Welcome back, {{ parent.full_name }}</h2>
                    <p class="mb-0 opacity-75">{{ now.strftime('%A, %B %d, %Y') }}</p>
                </div>
                <button class="btn btn-light text-primary fw-bold" data-bs-toggle="modal"
                    data-bs-target="#addChildModal">
                    <i class="fas fa-plus me-2"></i> Add Child
                </button>
            </div>
        </div>
    </div>

    <div class="row g-4">
        <!-- Sidebar: Children & Bookings -->
        <div class="col-lg-4">
            <!-- My Children -->
            <div class="card mb-4 shadow-sm">
                <div class="card-header bg-white border-bottom">
                    <h5 class="mb-0 text-primary"><i class="fas fa-child me-2"></i> My Children</h5>
                </div>
                {% if children %}
                <div class="list-group list-group-flush">
                    {% for child in children %}
                    <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-0 fw-bold">{{ child.name }}</h6>
                            <small class="text-muted">Year {{ child.grade }} | Age: {{ child.age }}</small>
                        </div>
                        <span class="badge bg-secondary rounded-pill">{{ child.bookings|length }} Bookings</span>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="card-body text-center text-muted">
                    <p class="mb-0">No children added yet.</p>
                </div>
                {% endif %}
            </div>

            <!-- Upcoming Bookings -->
            <div class="card shadow-sm">
                <div class="card-header bg-white border-bottom">
                    <h5 class="mb-0 text-primary"><i class="fas fa-calendar-check me-2"></i> My Bookings</h5>
                </div>
                {% if bookings %}
                <div class="list-group list-group-flush">
                    {% for booking in bookings %}
                    <div class="list-group-item">
                        <div class="d-flex justify-content-between">
                            <h6 class="mb-1 fw-bold">{{ booking.activity.name }}</h6>
                            <span class="badge bg-success">Confirmed</span>
                        </div>
                        <p class="mb-1 small text-muted">Child: {{ booking.child.name }}</p>
                        <div class="d-flex justify-content-between align-items-center mt-2">
                            <small class="text-muted"><i class="far fa-clock me-1"></i> {{
                                booking.booking_date.strftime('%d %b %Y') }}</small>
                            <div>
                                <a href="{{ url_for('generate_invoice', booking_id=booking.id) }}"
                                    class="btn btn-sm btn-outline-primary rounded-circle" title="Download Invoice">
                                    <i class="fas fa-file-invoice"></i>
                                </a>
                                <form action="{{ url_for('cancel_booking', booking_id=booking.id) }}" method="POST"
                                    style="display:inline;"
                                    onsubmit="return confirm('Are you sure you want to cancel this booking?');">
                                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                                    <button type="submit" class="btn btn-sm btn-outline-danger rounded-circle"
                                        title="Cancel">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="card-body text-center text-muted">
                    <p class="mb-0">No active bookings.</p>
                </div>
                {% endif %}
            </div>
        </div>

        <!-- Main Content: Available Activities -->
        <div class="col-lg-8">
            <h3 class="mb-4 font-heading text-primary">Available Activities</h3>
            <div class="row g-4">
                {% for activity in activities %}
                <div class="col-md-6">
                    <div class="card h-100 shadow-sm border-0">
                        <div class="card-header bg-white border-0 pt-4 px-4 pb-0">
                            <div class="d-flex justify-content-between align-items-start">
                                <span class="badge bg-secondary">{{ activity.day_of_week }}</span>
                                <h4 class="text-primary fw-bold mb-0">£{{ "%.2f"|format(activity.price) }}</h4>
                            </div>
                        </div>
                        <div class="card-body px-4">
                            <h5 class="card-title fw-bold mt-2">{{ activity.name }}</h5>
                            <p class="text-muted small mb-2">
                                <i class="far fa-clock me-1"></i> {{ activity.start_time }} - {{ activity.end_time }}
                                <span class="mx-2">|</span>
                                <i class="fas fa-chalkboard-teacher me-1"></i> {{ activity.tutor.full_name if
                                activity.tutor else 'To be assigned' }}
                            </p>
                            <p class="card-text text-muted">{{ activity.description }}</p>

                            <div class="mt-3">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    {% set booked = activity.bookings|length %}
                                    {% set available = activity.max_capacity - booked %}
                                    {% set percent = (booked / activity.max_capacity) * 100 %}

                                    {% if percent >= 100 %}
                                    <span class="badge bg-danger">
                                        <i class="fas fa-exclamation-circle me-1"></i>FULL
                                    </span>
                                    {% elif available <= 3 %} <span class="badge bg-warning text-dark">
                                        <i class="fas fa-hourglass-half me-1"></i>Only {{ available }} spots left
                                        </span>
                                        {% else %}
                                        <span class="badge bg-success">
                                            <i class="fas fa-check-circle me-1"></i>{{ available }} spots available
                                        </span>
                                        {% endif %}

                                        <small class="text-muted">
                                            {{ booked }} / {{ activity.max_capacity }} enrolled
                                        </small>
                                </div>
                                <div class="progress" style="height: 8px;">
                                    <div class="progress-bar bg-{{ 'danger' if percent >= 100 else ('warning' if percent >= 75 else 'success') }}"
                                        style="width: {{ percent }}%" role="progressbar" aria-valuenow="{{ percent }}"
                                        aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                            </div>

                            <!-- Tutor Profile Link -->
                            {% if activity.tutor %}
                            <div class="mt-3 pt-3 border-top">

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
