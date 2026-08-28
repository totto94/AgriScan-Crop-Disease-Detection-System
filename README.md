# 🌿 AgriScan - AI-Powered Crop Disease Detection System

## 📖 Overview
AgriScan is an AI-powered web application that helps smallholder farmers detect crop diseases early by uploading photos of their plants. It provides instant diagnosis, treatment recommendations, and connects farmers with agricultural experts.

## 🚀 Features
- **Disease Diagnosis**: Upload crop leaf images and get instant diagnosis with confidence scores
- **AI Chatbot**: Get answers to farming-related questions
- **Expert Directory**: Find and connect with agricultural extension officers
- **Appointment Booking**: Schedule consultations with experts
- **Diagnosis History**: View all past diagnoses
- **Admin Dashboard**: Manage users and view all diagnoses
- **GPS Location**: Capture farmer location for disease mapping

## 🛠️ Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: JSON (lightweight storage)
- **Templating**: Jinja2

## 📁 Project Structure
AgriScan-Web-Admin/
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── data/
│ └── users.json # User database
├── static/
│ ├── css/
│ │ └── style.css # Custom styles
│ └── js/
│ └── script.js # JavaScript
└── templates/
├── base.html # Base template
├── login.html # Login page
├── signup.html # Signup page
├── dashboard.html # Farmer dashboard
├── diagnosis.html # Diagnosis page
├── chatbot.html # AI Chatbot
├── experts.html # Expert directory
├── appointments.html # Appointment booking
├── admin_login.html # Admin login
├── admin_dashboard.html # Admin dashboard
├── admin_users.html # Admin users
└── admin_diagnoses.html # Admin diagnoses

## 🔧 How to Run the Application

### Prerequisites
- Python 3.8 or higher
- Flask 2.3.3

### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/AgriScan-Crop-Disease-Detection.git

# Navigate to project directory
cd AgriScan-Crop-Disease-Detection

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
Default Admin Credentials

    Email: admin@agriscan.com

    Password: admin123

📊 API Endpoints
Authentication

    GET / - Home page (redirects to login)

    GET /login - Login page

    POST /login - Process login

    GET /signup - Signup page

    POST /signup - Process signup

    GET /logout - Logout

Farmer Features

    GET /farmer/dashboard - Farmer dashboard

    GET /farmer/diagnosis - Diagnosis page

    POST /farmer/diagnosis - Process diagnosis

    GET /farmer/history - Diagnosis history

    GET /farmer/chatbot - Chatbot interface

    GET /farmer/experts - Expert directory

    GET /farmer/expert/<id> - Expert details

    POST /farmer/book_appointment - Book appointment

    GET /farmer/appointments - View appointments

Admin Features

    GET /admin/login - Admin login

    POST /admin/login - Process admin login

    GET /admin/dashboard - Admin dashboard

    GET /admin/users - Manage users

    POST /admin/delete_user/<id> - Delete user

    GET /admin/diagnoses - View all diagnoses

API

    POST /api/chat - Chatbot API endpoint

👤 User Roles

    Farmer: Upload images, view diagnoses, chatbot, expert directory, appointment booking

    Admin: Manage users, view all diagnoses, system monitoring

📊 Database Schema
Users Table (JSON)
json

{
    "users": [
        {
            "id": 1,
            "fullName": "Admin User",
            "email": "admin@agriscan.com",
            "password": "admin123",
            "userType": "admin",
            "location": "Nairobi",
            "latitude": "-1.286389",
            "longitude": "36.817223",
            "createdAt": "2025-01-01",
            "diagnoses": []
        }
    ]
}

Diagnoses

Each user has a diagnoses array containing:
json

{
    "id": 1,
    "diseaseName": "Early Blight",
    "confidence": 85,
    "treatment": "Apply copper-based fungicides...",
    "timestamp": "2025-01-01 10:00"
}

Appointments
json

{
    "appointments": [
        {
            "id": 1,
            "farmer_id": 2,
            "farmer_name": "John Farmer",
            "expert_id": 1,
            "date": "2025-08-15",
            "time": "10:00",
            "notes": "Tomato disease",
            "status": "pending",
            "created_at": "2025-08-10 09:00"
        }
    ]
}

🌍 SDG Alignment

    SDG 1 (No Poverty): Secure farmers' incomes

    SDG 2 (Zero Hunger): Increase agricultural productivity

    SDG 4 (Quality Education): Digital skills for farmers

    SDG 12 (Responsible Consumption): Sustainable farming

📝 License

This project is for academic purposes.
👨‍💻 Author

Jessy Tibi - United States International University
🙏 Acknowledgements

    Supervisor: Dr.Stanley Githinji

    United States International University

# Open browser and go to http://localhost:5000

