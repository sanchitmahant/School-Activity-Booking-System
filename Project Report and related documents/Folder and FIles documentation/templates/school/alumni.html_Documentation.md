# HTML Template: alumni.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\school\alumni.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Alumni Network{% endblock %}

{% block content %}
<!-- Hero Section -->
<div style="background: linear-gradient(135deg, #002E5D 0%, #0056A3 100%); padding: 100px 0;">
    <div class="container text-center text-white">
        <h1 class="display-3 fw-bold mb-4" style="color: white;">Greenwood Alumni</h1>
        <p class="lead" style="max-width: 800px; margin: 0 auto; font-size: 1.3rem;">
            A global community of leaders, innovators, and changemakers shaping the future
        </p>
        <p class="mt-4" style="font-size: 1.1rem; opacity: 0.9;">
            <strong>8,500+ alumni</strong> in over <strong>75 countries</strong>
        </p>
    </div>
</div>

<!-- Notable Alumni -->
<div class="py-6" style="background: white;">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3" style="color: #002E5D;">Distinguished Alumni</h2>
            <p class="lead text-muted">Leading in fields from medicine to technology, arts to public service</p>
        </div>

        <div class="row g-4">
            <!-- Dr. Emily Watson -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4 text-center">
                        <div class="mx-auto mb-4">
                            <img src="https://randomuser.me/api/portraits/women/44.jpg" alt="Dr. Emily Watson"
                                style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #FF6B6B;">
                        </div>
                        <h4 class="fw-bold mb-2">Dr. Emily Watson</h4>
                        <p class="text-muted mb-3">Chief Surgeon, Royal Marsden Hospital</p>
                        <p class="small">"Greenwood instilled in me the discipline and compassion that define my
                            approach to medicine. The rigorous science program prepared me perfectly for Cambridge
                            Medical School."</p>
                    </div>
                </div>
            </div>

            <!-- James Chen -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4 text-center">
                        <div class="mx-auto mb-4">
                            <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="James Chen"
                                style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #4facfe;">
                        </div>
                        <h4 class="fw-bold mb-2">James Chen</h4>
                        <p class="text-muted mb-3">Tech Entrepreneur, AI Startup Founder</p>
                        <p class="small">"The robotics and programming courses at Greenwood sparked my passion for AI.
                            Now my company develops cutting-edge machine learning solutions used globally."</p>
                    </div>
                </div>
            </div>

            <!-- Sophie Laurent -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4 text-center">
                        <div class="mx-auto mb-4">
                            <img src="https://randomuser.me/api/portraits/women/65.jpg" alt="Sophie Laurent"
                                style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #43e97b;">
                        </div>
                        <h4 class="fw-bold mb-2">Sophie Laurent</h4>
                        <p class="text-muted mb-3">Concert Pianist, Royal Philharmonic</p>
                        <p class="small">"Training under Dr. Richardson at Greenwood gave me the foundation for my
                            performing career. The school's dedication to excellence in music is unmatched."</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row g-4 mt-2">
            <!-- Marcus Okafor -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4 text-center">
                        <div class="mx-auto mb-4">
                            <img src="https://randomuser.me/api/portraits/men/59.jpg" alt="Hon. Marcus Okafor"
                                style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #f093fb;">
                        </div>
                        <h4 class="fw-bold mb-2">Hon. Marcus Okafor</h4>
                        <p class="text-muted mb-3">Member of Parliament, Minister of Education</p>
                        <p class="small">"Greenwood taught me the importance of service and leadership. The debate
                            society and Model UN prepared me for a career in public service."</p>
                    </div>
                </div>
            </div>

            <!-- Professor Amelia Singh -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4 text-center">
                        <div class="mx-auto mb-4">
                            <img src="https://randomuser.me/api/portraits/women/26.jpg" alt="Professor Amelia Singh"
                                style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #667eea;">
                        </div>
                        <h4 class="fw-bold mb-2">Professor Amelia Singh</h4>
                        <p class="text-muted mb-3">Research Fellow, CERN</p>
                        <p class="small">"The advanced mathematics and physics programs at Greenwood set me on the path
                            to particle physics research. I'm proud to represent the school in my field."</p>
                    </div>
                </div>
            </div>

            <!-- Rachel Thompson -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4 text-center">
                        <div class="mx-auto mb-4">
                            <img src="https://randomuser.me/api/portraits/women/33.jpg" alt="Rachel Thompson"
                                style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #FFD700;">
                        </div>
                        <h4 class="fw-bold mb-2">Rachel Thompson</h4>
                        <p class="text-muted mb-3">Olympic Gold Medalist, Swimming</p>
                        <p class="small">"Training with Coach Anderson's elite squad prepared me for Olympic
                            competition. The facilities and coaching at Greenwood are world-class."</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Career Paths -->
<div class="py-6" style="background: linear-gradient(to bottom, #f8f9fa, #ffffff);">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3" style="color: #002E5D;">Where They Are Now</h2>
            <p class="lead text-muted">Alumni excellence across industries</p>
        </div>

        <div class="row g-4">
            <div class="col-md-3 text-center">
                <div class="p-4">
                    <h3 class="display-4 fw-bold mb-2" style="color: #0DA49F;">32%</h3>
                    <p class="fw-bold mb-2">Medicine & Healthcare</p>
                    <p class="small text-muted">Doctors, Surgeons, Researchers</p>
                </div>
            </div>
            <div class="col-md-3 text-center">
                <div class="p-4">
                    <h3 class="display-4 fw-bold mb-2" style="color: #0DA49F;">28%</h3>
                    <p class="fw-bold mb-2">Technology & Engineering</p>
                    <p class="small text-muted">Tech Entrepreneurs, Engineers</p>

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
