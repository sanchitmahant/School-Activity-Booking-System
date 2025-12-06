# Stylesheet: style.css

## 1. Executive Summary
Controls the visual presentation, formatting, and layout of the HTML documents.

## 2. Code Logic & Functionality
Defines CSS classes and ID selectors. Sets properties such as color, font-family, margin, and padding to create a responsive and cohesive visual design.

## 3. Key Concepts & Definitions
- **CSS3**: Cascading Style Sheets Level 3.
- **Responsive Design**: Web design approach that makes web pages render well on a variety of devices and window or screen sizes.
- **Selector**: The part of a CSS rule that describes the elements to be styled.

## 4. Location Details
**Path**: `static\css\style.css`
**Type**: .CSS File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```css
/* 
   Greenwood International School - Modern Academic Theme
   Inspiration: University of East London (UEL)
   Palette: Blue Chill (#0DA49F), Deep Navy (#002E5D), Clean White
*/

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');

:root {
    /* UEL Inspired Palette */
    --primary-blue: #002E5D;
    /* Deep Navy - Authority */
    --accent-teal: #0DA49F;
    /* Blue Chill - Modernity */
    --accent-gold: #D4AF37;
    /* Subtle Gold for prestige */

    /* Backgrounds */
    --bg-body: #FFFFFF;
    --bg-light: #F8F9FA;
    --bg-dark: #002E5D;

    /* Text */
    --text-main: #212529;
    --text-muted: #6c757d;
    --text-light: #FFFFFF;

    /* Typography */
    --font-heading: 'Inter', sans-serif;
    --font-body: 'Roboto', sans-serif;

    /* Components */
    --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    --hover-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    --border-radius: 8px;
}

body {
    background-color: var(--bg-body);
    color: var(--text-main);
    font-family: var(--font-body);
    line-height: 1.6;
    overflow-x: hidden;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    font-family: var(--font-heading);
    color: var(--primary-blue);
    font-weight: 700;
    letter-spacing: -0.5px;
}

a {
    color: var(--primary-blue);
    text-decoration: none;
    transition: all 0.3s ease;
}

a:hover {
    color: var(--accent-teal);
}

/* --- Navigation --- */
.navbar {
    background: #FFFFFF !important;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
    padding: 1rem 0;
}

.navbar-brand {
    font-family: var(--font-heading);
    font-weight: 800;
    font-size: 1.8rem;
    color: var(--primary-blue) !important;
    letter-spacing: -1px;
}

.nav-link {
    color: var(--text-main) !important;
    font-weight: 500;
    font-size: 0.95rem;
    margin-left: 1.5rem;
    position: relative;
}

.nav-link::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: -5px;
    left: 0;
    background-color: var(--accent-teal);
    transition: width 0.3s ease;
}

.nav-link:hover::after {
    width: 100%;
}

.nav-link.active {
    color: var(--accent-teal) !important;
}

/* --- Hero Section --- */
.hero-section {
    position: relative;
    height: 85vh;
    display: flex;
    align-items: center;
    background: linear-gradient(rgba(0, 46, 93, 0.7), rgba(0, 46, 93, 0.5)),
        url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
    background-size: cover;
    background-position: center;
    color: white;
    clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%);
}

.hero-content {
    max-width: 800px;
}

.hero-title {
    font-size: 4.5rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    color: #FFFFFF;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 1.5rem;
    font-weight: 300;
    margin-bottom: 2.5rem;
    opacity: 0.9;
}

.btn-primary-custom {
    background-color: var(--accent-teal);
    border: none;
    padding: 15px 40px;
    font-weight: 600;
    border-radius: 50px;
    color: white;
    transition: transform 0.3s ease, box-shadow 0.3s ease;

... [Code Truncated for Documentation Readability - See Source File for Complete Logic] ...
```
