# HTML Template: payment.html

## 1. Executive Summary
Defines the structural layout and content for a specific web page view.

## 2. Code Logic & Functionality
Uses the Jinja2 templating engine. The file allows for dynamic data insertion using `{{ variable }}` syntax and control structures like `{% if %}` loops within standard HTML markup.

## 3. Key Concepts & Definitions
- **Jinja2**: A modern and designer-friendly templating language for Python.
- **Template Inheritance**: The ability to extend a base layout (`base.html`) to avoid code duplication.
- **DOM**: Document Object Model, the data representation of the objects that comprise the structure and content of a document on the web.

## 4. Location Details
**Path**: `templates\payment.html`
**Type**: .HTML File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```html
{% extends "base.html" %}

{% block title %}Secure Checkout{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="row g-4">
                <!-- Left Side: Payment Form -->
                <div class="col-md-7">
                    <div class="card shadow-sm border-0" style="border-radius: 12px;">
                        <div class="card-body p-4">
                            <div class="mb-4">
                                <h5 class="fw-bold mb-1" style="color: #1a1a1a;">Payment Details</h5>
                                <p class="text-muted small mb-0">Complete your secure checkout</p>
                            </div>

                            <form id="payment-form" action="{{ url_for('book_activity') }}" method="POST">
                                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                                <input type="hidden" name="activity_id" value="{{ activity.id }}">
                                <input type="hidden" name="child_id" value="{{ child.id }}">
                                <input type="hidden" name="booking_date" value="{{ date }}">

                                <!-- Email -->
                                <div class="mb-4">
                                    <label class="form-label small fw-600 mb-2"
                                        style="color: #4a4a4a; letter-spacing: 0.3px;">Email Address</label>
                                    <input type="email" name="email" class="form-control" placeholder="you@example.com"
                                        required
                                        style="padding: 13px 15px; font-size: 15px; border: 1px solid #d1d5db; border-radius: 8px;">
                                </div>

                                <!-- Card Information -->
                                <div class="mb-4">
                                    <label class="form-label small fw-600 mb-2"
                                        style="color: #4a4a4a; letter-spacing: 0.3px;">Card Information</label>
                                    <div class="border rounded-3"
                                        style="overflow: hidden; border-color: #d1d5db !important;">
                                        <!-- Card Number -->
                                        <div class="position-relative" style="border-bottom: 1px solid #e5e7eb;">
                                            <input type="text" name="card_number" id="card-number"
                                                class="form-control border-0" placeholder="1234 5678 9012 3456"
                                                maxlength="19" required
                                                style="padding: 14px 50px 14px 45px; font-size: 15px; font-family: 'Courier New', monospace;">
                                            <div class="position-absolute top-50 start-0 translate-middle-y ms-3">
                                                <i class="fas fa-credit-card text-muted" id="card-icon"></i>
                                            </div>
                                            <div class="position-absolute top-50 end-0 translate-middle-y me-3">
                                                <i class="fab fa-cc-visa text-muted opacity-50"
                                                    style="font-size: 24px;"></i>
                                            </div>
                                        </div>
                                        <!-- Expiry & CVC -->
                                        <div class="row g-0">
                                            <div class="col-6" style="border-right: 1px solid #e5e7eb;">
                                                <input type="text" name="expiry_date" id="expiry"
                                                    class="form-control border-0" placeholder="MM / YY" maxlength="7"
                                                    required
                                                    style="padding: 14px 15px; font-size: 15px; font-family: 'Courier New', monospace;">
                                            </div>
                                            <div class="col-6">
                                                <input type="text" name="cvv" id="cvc" class="form-control border-0"
                                                    placeholder="CVV" maxlength="4" required
                                                    style="padding: 14px 15px; font-size: 15px; font-family: 'Courier New', monospace;">
                                            </div>
                                        </div>
                                    </div>
                                    <small class="text-muted d-block mt-2"><i class="fas fa-lock me-1"></i> Your payment
                                        information is encrypted</small>
                                </div>

                                <!-- Cardholder Name -->
                                <div class="mb-4">
                                    <label class="form-label small fw-600 mb-2"
                                        style="color: #4a4a4a; letter-spacing: 0.3px;">Cardholder Name</label>
                                    <input type="text" name="cardholder_name" class="form-control"
                                        placeholder="John Doe" required
                                        style="padding: 13px 15px; font-size: 15px; border: 1px solid #d1d5db; border-radius: 8px;">
                                </div>

                                <!-- Billing Address -->
                                <div class="mb-4">
                                    <label class="form-label small fw-600 mb-2"
                                        style="color: #4a4a4a; letter-spacing: 0.3px;">Billing Address</label>
                                    <input type="text" class="form-control mb-3" placeholder="Street address" required
                                        style="padding: 13px 15px; font-size: 15px; border: 1px solid #d1d5db; border-radius: 8px;">
                                    <div class="row g-3">
                                        <div class="col-6">
                                            <input type="text" class="form-control" placeholder="City" required
                                                style="padding: 13px 15px; font-size: 15px; border: 1px solid #d1d5db; border-radius: 8px;">
                                        </div>
                                        <div class="col-6">
                                            <input type="text" class="form-control" placeholder="Postcode" required
                                                style="padding: 13px 15px; font-size: 15px; border: 1px solid #d1d5db; border-radius: 8px;">
                                        </div>
                                    </div>
                                </div>

                                <!-- Payment Button -->
                                <button type="submit" id="pay-btn" class="btn w-100 py-3 fw-semibold shadow-sm"
                                    style="background: #0DA49F; border: none; font-size: 16px; border-radius: 8px; color: white; transition: all 0.2s;">
                                    <i class="fas fa-lock me-2"></i>Pay £{{ "%.2f"|format(activity.price) }}
                                </button>

                                <!-- Security Notice -->
                                <div class="text-center mt-4">
                                    <div
                                        class="d-flex justify-content-center align-items-center gap-3 text-muted small">
                                        <span><i class="fas fa-shield-alt me-1"></i> Secure checkout</span>
                                        <span>•</span>
                                        <span><i class="fas fa-lock me-1"></i> 256-bit encryption</span>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>

                <!-- Right Side: Order Summary -->
                <div class="col-md-5">
                    <div class="card shadow-sm border-0" style="border-radius: 12px; background: #f9fafb;">
                        <div class="card-body p-4">
                            <h6 class="fw-bold mb-4" style="color: #1a1a1a;">Order Summary</h6>

                            <!-- Activity Details -->
                            <div class="mb-4 pb-4" style="border-bottom: 1px solid #e5e7eb;">
                                <div class="fw-semibold mb-2" style="color: #1a1a1a;">{{ activity.name }}</div>
                                <div class="small text-muted mb-1">
                                    <i class="fas fa-user me-2"></i>{{ child.name }}
                                </div>
                                <div class="small text-muted mb-1">
                                    <i class="fas fa-calendar me-2"></i>{{ activity.day_of_week }}, {{ date }}
                                </div>
                                <div class="small text-muted">
                                    <i class="fas fa-clock me-2"></i>{{ activity.start_time }} - {{ activity.end_time }}
                                </div>
                            </div>

                            <!-- Price Breakdown -->
                            <div class="mb-4 pb-4" style="border-bottom: 1px solid #e5e7eb;">
                                <div class="d-flex justify-content-between mb-3">
                                    <span class="text-muted">Activity Fee</span>
                                    <span class="fw-semibold">£{{ "%.2f"|format(activity.price) }}</span>
                                </div>
                                <div class="d-flex justify-content-between">
                                    <span class="text-muted">Service Fee</span>
                                    <span class="text-success fw-semibold">FREE</span>
                                </div>
                            </div>

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
