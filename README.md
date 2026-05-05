# Admin Portal – Opportunity Management System

## 📌 Project Overview

This is a full-stack admin portal developed using **Flask (Python backend)** and **HTML, CSS, JavaScript (frontend)**.
It allows administrators to manage opportunities with secure authentication and database integration.

---

## 🚀 Version Information

* **Project Version:** 1.0
* **Python Version:** 3.x
* **Flask Version:** 2.x
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, JavaScript (ES6)

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **API:** REST APIs

---

## 🔐 Features

### Authentication

* Admin Signup & Login
* Email validation & password rules
* Remember Me session support
* Forgot Password with token-based reset (1-hour expiry)

---

### Dashboard

* Admin dashboard with navigation
* Personalized admin profile

---

### Opportunity Management

* Create opportunities
* View only your own opportunities
* Edit opportunities
* Delete opportunities
* Fully database-driven (no hardcoded data)

---

## 📂 Project Structure

Backend/

* app.py

Frontend/

* admin.html
* admin.css
* admin.js
* reset.html

---

## ⚙️ Setup Instructions

1. Clone the repository
2. Navigate to Backend folder
3. Create virtual environment

   ```
   python -m venv venv
   ```
4. Activate virtual environment

   ```
   venv\Scripts\activate
   ```
5. Install dependencies

   ```
   pip install flask flask-cors
   ```
6. Run the server

   ```
   python app.py
   ```
7. Open `admin.html` in browser

---

## 🔗 API Endpoints

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

---

## 📌 Key Highlights

* User-specific data isolation
* Secure session management
* Token-based password reset
* Clean UI with backend integration

---

## 👩‍💻 Author

Trupti G M
