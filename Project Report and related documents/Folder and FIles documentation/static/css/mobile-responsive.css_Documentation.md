# Stylesheet: mobile-responsive.css

## 1. Executive Summary
Controls the visual presentation, formatting, and layout of the HTML documents.

## 2. Code Logic & Functionality
Defines CSS classes and ID selectors. Sets properties such as color, font-family, margin, and padding to create a responsive and cohesive visual design.

## 3. Key Concepts & Definitions
- **CSS3**: Cascading Style Sheets Level 3.
- **Responsive Design**: Web design approach that makes web pages render well on a variety of devices and window or screen sizes.
- **Selector**: The part of a CSS rule that describes the elements to be styled.

## 4. Location Details
**Path**: `static\css\mobile-responsive.css`
**Type**: .CSS File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```css
/**
 * Mobile Optimization & Responsive Enhancements
 * Touch-friendly, responsive design improvements
 */

/* Mobile-First Base Reset */
* {
    -webkit-tap-highlight-color: transparent;
    -webkit-touch-callout: none;
}

/* Touch-Friendly Buttons */
@media (hover: none) and (pointer: coarse) {

    .btn,
    button,
    a.btn {
        min-height: 44px;
        /* iOS minimum touch target */
        padding: 12px 20px;
    }

    .btn-sm {
        min-height: 40px;
        padding: 10px 16px;
    }

    .btn-lg {
        min-height: 52px;
        padding: 16px 24px;
    }
}

/* Responsive Tables */
@media (max-width: 768px) {
    .table-responsive {
        border: 0;
    }

    .table-responsive table {
        display: block;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    /* Stack Table on Mobile */
    .table-mobile-stack thead {
        display: none;
    }

    .table-mobile-stack tbody,
    .table-mobile-stack tr,
    .table-mobile-stack td {
        display: block;
        width: 100%;
    }

    .table-mobile-stack tr {
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
    }

    .table-mobile-stack td {
        text-align: right;
        padding-left: 50%;
        position: relative;
        border: none;
    }

    .table-mobile-stack td::before {
        content: attr(data-label);
        position: absolute;
        left: 0;
        width: 45%;
        padding-left: 1rem;
        font-weight: bold;
        text-align: left;
    }
}

/* Mobile Navigation */
@media (max-width: 991px) {
    .navbar-collapse {
        max-height: 80vh;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }

    .navbar-nav {
        padding: 1rem 0;
    }

    .navbar-nav .nav-link {
        padding: 12px 16px;
        font-size: 16px;
    }
}

/* Mobile Modals */
@media (max-width: 576px) {
    .modal-dialog {
        margin: 0.5rem;
        max-width: calc(100% - 1rem);
    }

    .modal-fullscreen-sm-down {
        width: 100vw;
        max-width: none;
        height: 100%;
        margin: 0;
    }

    .modal-fullscreen-sm-down .modal-content {
        height: 100%;
        border: 0;
        border-radius: 0;
    }
}

/* Mobile Forms */
@media (max-width: 768px) {

    .form-control,
    .form-select {
        font-size: 16px;
        /* Prevents iOS zoom on focus */
        min-height: 44px;
    }

    .form-label {
        font-size: 14px;
        font-weight: 600;
    }
}

/* Touch-Friendly Cards */
.card {
    -webkit-tap-highlight-color: transparent;
}

.card-clickable {
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card-clickable:active {
    transform: scale(0.98);
}

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
