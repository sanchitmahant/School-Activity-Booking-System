# Stylesheet: loading-states.css

## 1. Executive Summary
Controls the visual presentation, formatting, and layout of the HTML documents.

## 2. Code Logic & Functionality
Defines CSS classes and ID selectors. Sets properties such as color, font-family, margin, and padding to create a responsive and cohesive visual design.

## 3. Key Concepts & Definitions
- **CSS3**: Cascading Style Sheets Level 3.
- **Responsive Design**: Web design approach that makes web pages render well on a variety of devices and window or screen sizes.
- **Selector**: The part of a CSS rule that describes the elements to be styled.

## 4. Location Details
**Path**: `static\css\loading-states.css`
**Type**: .CSS File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```css
/**
 * Loading States & Animations
 * Professional loading indicators and progress feedback
 */

/* Global Loading Overlay */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 46, 93, 0.95);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.loading-overlay.active {
    display: flex;
}

/* Spinner Loader */
.spinner-loader {
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-top-color: #0DA49F;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* Three Dots Loader */
.dots-loader {
    display: flex;
    gap: 8px;
}

.dots-loader div {
    width: 12px;
    height: 12px;
    background: #0DA49F;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;
}

.dots-loader div:nth-child(1) {
    animation-delay: -0.32s;
}

.dots-loader div:nth-child(2) {
    animation-delay: -0.16s;
}

@keyframes bounce {

    0%,
    80%,
    100% {
        transform: scale(0);
    }

    40% {
        transform: scale(1);
    }
}

/* Skeleton Loading */
.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s ease-in-out infinite;
    border-radius: 4px;
}

.skeleton-text {
    height: 16px;
    margin-bottom: 8px;
}

.skeleton-heading {
    height: 24px;
    width: 60%;
    margin-bottom: 16px;
}

.skeleton-card {
    height: 200px;
    border-radius: 12px;
}

@keyframes skeleton-loading {
    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }
}

/* Progress Bar */
.loading-progress {
    width: 100%;
    height: 4px;
    background: #e0e0e0;
    border-radius: 2px;
    overflow: hidden;
    position: relative;
}

.loading-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #0DA49F, #0CB3A7);
    width: 0%;
    transition: width 0.3s ease;
    animation: progress-indeterminate 1.5s infinite linear;
}

@keyframes progress-indeterminate {
    0% {
        width: 0%;
        margin-left: 0%;
    }

    50% {
        width: 50%;
        margin-left: 25%;
    }

    100% {
        width: 0%;
        margin-left: 100%;
    }
}

/* Button Loading State */
.btn-loading {
    position: relative;
    pointer-events: none;
    opacity: 0.7;
}


... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
