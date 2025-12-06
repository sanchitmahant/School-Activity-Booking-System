# HTML Template: tutor_detail.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\admin\tutor_detail.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}{{ tutor.full_name }} - Tutor Profile{% endblock %}

{% block content %}
<div class="container py-5">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0"><i class="fas fa-user-graduate me-2 text-primary"></i>Tutor Profile</h2>
        <a href="{{ url_for('admin_tutors') }}" class="btn btn-outline-primary">
            <i class="fas fa-arrow-left me-2"></i>Back to Tutors
        </a>
    </div>

    <div class="row">
        <!-- Left Column - Profile Info -->
        <div class="col-lg-4 mb-4">
            <hr class="my-3">

            <div class="text-start">
                <p class="mb-2">
                    <i class="fas fa-envelope text-primary me-2"></i>
                    <strong>Email:</strong><br>
                    <span class="text-muted">{{ tutor.email }}</span>
                </p>
                <p class="mb-2">
                    <i class="fas fa-calendar text-primary me-2"></i>
                    <strong>Joined:</strong><br>
                    <span class="text-muted">{{ tutor.application_date.strftime('%B %d, %Y') if
                        tutor.application_date else 'N/A' }}</span>
                </p>
                {% if tutor.approved_by %}
                <p class="mb-0">
                    <i class="fas fa-user-check text-success me-2"></i>
                    <strong>Approved By:</strong><br>
                    <span class="text-muted">Admin ({{ tutor.approval_date.strftime('%B %d, %Y') if
                        tutor.approval_date else 'N/A' }})</span>
                </p>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Revenue Card -->
    <div class="card border-0 shadow-sm mt-4">
        <div class="card-header bg-success text-white">
            <h6 class="mb-0"><i class="fas fa-pound-sign me-2"></i>Revenue Generated</h6>
        </div>
        <div class="card-body text-center">
            <h2 class="text-success mb-0">£{{ "%.2f"|format(total_revenue) }}</h2>
            <p class="text-muted small mb-0">Total from {{ tutor.activities|length }} activities</p>
        </div>
        <div class="card-body p-0">
            {% if activity_stats %}
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Activity</th>
                            <th>Schedule</th>
                            <th>Enrolled</th>
                            <th>Capacity</th>
                            <th>Price</th>
                            <th>Revenue</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for stat in activity_stats %}
                        <tr>
                            <td><strong>{{ stat.activity.name }}</strong></td>
                            <td>
                                <span class="badge bg-secondary">{{ stat.activity.day_of_week }}</span>
                                <br><small class="text-muted">{{ stat.activity.start_time }} - {{
                                    stat.activity.end_time }}</small>
                            </td>
                            <td class="text-center">
                                <span class="badge bg-success">{{ stat.booked }}</span>
                            </td>
                            <td class="text-center">
                                <span class="badge bg-info">{{ stat.capacity }}</span>
                            </td>
                            <td class="text-center">
                                <strong>£{{ "%.2f"|format(stat.activity.price) }}</strong>
                            </td>
                            <td class="text-center">
                                <strong class="text-success">£{{ "%.2f"|format(stat.revenue) }}</strong>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                    <tfoot class="table-light">
                        <tr>
                            <td colspan="2"><strong>TOTAL</strong></td>
                            <td class="text-center"><strong>{{ total_students }} students</strong></td>
                            <td colspan="2"></td>
                            <td class="text-center"><strong class="text-success">£{{
                                    "%.2f"|format(total_revenue) }}</strong></td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            {% else %}
            <div class="p-4 text-center text-muted">
                <i class="fas fa-inbox fa-3x mb-3"></i>
                <p class="mb-0">This tutor has no assigned activities yet.</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>
</div>
</div>

<style>
    .avatar {
        font-weight: bold;
    }
</style>
{% endblock %}
```
