backend-implementation-using-Python-Flask

Admin Portal – Opportunity Management System

Project Overview

This is a full-stack admin portal developed using **Flask (backend)** and **HTML, CSS, JavaScript (frontend)**.
It allows administrators to manage opportunities with secure authentication and database integration.

Features

Authentication

* Admin Signup & Login
* Email validation & password rules
* Remember Me session support
* Forgot Password with secure token (1-hour expiry)

Dashboard

* Admin dashboard with navigation
* Personalized user view

Opportunity Management

* Create new opportunities
* View only your own opportunities
* Edit existing opportunities
* Delete opportunities
* Data stored in SQLite database
* No hardcoded data (fully dynamic)

Tech Stack

Backend:Flask (Python)
Frontend:HTML, CSS, JavaScript
Database:SQLite
API: REST APIs

 Project Structure

Backend/
app.py

Frontend/
* admin.html
* admin.css
* admin.js
* reset.html

Setup Instructions

1. Clone the repository
2. Navigate to Backend folder
3. Create virtual environment
4. Install dependencies

   pip install flask flask-cors
  
5. Run the server

   python app.py

6. Open admin.html in browser

API Endpoints

* POST /signup
* POST /login
* POST /logout
* GET /check-session
* POST /forgot-password
* POST /reset-password
* POST /create-opportunity
* GET /get-opportunities
* PUT /update-opportunity/{id}
* DELETE /delete-opportunity/{id}

Key Highlights

* User-specific data isolation
* Secure session management
* Token-based password reset
* Clean UI (no modifications required)

Author

Trupti G M
