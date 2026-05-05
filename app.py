from flask import Flask, request, jsonify
from flask import session
from flask_cors import CORS
import uuid
from datetime import datetime, timedelta
import sqlite3
import re



app = Flask(__name__)
app.secret_key = "secret123"
from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=7)
CORS(app,supports_credentials=True)

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("users.db")

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
  ''')
# OPPORTUNITIES TABLE
    conn.execute('''
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_email TEXT,
            name TEXT,
            category TEXT,
            duration TEXT,
            start_date TEXT,
            description TEXT,
            skills TEXT,
            future_opportunities TEXT,
            max_applicants INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 🔥 add new columns if they don't exist
    try:
        conn.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    except:
        pass

    try:
        conn.execute("ALTER TABLE users ADD COLUMN token_expiry TEXT")
    except:
        pass

    try:
        conn.execute("ALTER TABLE opportunities ADD COLUMN skills TEXT")
    except:
        pass

    try:
        conn.execute("ALTER TABLE opportunities ADD COLUMN future_opportunities TEXT")
    except:
        pass

    try:
        conn.execute("ALTER TABLE opportunities ADD COLUMN max_applicants INTEGER")
    except:
        pass

    try:
        conn.execute("ALTER TABLE opportunities ADD COLUMN created_at TEXT")
    except:
        pass

    conn.close()
    

init_db()


# ---------- EMAIL VALIDATION ----------
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


# ---------- SIGNUP ----------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    fullname = data.get("fullname")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    # validations
    if not fullname or not email or not password or not confirm_password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400

    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters"}), 400

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match"}), 400

    conn = get_db()

    # check existing user
    existing = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"success": False, "message": "Account already exists"}), 400

    # insert user
    conn.execute(
        "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
        (fullname, email, password)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Signup successful"
    })


# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")
    remember = data.get("rememberMe", False)

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()
    conn.close()

    if user:
        session['user'] = email

        # 🔥 Remember Me logic
        if remember:
            session.permanent = True   # long session
        else:
            session.permanent = False  # ends when browser closes

        return jsonify({
            "success": True,
            "message": "Login successful"
        })

    return jsonify({
        "success": False,
        "message": "Invalid email or password"
    }), 401

@app.route('/check-session', methods=['GET'])
def check_session():
    if 'user' in session:
        return jsonify({
            "loggedIn": True,
            "email": session['user']
        })
    return jsonify({
        "loggedIn": False
    })

# ---------- DASHBOARD ----------
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    return jsonify({
        "success": True,
        "data": {
            "message": "Welcome to dashboard"
        }
    })

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True, "message": "Logged out successfully"})

# forgot password api#

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get("email")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    if user:
        token = str(uuid.uuid4())
        expiry = datetime.now() + timedelta(hours=1)

        conn.execute(
            "UPDATE users SET reset_token=?, token_expiry=? WHERE email=?",
            (token, expiry.isoformat(), email)   # ✅ important
        )
        conn.commit()

        print(f"Reset link: http://127.0.0.1:5500/sky/reset.html?token={token}")

    conn.close()

    return jsonify({
        "success": True,
        "message": "If the email exists, a reset link has been sent"
    })

# reset password api#
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("password")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE reset_token=?",
        (token,)
    ).fetchone()

    if not user:
        return jsonify({"success": False, "message": "Invalid or expired link"}), 400

    expiry = datetime.fromisoformat(user[5])

    if datetime.now() > expiry:
        return jsonify({"success": False, "message": "Link expired"}), 400
    
    if len(new_password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters"}), 400
    conn.execute(
        "UPDATE users SET password=?, reset_token=NULL, token_expiry=NULL WHERE reset_token=?",
        (new_password, token)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Password reset successful"})

#get opportunities api#
@app.route('/create-opportunity', methods=['POST'])
def create_opportunity():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json or {}
    name = (data.get('name') or '').strip()
    category = (data.get('category') or '').strip()
    duration = (data.get('duration') or '').strip()
    start_date = (data.get('start_date') or '').strip()
    description = (data.get('description') or '').strip()
    skills = data.get('skills', [])
    future_opportunities = (data.get('future_opportunities') or '').strip()
    max_applicants = data.get('max_applicants')

    
    if not name or not category or not duration or not start_date or not description or not future_opportunities:
        return jsonify({"success": False, "message": "All required opportunity fields must be provided"}), 400

    raw_skills = skills if isinstance(skills, list) else [s.strip() for s in str(skills or '').split(',')]
    if not any(s.strip() for s in raw_skills):
        return jsonify({"success": False, "message": "Skills to Gain is required"}), 400

    category_map = {
        'technology': 'Technology',
        'business': 'Business',
        'design': 'Design',
        'marketing': 'Marketing',
        'data science': 'Data Science',
        'data': 'Data Science',
        'other': 'Other'
    }
    normalized_category = category.strip().lower()
    if normalized_category not in category_map:
        return jsonify({"success": False, "message": "Invalid opportunity category"}), 400
    category = category_map[normalized_category]

    if isinstance(skills, list):
        skills = ','.join([s.strip() for s in skills if s and s.strip()])
    else:
        skills = str(skills or '').strip()

    try:
        max_applicants = int(max_applicants) if max_applicants not in (None, '') else 0
    except ValueError:
        max_applicants = 0

    email = session['user']
    conn = get_db()
    conn.execute(
        "INSERT INTO opportunities (admin_email, name, category, duration, start_date, description, skills, future_opportunities, max_applicants) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (email, name, category, duration, start_date, description, skills, future_opportunities, max_applicants)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Opportunity created successfully"}), 201

@app.route('/update-opportunity/<int:opportunity_id>', methods=['PUT'])
def update_opportunity(opportunity_id):
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json or {}
    name = (data.get('name') or '').strip()
    category = (data.get('category') or '').strip()
    duration = (data.get('duration') or '').strip()
    start_date = (data.get('start_date') or '').strip()
    description = (data.get('description') or '').strip()
    skills = data.get('skills', [])
    future_opportunities = (data.get('future_opportunities') or '').strip()
    max_applicants = data.get('max_applicants')

    if not name or not category or not duration or not start_date or not description or not future_opportunities:
        return jsonify({"success": False, "message": "All required opportunity fields must be provided"}), 400

    raw_skills = skills if isinstance(skills, list) else [s.strip() for s in str(skills or '').split(',')]
    if not any(s.strip() for s in raw_skills):
        return jsonify({"success": False, "message": "Skills to Gain is required"}), 400
    
    category_map = {
        'technology': 'Technology',
        'business': 'Business',
        'design': 'Design',
        'marketing': 'Marketing',
        'data science': 'Data Science',
        'data': 'Data Science',
        'other': 'Other'
    }
    normalized_category = category.strip().lower()
    if normalized_category not in category_map:
        return jsonify({"success": False, "message": "Invalid opportunity category"}), 400
    category = category_map[normalized_category]

    if isinstance(skills, list):
        skills = ','.join([s.strip() for s in skills if s and s.strip()])
    else:
        skills = str(skills or '').strip()

    try:
        max_applicants = int(max_applicants) if max_applicants not in (None, '') else 0
    except ValueError:
        max_applicants = 0

    email = session['user']
    conn = get_db()
    cursor = conn.execute(
        "UPDATE opportunities SET name=?, category=?, duration=?, start_date=?, description=?, skills=?, future_opportunities=?, max_applicants=? WHERE id=? AND admin_email=?",
        (name, category, duration, start_date, description, skills, future_opportunities, max_applicants, opportunity_id, email)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated == 0:
        return jsonify({"success": False, "message": "Opportunity not found or access denied"}), 404

    return jsonify({"success": True, "message": "Opportunity updated successfully"})

@app.route('/delete-opportunity/<int:opportunity_id>', methods=['DELETE'])
def delete_opportunity(opportunity_id):
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    email = session['user']
    conn = get_db()
    cursor = conn.execute(
        "DELETE FROM opportunities WHERE id=? AND admin_email=?",
        (opportunity_id, email)
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"success": False, "message": "Opportunity not found or access denied"}), 404

    return jsonify({"success": True, "message": "Opportunity deleted successfully"})

@app.route('/get-opportunities', methods=['GET'])
def get_opportunities():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    email = session['user']

    conn = get_db()
    rows = conn.execute(
        "SELECT id, name, category, duration, start_date, description, skills, future_opportunities, max_applicants FROM opportunities WHERE admin_email=? ORDER BY created_at DESC",
        (email,)
    ).fetchall()
    conn.close()

    data = []
    for row in rows:
        skills = row[6] or ''
        data.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "duration": row[3],
            "start_date": row[4],
            "description": row[5],
            "skills": [s.strip() for s in skills.split(',') if s.strip()] if skills else [],
            "future_opportunities": row[7] or '',
            "max_applicants": row[8] or 0
        })

    return jsonify({
        "success": True,
        "data": data
    })

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)