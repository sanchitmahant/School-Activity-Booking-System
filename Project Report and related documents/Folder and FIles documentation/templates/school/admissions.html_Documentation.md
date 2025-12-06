# HTML Template: admissions.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\school\admissions.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Admissions{% endblock %}

{% block content %}
<!-- Hero Section -->
<div style="background: linear-gradient(135deg, #002E5D 0%, #0056A3 100%); padding: 100px 0;">
    <div class="container text-center text-white">
        <h1 class="display-3 fw-bold mb-4" style="color: white;" style="color: white;">Join Greenwood International</h1>
        <p class="lead" style="max-width: 800px; margin: 0 auto; font-size: 1.3rem;">
            Welcoming exceptional students who aspire to excellence, leadership, and lifelong learning
        </p>
    </div>
</div>

<!-- Quick Process Overview -->
<div style="background: #0DA49F; padding: 50px 0;">
    <div class="container">
        <div class="row text-center text-white">
            <div class="col-md-3">
                <div class="mb-3">
                    <div
                        style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                        <span class="display-6 fw-bold">1</span>
                    </div>
                </div>
                <p class="fw-bold mb-0">Inquiry & Tour</p>
            </div>
            <div class="col-md-3">
                <div class="mb-3">
                    <div
                        style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                        <span class="display-6 fw-bold">2</span>
                    </div>
                </div>
                <p class="fw-bold mb-0">Application</p>
            </div>
            <div class="col-md-3">
                <div class="mb-3">
                    <div
                        style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                        <span class="display-6 fw-bold">3</span>
                    </div>
                </div>
                <p class="fw-bold mb-0">Assessment</p>
            </div>
            <div class="col-md-3">
                <div class="mb-3">
                    <div
                        style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                        <span class="display-6 fw-bold">4</span>
                    </div>
                </div>
                <p class="fw-bold mb-0">Offer & Registration</p>
            </div>
        </div>
    </div>
</div>

<!-- Main Content -->
<div class="py-6" style="background: white;">
    <div class="container">
        <div class="row g-5">
            <div class="col-lg-8">
                <h2 class="display-6 fw-bold mb-4" style="color: #002E5D;">Application Process</h2>

                <div class="mb-5">
                    <h4 class="fw-bold mb-3" style="color: #0DA49F;">
                        <i class="fas fa-calendar-check me-2"></i>Key Dates
                    </h4>
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-4">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <p class="fw-bold mb-1">Autumn Term Applications</p>
                                    <p class="text-muted mb-0">Deadline: 31st March 2025</p>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <p class="fw-bold mb-1">Spring Term Applications</p>
                                    <p class="text-muted mb-0">Deadline: 31st October 2024</p>
                                </div>
                                <div class="col-md-6">
                                    <p class="fw-bold mb-1">Assessment Days</p>
                                    <p class="text-muted mb-0">January & June annually</p>
                                </div>
                                <div class="col-md-6">
                                    <p class="fw-bold mb-1">Campus Tours</p>
                                    <p class="text-muted mb-0">Every Friday at 10:00 AM</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mb-5">
                    <h4 class="fw-bold mb-3" style="color: #0DA49F;">
                        <i class="fas fa-user-graduate me-2"></i>Entry Requirements
                    </h4>
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-4">
                            <ul class="mb-0">
                                <li class="mb-2">Completed application form with recent photograph</li>
                                <li class="mb-2">Previous 2 years academic reports and transcripts</li>
                                <li class="mb-2">Two teacher references (preferably from English & Mathematics teachers)
                                </li>
                                <li class="mb-2">Personal statement (500 words) describing interests and aspirations
                                </li>
                                <li class="mb-2">Assessment in English, Mathematics, and Reasoning</li>
                                <li>Interview with Headmaster and relevant Head of Department</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="mb-5">
                    <h4 class="fw-bold mb-3" style="color: #0DA49F;">
                        <i class="fas fa-pound-sign me-2"></i>Fees & Financial Aid
                    </h4>
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-4">
                            <p><strong>Day Student Fees:</strong> £8,500 per term</p>
                            <div class="card-body p-4">
                                <h4 class="fw-bold mb-4" style="color: white;">Admissions Office</h4>
                                <p class="mb-3">
                                    <i class="fas fa-envelope me-2"></i>
                                    greenwoodinternationaluk@gmail.com
                                </p>
                                <p class="mb-3">
                                    <i class="fas fa-phone me-2"></i>
                                    +44 (0) 1491 570000
                                </p>
                                <p class="mb-4">
                                    <i class="fas fa-clock me-2"></i>
                                    Mon-Fri: 8:00 AM - 5:00 PM
                                </p>
                                <a href="{{ url_for('contact') }}" class="btn btn-light w-100 rounded-pill">
                                    Contact Us
                                </a>
                            </div>
                        </div>

                        <!-- Why Choose Us -->
                        <div class="card border-0 shadow-sm">
                            <div class="card-body p-4">
                                <h5 class="fw-bold mb-4" style="color: #002E5D;">Why Greenwood?</h5>
                                <div class="mb-3">
                                    <i class="fas fa-check-circle me-2" style="color: #0DA49F;"></i>
                                    <strong>98%</strong> university placement rate
                                </div>
                                <div class="mb-3">

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
