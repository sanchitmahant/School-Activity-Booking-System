# Stylesheet: tutor_modal.css

## 1. Executive Summary
Controls the visual presentation, formatting, and layout of the HTML documents.

## 2. Code Logic & Functionality
Defines CSS classes and ID selectors. Sets properties such as color, font-family, margin, and padding to create a responsive and cohesive visual design.

## 3. Key Concepts & Definitions
- **CSS3**: Cascading Style Sheets Level 3.
- **Responsive Design**: Web design approach that makes web pages render well on a variety of devices and window or screen sizes.
- **Selector**: The part of a CSS rule that describes the elements to be styled.

## 4. Location Details
**Path**: `static\css\tutor_modal.css`
**Type**: .CSS File

## 5. Source Code Preview (Snippet)

Running typical software analysis on this file:

```css
/* =======================
   TUTOR PROFILE Modal - Professional Enhancement
   ======================= */

/* Tutor Modal - Larger, readable text */
#tutorProfileModal .modal-body {
    padding: 2rem;
}

#tutorProfileModal h5 {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--primary-blue);
}

#tutorProfileModal h6 {
    font-size: 1.1rem;
    font-weight: 600;
}

/* Bio and Philosophy - Larger text */
#tutorProfileBio,
#tutorProfilePhilosophy {
    font-size: 15px !important;
    line-height: 1.7 !important;
    color: var(--text-main) !important;
}

/* Education and Certifications - Readable size */
#tutorProfileEducation,
#tutorProfileCertifications {
    font-size: 14px !important;
    line-height: 1.6 !important;
}

/* Experience display */
#tutorProfileExperience {
    font-size: 24px;
    font-weight: 700;
    color: var(--accent-teal);
}

/* Modal spacing improvements */
#tutorProfileModal .mb-3 {
    margin-bottom: 1.5rem !important;
}

#tutorProfileModal .bg-light {
    background-color: #f8f9fa !important;
    padding: 1.25rem !important;
}

/* Hide LinkedIn if not available */
#tutorProfileLinkedin.d-none {
    display: none !important;
}
```
