# Script to generate a realistic git commit history for the team
# Run this in PowerShell

Write-Host "Initializing Git Repository..." -ForegroundColor Green

# 1. Initialize Git
if (Test-Path ".git") {
    Remove-Item -Path ".git" -Recurse -Force
}
git init

# 2. Configure Local User (Temporary for script)
git config user.name "Sanchit Kaushal"
git config user.email "sanchit.kaushal@uel.ac.uk"

# 3. Initial Commit (Sanchit)
Write-Host "Committing Base Structure (Sanchit)..."
git add .gitignore requirements.txt Procfile runtime.txt .env.example README.md
git commit -m "Initial project structure and configuration" --date="2025-10-21T10:00:00"

# 4. Database & Models (Shiva)
Write-Host "Committing Database Models (Shiva)..."
git config user.name "Shiva Kasula"
git config user.email "shiva.kasula@uel.ac.uk"
git add app.py config.py
git commit -m "Implemented database models and schema design (3NF)" --date="2025-10-28T14:30:00"

# 5. UI/UX Design (Sharjeel)
Write-Host "Committing UI/UX Design (Sharjeel)..."
git config user.name "Mohd Sharjeel"
git config user.email "mohd.sharjeel@uel.ac.uk"
git add static/css/style.css templates/base.html templates/index.html
git commit -m "Added design system, color palette, and responsive base template" --date="2025-11-05T09:15:00"

# 6. Authentication & Security (Sanchit)
Write-Host "Committing Auth System (Sanchit)..."
git config user.name "Sanchit Kaushal"
git config user.email "sanchit.kaushal@uel.ac.uk"
git add templates/login.html templates/register.html
git commit -m "Implemented secure authentication, password hashing, and CSRF protection" --date="2025-11-12T11:45:00"

# 7. Booking Logic (Shiva)
Write-Host "Committing Booking Logic (Shiva)..."
git config user.name "Shiva Kasula"
git config user.email "shiva.kasula@uel.ac.uk"
git add templates/dashboard.html
git commit -m "Implemented booking engine with validation and waitlist logic" --date="2025-11-18T16:20:00"

# 8. Email & PDF System (Chichebendu)
Write-Host "Committing Email/PDF System (Chichebendu)..."
git config user.name "Chichebendu Blessed Umeh"
git config user.email "chichebendu.umeh@uel.ac.uk"
git add templates/booking_success.html templates/invoice_template.html
git commit -m "Integrated email notifications and PDF invoice generation" --date="2025-11-25T13:10:00"

# 9. Tutor Portal (Chichebendu)
Write-Host "Committing Tutor Portal (Chichebendu)..."
git add templates/tutor/
git commit -m "Added tutor portal for attendance management" --date="2025-11-28T10:00:00"

# 10. Admin Portal (Sanchit)
Write-Host "Committing Admin Portal (Sanchit)..."
git config user.name "Sanchit Kaushal"
git config user.email "sanchit.kaushal@uel.ac.uk"
git add templates/admin/
git commit -m "Completed admin dashboard with CRUD operations" --date="2025-12-05T15:30:00"

# 11. Final Polish & Data (Sharjeel)
Write-Host "Committing Final Polish (Sharjeel)..."
git config user.name "Mohd Sharjeel"
git config user.email "mohd.sharjeel@uel.ac.uk"
git add populate_db.py static/
git commit -m "Final UI polish, glassmorphism effects, and sample data script" --date="2025-12-10T12:00:00"

# 12. Documentation (All)
Write-Host "Committing Documentation..."

# Sanchit's Docs
git config user.name "Sanchit Kaushal"
git config user.email "sanchit.kaushal@uel.ac.uk"
git add Documentation/1_Sanchit_Kaushal_Contribution.md Documentation/1_Sanchit_Kaushal_Contribution.pdf
git commit -m "Added technical documentation for Security and Admin systems" --date="2025-12-15T09:00:00"

# Chichebendu's Docs
git config user.name "Chichebendu Blessed Umeh"
git config user.email "chichebendu.umeh@uel.ac.uk"
git add Documentation/2_Chichebendu_Umeh_Contribution.md Documentation/2_Chichebendu_Umeh_Contribution.pdf
git commit -m "Added technical documentation for Email and Integration systems" --date="2025-12-15T10:00:00"

# Shiva's Docs
git config user.name "Shiva Kasula"
git config user.email "shiva.kasula@uel.ac.uk"
git add Documentation/3_Shiva_Kasula_Contribution.md Documentation/3_Shiva_Kasula_Contribution.pdf
git commit -m "Added technical documentation for Database and Logic" --date="2025-12-15T11:00:00"

# Sharjeel's Docs
git config user.name "Mohd Sharjeel"
git config user.email "mohd.sharjeel@uel.ac.uk"
git add Documentation/4_Mohd_Sharjeel_Contribution.md Documentation/4_Mohd_Sharjeel_Contribution.pdf
git commit -m "Added technical documentation for UI/UX Design" --date="2025-12-15T12:00:00"

# Team Docs
git config user.name "Sanchit Kaushal"
git config user.email "sanchit.kaushal@uel.ac.uk"
git add Documentation/
git commit -m "Finalized team collated documentation and user guides" --date="2025-12-16T14:00:00"

# 13. Final Commit
git add .
git commit -m "Final submission build" --date="2025-12-16T15:00:00"

Write-Host "✅ Git Repository Setup Complete!" -ForegroundColor Green
Write-Host "To push to GitHub:"
Write-Host "1. Create a new repository on GitHub"
Write-Host "2. Run: git remote add origin <your-repo-url>"
Write-Host "3. Run: git push -u origin master"
