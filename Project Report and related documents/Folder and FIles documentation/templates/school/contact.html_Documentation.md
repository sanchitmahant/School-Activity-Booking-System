# HTML Template: contact.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\school\contact.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Contact Us{% endblock %}

{% block content %}
<!-- Header Section -->
<div class="py-5" style="background: linear-gradient(135deg, #002E5D 0%, #0056A3 100%);">
    <div class="container text-center text-white">
        <h1 class="display-4 fw-bold mb-3" style="color: white;">Get In Touch</h1>
        <p class="lead">We're here to help and answer any question you might have</p>
    </div>
</div>

<!-- Contact Section -->
<div class="container py-5">
    <div class="row g-4">
        <!-- Contact Form -->
        <div class="col-lg-7">
            <div class="card shadow-sm border-0 p-4">
                <h3 class="mb-4" style="color: #002E5D;">Send Us a Message</h3>
                <form action="{{ url_for('contact_submit') if url_for else '#' }}" method="POST">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" class="form-control" name="name" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Email Address</label>
                            <input type="email" class="form-control" name="email" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Phone Number</label>
                        <input type="tel" class="form-control" name="phone">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Subject</label>
                        <select class="form-select" name="subject" required>
                            <option value="">Select a topic...</option>
                            <option>General Inquiry</option>
                            <option>Admissions</option>
                            <option>Activities & Programs</option>
                            <option>Billing & Payments</option>
                            <option>Technical Support</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Message</label>
                        <textarea class="form-control" name="message" rows="5" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-lg w-100"
                        style="background: #0DA49F; color: white; border-radius: 50px;">
                        <i class="fas fa-paper-plane me-2"></i>Send Message
                    </button>
                </form>
            </div>
        </div>

        <!-- Contact Information -->
        <div class="col-lg-5">
            <div class="card shadow-sm border-0 p-4 mb-4"
                style="background: linear-gradient(135deg, #002E5D, #0056A3); color: white;">
                <h4 class="mb-4" style="color: white;">Contact Information</h4>

                <div class="mb-4">
                    <div class="d-flex align-items-start mb-3">
                        <i class="fas fa-map-marker-alt fa-lg me-3 mt-1"></i>
                        <div>
                            <h6 class="mb-1" style="color: white;">Address</h6>
                            <p class="mb-0" style="opacity: 0.9;">Greenwood Hall<br>Henley-on-Thames<br>Oxfordshire, RG9
                                1AA<br>United Kingdom</p>
                        </div>
                    </div>

                    <div class="d-flex align-items-start mb-3">
                        <i class="fas fa-phone fa-lg me-3 mt-1"></i>
                        <div>
                            <h6 class="mb-1" style="color: white;">Phone</h6>
                            <p class="mb-0" style="opacity: 0.9;">+44 (0) 1491 570000</p>
                        </div>
                    </div>

                    <div class="d-flex align-items-start mb-3">
                        <i class="fas fa-envelope fa-lg me-3 mt-1"></i>
                        <div>
                            <h6 class="mb-1" style="color: white;">Email</h6>
                            <p class="mb-0" style="opacity: 0.9;">greenwoodinternationaluk@gmail.com</p>
                        </div>
                    </div>

                    <div class="d-flex align-items-start">
                        <i class="fas fa-clock fa-lg me-3 mt-1"></i>
                        <div>
                            <h6 class="mb-1" style="color: white;">Office Hours</h6>
                            <p class="mb-0" style="opacity: 0.9;">
                                Monday - Friday: 8:00 AM - 5:00 PM<br>
                                Saturday: 9:00 AM - 1:00 PM<br>
                                Sunday: Closed
                            </p>
                        </div>
                    </div>
                </div>

                <div class="pt-3 border-top" style="border-color: rgba(255,255,255,0.2) !important;">
                    <h6 class="mb-3" style="color: white;">Follow Us</h6>
                    <div class="d-flex gap-3">
                        <a href="#" class="text-white"><i class="fab fa-facebook fa-2x"></i></a>
                        <a href="#" class="text-white"><i class="fab fa-twitter fa-2x"></i></a>
                        <a href="#" class="text-white"><i class="fab fa-instagram fa-2x"></i></a>
                        <a href="#" class="text-white"><i class="fab fa-linkedin fa-2x"></i></a>
                    </div>
                </div>
            </div>

            <!-- Quick Links -->
            <div class="card shadow-sm border-0 p-4">
                <h5 class="mb-3" style="color: #002E5D;">Quick Links</h5>
                <ul class="list-unstyled">
                    <li class="mb-2"><a href="{{ url_for('admissions') }}" style="color: #0DA49F;"><i
                                class="fas fa-chevron-right me-2"></i>Admissions</a></li>
                    <li class="mb-2"><a href="{{ url_for('portal_home') }}" style="color: #0DA49F;"><i
                                class="fas fa-chevron-right me-2"></i>Parent Portal</a></li>
                    <li class="mb-2"><a href="{{ url_for('academic') }}" style="color: #0DA49F;"><i
                                class="fas fa-chevron-right me-2"></i>Academic Programs</a></li>
                    <li><a href="{{ url_for('index') }}#activities" style="color: #0DA49F;"><i
                                class="fas fa-chevron-right me-2"></i>Activities</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- Map Section (Placeholder) -->
<div class="py-5" style="background: linear-gradient(135deg, #002E5D 0%, #0056A3 100%);">
    <div class="container">
        <h2 class="text-center mb-2 fw-bold" style="color: white;">Visit Our Campus</h2>
        <p class="text-center text-white mb-4" style="opacity: 0.9;">Greenwood Hall, Henley-on-Thames, Oxfordshire RG9
            1AA</p>
        <div class="card shadow-lg border-0" style="overflow: hidden; border-radius: 15px;">
            <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39788.77766418426!2d-0.9316744!3d51.5356871!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48769de8ec1c2c8d%3A0x5ee7f9a3b5e4b7c8!2sHenley-on-Thames!5e0!3m2!1sen!2suk!4v1234567890123!5m2!1sen!2suk"
                width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
        </div>
        <div class="text-center mt-4">
            <a href="https://www.google.com/maps/search/Henley-on-Thames+RG9+1AA" target="_blank"
                class="btn btn-lg px-5 py-3"
                style="background: #0DA49F; color: white; border: none; border-radius: 50px; font-weight: 600;">
                <i class="fas fa-directions me-2"></i>Get Directions
            </a>
        </div>
    </div>
</div>
{% endblock %}
```
