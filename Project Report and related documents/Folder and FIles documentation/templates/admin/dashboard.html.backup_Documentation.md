# Resource File: dashboard.html.backup

## 1. Executive Summary
A supporting file used by the application for configuration or data storage.

## 2. Code Logic & Functionality
Contains static data or configuration parameters read by the application at runtime.

## 3. Key Concepts & Definitions
- **Static Asset**: A file that is not generated dynamically (e.g., images, text files).
- **Configuration**: Settings that determine the behavior of the software.

## 4. Location Details
**Path**: `templates\admin\dashboard.html.backup`
**Type**: .BACKUP File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```backup
{% extends "base.html" %}

{% block title %}Admin Dashboard{% endblock %}

{% block content %}
<div class="container py-5">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-5">
        <div>
            <h1 class="fw-bold font-heading text-primary">Command Center</h1>
            <p class="text-muted">System Overview & Management</p>
        </div>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addActivityModal">
            <i class="fas fa-plus me-2"></i> New Activity
        </button>
    </div>

    <!-- Stats Row -->
    <div class="row g-4 mb-5">
        <div class="col-md-4">
            <div class="card shadow-sm border-0 h-100">
                <div class="card-body d-flex align-items-center">
                    <div class="rounded-circle bg-primary bg-opacity-10 p-3 me-3">
                        <i class="fas fa-calendar-check fa-2x text-primary"></i>
                    </div>
                    <div>
                        <h3 class="mb-0 fw-bold">{{ total_bookings }}</h3>
                        <small class="text-muted">Total Bookings</small>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card shadow-sm border-0 h-100">
                <div class="card-body d-flex align-items-center">
                    <div class="rounded-circle bg-success bg-opacity-10 p-3 me-3">
                        <i class="fas fa-pound-sign fa-2x text-success"></i>
                    </div>
                    <div>
                        <h3 class="mb-0 fw-bold">£{{ "%.2f"|format(total_revenue) }}
                        </h3>
                        <small class="text-muted">Total Revenue</small>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card shadow-sm border-0 h-100">
                <div class="card-body d-flex align-items-center">
                    <div class="rounded-circle bg-warning bg-opacity-10 p-3 me-3">
                        <i class="fas fa-users fa-2x text-warning"></i>
                    </div>
                    <div>
                        <h3 class="mb-0 fw-bold">{{ activities|length }}</h3>
                        <small class="text-muted">Active Activities</small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Activity Management -->
    <div class="card shadow-sm border-0 mb-5">
        <div class="card-header bg-white border-bottom py-3">
            <h5 class="mb-0 text-primary"><i class="fas fa-tasks me-2"></i> Manage
                Activities</h5>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Name</th>
                            <th>Schedule</th>
                            <th>Price</th>
                            <th>Capacity</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for activity in activities %}
                        <tr>
                            <td class="align-middle fw-bold">{{ activity.name }}
                            </td>
                            <td class="align-middle">
                                <span class="badge bg-secondary">{{ activity.day_of_week }}</span>
                                <small class="d-block text-muted">{{ activity.start_time }} - {{ activity.end_time
                                    }}</small>
                            </td>
                            <td class="align-middle">£{{ "%.2f"|format(activity.price) }}</td>
                            <td class="align-middle">
                                <span
                                    class="badge bg-{{ 'danger' if activity.bookings|length >= activity.max_capacity else 'success' }}">
                                    {{ activity.bookings|length }} / {{ activity.max_capacity }}
                                </span>
                            </td>
                            <td class="align-middle">
                                <button class="btn btn-sm btn-outline-primary rounded-circle me-1"
                                    data-bs-toggle="modal" data-bs-target="#viewBookingsModal{{ activity.id }}"
                                    title="View Bookings">
                                    <i class="fas fa-users"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-primary rounded-circle me-1"
                                    data-bs-toggle="modal" data-bs-target="#editActivityModal"
                                    data-id="{{ activity.id }}" data-name="{{ activity.name }}"
                                    data-price="{{ activity.price }}" data-day="{{ activity.day_of_week }}"
                                    data-start="{{ activity.start_time }}" data-end="{{ activity.end_time }}"
                                    data-tutor="{{ activity.tutor_id if activity.tutor_id else '' }}">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger rounded-circle" data-bs-toggle="modal"
                                    data-bs-target="#deleteModal"
                                    data-url="{{ url_for('delete_activity', id=activity.id) }}"><i
                                        class="fas fa-trash"></i></button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Tutor Management -->
    <div class="card shadow-sm border-0 mb-5">
        <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
            <h5 class="mb-0 text-primary"><i class="fas fa-chalkboard-teacher me-2"></i> Manage
                Tutors</h5>
            <button class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addTutorModal">
                <i class="fas fa-plus me-1"></i> Add Tutor
            </button>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Name</th>
                            <th>Specialization</th>
                            <th>Email</th>
                            <th>Assigned Activities</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for tutor in tutors %}
                        <tr>
                            <td class="align-middle fw-bold">{{ tutor.full_name }}
                            </td>
                            <td class="align-middle">{{ tutor.specialization }}</td>

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
