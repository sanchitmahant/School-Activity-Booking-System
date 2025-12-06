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
**Path**: `templates\tutor\dashboard.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Tutor Dashboard{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h1 class="text-primary mb-1">Welcome, {{ tutor.full_name }}</h1>
            <p class="text-muted">Manage your activities and track attendance.</p>
        </div>
        <div class="text-end">
            <span class="badge bg-secondary p-2 fs-6 mb-2">{{ tutor.specialization }}</span>
            <br>
            <small class="text-muted">{{ now.strftime('%A, %d %B %Y') }}</small>
        </div>
    </div>

    <div class="row">
        <!-- Assigned Activities -->
        <div class="col-lg-12">
            <div class="card shadow-sm border-0 mb-4">
                <div class="card-header bg-white border-bottom py-3">
                    <h5 class="mb-0 text-primary"><i class="fas fa-calendar-alt me-2"></i> Your Activities</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="bg-light">
                                <tr>
                                    <th class="ps-4">Activity Name</th>
                                    <th>Schedule</th>
                                    <th>Enrolled</th>
                                    <th>Capacity</th>
                                    <th class="text-end pe-4">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for activity in activities %}
                                <tr>
                                    <td class="ps-4 fw-bold">{{ activity.name }}</td>
                                    <td>
                                        <span class="badge bg-light text-dark border">
                                            {{ activity.day_of_week }} | {{ activity.start_time }} - {{
                                            activity.end_time }}
                                        </span>
                                    </td>
                                    <td>
                                        {% set enrolled_count = activity.bookings|selectattr('status', 'equalto',
                                        'confirmed')|list|length %}
                                        <span
                                            class="badge bg-{{ 'success' if enrolled_count < activity.max_capacity else 'danger' }}">
                                            {{ enrolled_count }} Student(s)
                                        </span>
                                    </td>
                                    <td>{{ activity.max_capacity }}</td>
                                    <td class="text-end pe-4">
                                        <a href="{{ url_for('tutor_attendance', activity_id=activity.id) }}"
                                            class="btn btn-sm btn-primary me-2">
                                            <i class="fas fa-clipboard-check me-1"></i> Mark Attendance
                                        </a>
                                        <a href="{{ url_for('attendance_history', activity_id=activity.id) }}"
                                            class="btn btn-sm btn-outline-secondary">
                                            <i class="fas fa-history me-1"></i> History
                                        </a>
                                    </td>
                                </tr>
                                {% else %}
                                <tr>
                                    <td colspan="5" class="text-center py-4 text-muted">
                                        You have not been assigned any activities yet.
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
