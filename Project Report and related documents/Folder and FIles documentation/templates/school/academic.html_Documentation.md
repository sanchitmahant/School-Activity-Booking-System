# HTML Template: academic.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\school\academic.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{%block title %}Academic Excellence{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="academic-hero"
    style="background: linear-gradient(135deg, #002E5D 0%, #0056A3 100%); padding: 100px 0; position: relative; overflow: hidden;">
    <div class="container text-center text-white" style="position: relative; z-index: 2;">
        <h1 class="display-3 fw-bold mb-4" style="color: white;" data-aos="fade-up" style="color: white;">Academic Excellence</h1>
        <p class="lead" style="max-width: 700px; margin: 0 auto; font-size: 1.3rem;" data-aos="fade-up"
            data-aos-delay="100">
            Inspiring minds, nurturing talents, and preparing global leaders for tomorrow's challenges
        </p>
    </div>
</div>

<!-- Stats Bar -->
<div style="background: #0DA49F; padding: 40px 0;">
    <div class="container">
        <div class="row text-center text-white">
            <div class="col-md-3">
                <h2 class="display-4 fw-bold mb-2">98%</h2>
                <p class="mb-0">University Placement Rate</p>
            </div>
            <div class="col-md-3">
                <h2 class="display-4 fw-bold mb-2">A*-A</h2>
                <p class="mb-0">Average A-Level Grade</p>
            </div>
            <div class="col-md-3">
                <h2 class="display-4 fw-bold mb-2">42</h2>
                <p class="mb-0">Average IB Diploma Score</p>
            </div>
            <div class="col-md-3">
                <h2 class="display-4 fw-bold mb-2">15+</h2>
                <p class="mb-0">Elite Instructors</p>
            </div>
        </div>
    </div>
</div>

<!-- Curriculum Overview -->
<div class="py-6" style="background: white;">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3" style="color: #002E5D;">World-Class Extended Learning</h2>
            <p class="lead text-muted">Beyond the classroom: enrichment programs designed by Oxford & Cambridge
                graduates</p>
        </div>

        <div class="row g-4">
            <div class="col-md-6" data-aos="fade-right">
                <div class="p-5 h-100"
                    style="background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 20px; color: white;">
                    <i class="fas fa-atom fa-3x mb-4" style="opacity: 0.9;"></i>
                    <h3 class="fw-bold mb-3" style="color: white;">STEM Excellence</h3>
                    <p style="opacity: 0.95;">Advanced Mathematics, Science Olympiads, and Robotics with PhD-level
                        instruction. Our students regularly compete at international level in IMO, Science Bowl, and
                        FIRST Robotics championships.</p>
                    <ul class="mt-4" style="opacity: 0.9;">
                        <li>Mathematics Olympiad Preparation (IMO, UKMT)</li>
                        <li>Advanced AI & Machine Learning</li>
                        <li>Experimental Science & Research</li>
                        <li>Competitive Robotics Engineering</li>
                    </ul>
                </div>
            </div>

            <div class="col-md-6" data-aos="fade-left">
                <div class="p-5 h-100"
                    style="background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 20px; color: white;">
                    <i class="fas fa-book-open fa-3x mb-4" style="opacity: 0.9;"></i>
                    <h3 class="fw-bold mb-3" style="color: white;">Humanities & Languages</h3>
                    <p style="opacity: 0.95;">Literature, Philosophy, and Multilingual Excellence taught by published
                        scholars and native speakers. Preparation for Oxford/Cambridge entrance examinations included.
                    </p>
                    <ul class="mt-4" style="opacity: 0.9;">
                        <li>Creative Writing with Published Authors</li>
                        <li>Advanced Mandarin & French (DELF/HSK)</li>
                        <li>Classical Literature & Philosophy</li>
                        <li>International Debate & Public Speaking</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="row g-4 mt-4">
            <div class="col-md-6" data-aos="fade-right" data-aos-delay="100">
                <div class="p-5 h-100"
                    style="background: linear-gradient(135deg, #4facfe, #00f2fe); border-radius: 20px; color: white;">
                    <i class="fas fa-palette fa-3x mb-4" style="opacity: 0.9;"></i>
                    <h3 class="fw-bold mb-3" style="color: white;">Performing & Visual Arts</h3>
                    <p style="opacity: 0.95;">Concert-level music instruction and exhibition-quality art programs.
                        Training by Royal Academy musicians and exhibited contemporary artists.</p>
                    <ul class="mt-4" style="opacity: 0.9;">
                        <li>Classical Piano & Violin (ABRSM Diploma)</li>
                        <li>Contemporary & Digital Art Portfolio</li>
                        <li>Chamber Music & Orchestra</li>
                        <li>Art School Application Preparation</li>
                    </ul>
                </div>
            </div>

            <div class="col-md-6" data-aos="fade-left" data-aos-delay="100">
                <div class="p-5 h-100"
                    style="background: linear-gradient(135deg, #43e97b, #38f9d7); border-radius: 20px; color: white;">
                    <i class="fas fa-trophy fa-3x mb-4" style="opacity: 0.9;"></i>
                    <h3 class="fw-bold mb-3" style="color: white;">Elite Athletics</h3>
                    <p style="opacity: 0.95;">Professional-level coaching in tennis, swimming, and athletics. Trained by
                        Olympic coaches and former professional athletes.</p>
                    <ul class="mt-4" style="opacity: 0.9;">
                        <li>Competitive Tennis (LTA Pathway)</li>
                        <li>Elite Swimming Squad (ASA Level 4)</li>
                        <li>Sports Science & Athletic Development</li>
                        <li>National Competition Preparation</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Student Achievements -->
<div class="py-6" style="background: linear-gradient(to bottom, #f8f9fa, #ffffff);">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3" style="color: #002E5D;" style="color: white;">Recent Student Achievements</h2>
            <p class="lead text-muted">Excellence recognized globally</p>
        </div>

        <div class="row g-4">
            <div class="col-md-4" data-aos="zoom-in">
                <div class="card border-0 shadow-sm h-100 p-4 text-center">
                    <div class="mx-auto mb-3"
                        style="width: 80px; height: 80px; background: linear-gradient(135deg, #FFD700, #FFA500); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-medal fa-2x text-white"></i>
                    </div>
                    <h4 class="fw-bold mb-3" style="color: white;">International Awards</h4>
                    <p class="text-muted">12 students won medals at International Mathematics Olympiad, Science Bowl,
                        and Model UN conferences in 2024</p>
                </div>
            </div>

            <div class="col-md-4" data-aos="zoom-in" data-aos-delay="100">
                <div class="card border-0 shadow-sm h-100 p-4 text-center">
                    <div class="mx-auto mb-3"
                        style="width: 80px; height: 80px; background: linear-gradient(135deg, #8B4513, #D2691E); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-university fa-2x text-white"></i>
                    </div>
                    <h4 class="fw-bold mb-3" style="color: white;">Oxbridge Success</h4>

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
