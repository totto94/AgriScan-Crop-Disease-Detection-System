from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_cors import CORS
import json
import os
import hashlib
from datetime import datetime
from functools import wraps
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATA_FILE = 'data/users.json'

# ==================== DATA HELPERS ====================

def init_data():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({
                "users": [
                    {
                        "id": 1,
                        "fullName": "Admin User",
                        "email": "admin@agriscan.com",
                        "password": "admin123",
                        "userType": "admin",
                        "location": "Nairobi",
                        "createdAt": "2025-01-01",
                        "diagnoses": []
                    }
                ]
            }, f, indent=2)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== DECORATORS ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'admin':
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== FARMER ROUTES ====================

@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('user_type') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('farmer_dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        password = request.form.get('password')
        location = request.form.get('location')
        
        if not all([full_name, email, password]):
            flash('All fields are required', 'danger')
            return render_template('signup.html')
        
        data = load_data()
        
        for user in data['users']:
            if user['email'] == email:
                flash('Email already registered. Please login.', 'warning')
                return render_template('signup.html')
        
        new_user = {
            "id": len(data['users']) + 1,
            "fullName": full_name,
            "email": email,
            "password": password,
            "userType": "farmer",
            "location": location or "Not specified",
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "diagnoses": []
        }
        data['users'].append(new_user)
        save_data(data)
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        data = load_data()
        user = None
        for u in data['users']:
            if u['email'] == email and u['password'] == password:
                user = u
                break
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['fullName']
            session['user_type'] = user['userType']
            session['user_email'] = user['email']
            
            if user['userType'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('farmer_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/farmer/dashboard')
@login_required
def farmer_dashboard():
    data = load_data()
    user = None
    for u in data['users']:
        if u['id'] == session['user_id']:
            user = u
            break
    
    total_diagnoses = len(user.get('diagnoses', [])) if user else 0
    
    return render_template('dashboard.html', 
        user=user,
        total_diagnoses=total_diagnoses
    )

@app.route('/farmer/diagnosis', methods=['GET', 'POST'])
@login_required
def diagnosis():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image selected', 'danger')
            return redirect(url_for('diagnosis'))
        
        file = request.files['image']
        if file.filename == '':
            flash('No image selected', 'danger')
            return redirect(url_for('diagnosis'))
        
        if file:
            import random
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            diseases = [
                {"name": "Early Blight", "treatment": "Apply copper-based fungicides. Remove infected leaves."},
                {"name": "Late Blight", "treatment": "Apply mancozeb fungicides. Remove infected plants."},
                {"name": "Leaf Mold", "treatment": "Reduce humidity. Apply sulfur-based fungicides."},
                {"name": "Septoria Leaf Spot", "treatment": "Remove infected leaves. Improve air circulation."},
                {"name": "Bacterial Spot", "treatment": "Remove infected leaves. Avoid wetting foliage."},
                {"name": "Healthy", "treatment": "Plant is healthy. Continue good agricultural practices."}
            ]
            result = random.choice(diseases)
            confidence = 80 + random.randint(0, 19)
            
            data = load_data()
            for user in data['users']:
                if user['id'] == session['user_id']:
                    diagnosis_entry = {
                        "id": len(user.get('diagnoses', [])) + 1,
                        "diseaseName": result['name'],
                        "confidence": confidence,
                        "treatment": result['treatment'],
                        "imagePath": f"/static/uploads/{filename}",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    if 'diagnoses' not in user:
                        user['diagnoses'] = []
                    user['diagnoses'].append(diagnosis_entry)
                    break
            save_data(data)
            
            return render_template('diagnosis_result.html', 
                disease=result['name'],
                confidence=confidence,
                treatment=result['treatment'],
                image_path=f"/static/uploads/{filename}"
            )
    
    return render_template('diagnosis.html')

@app.route('/farmer/history')
@login_required
def history():
    data = load_data()
    user = None
    for u in data['users']:
        if u['id'] == session['user_id']:
            user = u
            break
    
    diagnoses = user.get('diagnoses', []) if user else []
    
    return render_template('history.html', diagnoses=diagnoses)

# ==================== CHATBOT ====================

@app.route('/farmer/chatbot')
@login_required
def farmer_chatbot():
    return render_template('chatbot.html', user_name=session.get('user_name'))

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    message = request.json.get('message', '')
    response = get_chat_response(message)
    return jsonify({'response': response})

def get_chat_response(message):
    lower = message.lower()
    
    if any(word in lower for word in ['early blight', 'tomato']):
        return "🍅 Tomato Early Blight:\n\nSymptoms: Brown spots with concentric rings on leaves.\n\nTreatment: Apply copper-based fungicides. Remove infected leaves."
    
    if any(word in lower for word in ['late blight', 'potato']):
        return "🥔 Potato Late Blight:\n\nSymptoms: Water-soaked lesions with white fuzzy growth.\n\nTreatment: Apply mancozeb fungicides. Remove infected plants."
    
    if any(word in lower for word in ['hello', 'hi', 'hey']):
        return "👋 Hello! I'm your AI farming assistant. Ask me about crop diseases, treatments, or farming tips!"
    
    if any(word in lower for word in ['thanks', 'thank you']):
        return "😊 You're welcome! Happy farming 🌱"
    
    return "🌱 I'm your farming assistant. I can help with disease identification, treatment recommendations, and farming best practices. What would you like to know?"

# ==================== EXPERTS & APPOINTMENTS ====================

@app.route('/farmer/experts')
@login_required
def farmer_experts():
    experts = get_experts_data()
    return render_template('experts.html', experts=experts)

@app.route('/farmer/expert/<int:expert_id>')
@login_required
def expert_detail(expert_id):
    experts = get_experts_data()
    expert = next((e for e in experts if e['id'] == expert_id), None)
    if not expert:
        flash('Expert not found', 'danger')
        return redirect(url_for('farmer_experts'))
    
    time_slots = get_available_slots(expert_id)
    return render_template('expert_detail.html', expert=expert, slots=time_slots)

@app.route('/farmer/book_appointment', methods=['POST'])
@login_required
def book_appointment():
    expert_id = request.form.get('expert_id')
    date = request.form.get('date')
    time = request.form.get('time')
    notes = request.form.get('notes', '')
    
    data = load_data()
    
    appointment = {
        "id": len(data.get('appointments', [])) + 1,
        "farmer_id": session['user_id'],
        "farmer_name": session.get('user_name'),
        "expert_id": int(expert_id),
        "date": date,
        "time": time,
        "notes": notes,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    if 'appointments' not in data:
        data['appointments'] = []
    data['appointments'].append(appointment)
    save_data(data)
    
    flash('Appointment booked successfully! The expert will confirm shortly.', 'success')
    return redirect(url_for('farmer_appointments'))

@app.route('/farmer/appointments')
@login_required
def farmer_appointments():
    data = load_data()
    appointments = data.get('appointments', [])
    user_appointments = [a for a in appointments if a['farmer_id'] == session['user_id']]
    return render_template('appointments.html', appointments=user_appointments)

def get_experts_data():
    return [
        {"id": 1, "name": "Dr. Jane Muthoni", "title": "Senior Agricultural Extension Officer", 
         "county": "Kiambu", "phone": "0712 345 678", "email": "jane.muthoni@agriculture.go.ke", 
         "specialty": "Crop Diseases", "image": "👩‍🌾", "available": True, "bio": "15+ years experience in crop disease management."},
        {"id": 2, "name": "Mr. Peter Ochieng", "title": "Agricultural Officer", 
         "county": "Nairobi", "phone": "0733 456 789", "email": "peter.ochieng@agriculture.go.ke", 
         "specialty": "Horticulture", "image": "👨‍🌾", "available": True, "bio": "Expert in vegetable and fruit crop production."},
        {"id": 3, "name": "Ms. Grace Wanjiru", "title": "Plant Health Specialist", 
         "county": "Nakuru", "phone": "0744 567 890", "email": "grace.wanjiru@agriculture.go.ke", 
         "specialty": "Crop Protection", "image": "👩‍🌾", "available": False, "bio": "Specializes in integrated pest management."}
    ]

def get_available_slots(expert_id):
    slots = []
    days = ['2025-08-15', '2025-08-16', '2025-08-19', '2025-08-20']
    times = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
    for day in days:
        for time in times:
            slots.append({"date": day, "time": time, "available": True})
    return slots[:12]

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        data = load_data()
        user = None
        for u in data['users']:
            if u['email'] == email and u['password'] == password and u.get('userType') == 'admin':
                user = u
                break
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['fullName']
            session['user_type'] = 'admin'
            session['user_email'] = user['email']
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    data = load_data()
    farmers = [u for u in data['users'] if u.get('userType') != 'admin']
    total_farmers = len(farmers)
    total_diagnoses = sum(len(u.get('diagnoses', [])) for u in farmers)
    
    return render_template('admin_dashboard.html',
        total_farmers=total_farmers,
        total_diagnoses=total_diagnoses,
        admin_name=session.get('user_name')
    )

@app.route('/admin/users')
@admin_required
def admin_users():
    data = load_data()
    farmers = [u for u in data['users'] if u.get('userType') != 'admin']
    return render_template('admin_users.html', users=farmers)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    data = load_data()
    data['users'] = [u for u in data['users'] if u['id'] != user_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/admin/diagnoses')
@admin_required
def admin_diagnoses():
    data = load_data()
    all_diagnoses = []
    for user in data['users']:
        if user.get('userType') != 'admin':
            for diag in user.get('diagnoses', []):
                diag['farmerName'] = user['fullName']
                all_diagnoses.append(diag)
    all_diagnoses.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return render_template('admin_diagnoses.html', diagnoses=all_diagnoses)

@app.route('/admin/chatbot')
@admin_required
def admin_chatbot():
    return render_template('admin_chatbot.html')

# ==================== MAIN ====================

if __name__ == '__main__':
    init_data()
    app.run(debug=True, host='0.0.0.0', port=5000)