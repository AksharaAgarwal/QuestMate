import os
import json
import sys
import datetime
from io import StringIO
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "questmate_final_rescue_2026"
app.config['JWT_SECRET_KEY'] = "questmate_jwt_secret_2026"
jwt = JWTManager(app)
CORS(app)

# ============================================
# DATABASE SETUP
# ============================================
os.makedirs('../data', exist_ok=True)
USER_DATA = '../data/users.json'
TASKS_DATA = '../data/tasks.json'
MENTORSHIP_DATA = '../data/mentorship.json'

def load_db(filename=USER_DATA):
    if not os.path.exists(filename):
        return {} if filename == USER_DATA else []
    with open(filename, 'r') as f:
        return json.load(f)

def save_db(data, filename=USER_DATA):
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# ============================================
# COMPREHENSIVE SKILL ROADMAPS & TASKS
# ============================================
SKILLS = {
    "Python": {
        "description": "Master Python programming from basics to advanced",
        "icon": "🐍",
        "difficulty_progression": {
            1: "Fundamentals", 2: "Variables", 3: "Conditionals", 
            4: "Loops", 5: "Functions", 6: "Data Structures",
            7: "OOP Basics", 8: "Advanced OOP", 9: "Error Handling", 10: "Mastery"
        }
    },
    "Web Development": {
        "description": "Learn HTML, CSS, JavaScript, and backend development",
        "icon": "🌐",
        "difficulty_progression": {
            1: "HTML Basics", 2: "CSS Styling", 3: "JavaScript",
            4: "DOM Manipulation", 5: "API Calls", 6: "Async/Await",
            7: "Frameworks", 8: "Backend", 9: "Databases", 10: "Full Stack"
        }
    },
    "DSA": {
        "description": "Data Structures and Algorithms for coding interviews",
        "icon": "📊",
        "difficulty_progression": {
            1: "Arrays", 2: "Linked Lists", 3: "Stacks",
            4: "Queues", 5: "Trees", 6: "Graphs",
            7: "Dynamic Programming", 8: "Greedy", 9: "Bit Manipulation", 10: "Mastery"
        }
    },
    "UI/UX": {
        "description": "Design principles, user experience, and interface design",
        "icon": "🎨",
        "difficulty_progression": {
            1: "Design Basics", 2: "Color Theory", 3: "Typography",
            4: "Layout", 5: "Prototyping", 6: "User Research",
            7: "Accessibility", 8: "Animation", 9: "System Design", 10: "Mastery"
        }
    }
}

ROADMAPS = {
    "Python": {
        1: {
            "title": "Hello World",
            "desc": "print('Hello, World!')",
            "expected": "Hello, World!\n",
            "explanation": "Learn how to output text using print()",
            "time_est": "5 min",
            "is_test": False
        },
        2: {
            "title": "Variables & Types",
            "desc": "x = 10\nprint(x)",
            "expected": "10\n",
            "explanation": "Create a variable and display its value",
            "time_est": "10 min",
            "is_test": False
        },
        3: {
            "title": "Arithmetic Operations",
            "desc": "a = 5\nb = 3\nprint(a + b)",
            "expected": "8\n",
            "explanation": "Perform basic math operations",
            "time_est": "10 min",
            "is_test": False
        },
        4: {
            "title": "String Manipulation",
            "desc": "name = 'Python'\nprint('Welcome to ' + name)",
            "expected": "Welcome to Python\n",
            "explanation": "Concatenate strings together",
            "time_est": "10 min",
            "is_test": False
        },
        5: {
            "title": "If-Else Statements",
            "desc": "x = 10\nif x > 5:\n    print('Greater')\nelse:\n    print('Smaller')",
            "expected": "Greater\n",
            "explanation": "Use conditional logic to make decisions",
            "time_est": "15 min",
            "is_test": False
        },
        6: {
            "title": "Loops",
            "desc": "for i in range(3):\n    print(i)",
            "expected": "0\n1\n2\n",
            "explanation": "Repeat code using loops",
            "time_est": "15 min",
            "is_test": False
        },
        7: {
            "title": "MILESTONE TEST 1",
            "desc": "Combine everything: Create a program that prints numbers 1-5",
            "expected": "for i in range(1, 6):\n    print(i)",
            "explanation": "Demonstrate mastery of basics",
            "time_est": "20 min",
            "is_test": True
        },
        8: {
            "title": "Lists & Indexing",
            "desc": "lst = [1, 2, 3]\nprint(lst[0])",
            "expected": "1\n",
            "explanation": "Work with lists and access elements",
            "time_est": "15 min",
            "is_test": False
        },
        9: {
            "title": "Functions",
            "desc": "def greet(name):\n    print('Hello ' + name)\ngreet('QuestMate')",
            "expected": "Hello QuestMate\n",
            "explanation": "Write reusable code with functions",
            "time_est": "20 min",
            "is_test": False
        },
        10: {
            "title": "MILESTONE TEST 2",
            "desc": "Advanced: Write a function that returns the sum of a list",
            "expected": "Advanced topics mastered!",
            "explanation": "Show advanced programming skills",
            "time_est": "30 min",
            "is_test": True
        }
    },
    "Web Development": {
        1: {
            "title": "HTML Basics",
            "desc": "<h1>Welcome to Web Dev</h1>",
            "expected": "<h1>Welcome to Web Dev</h1>\n",
            "explanation": "Create your first heading in HTML",
            "time_est": "10 min",
            "is_test": False
        },
        2: {
            "title": "HTML Forms",
            "desc": "<form><input type='text' placeholder='Enter name'></form>",
            "expected": "<form><input type='text' placeholder='Enter name'></form>\n",
            "explanation": "Build interactive forms",
            "time_est": "15 min",
            "is_test": False
        }
    },
    "DSA": {
        1: {
            "title": "Array Basics",
            "desc": "arr = [1, 2, 3]\nprint(len(arr))",
            "expected": "3\n",
            "explanation": "Understand array fundamentals",
            "time_est": "10 min",
            "is_test": False
        }
    },
    "UI/UX": {
        1: {
            "title": "Design Principles",
            "desc": "Read about 5 core design principles and list them",
            "expected": "Design knowledge acquired",
            "explanation": "Learn foundational design concepts",
            "time_est": "20 min",
            "is_test": False
        }
    }
}

# ============================================
# USER AUTHENTICATION
# ============================================
@app.route('/api/signup', methods=['POST'])
def signup():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    college = data.get('college', 'Default College').strip()
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    db = load_db()
    if username in db:
        return jsonify({"error": "User already exists"}), 409
    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db[username] = {
        "password": hashed,
        "xp": 0,
        "streak": 0,
        "consistency_shields": 1,
        "current_skill": None,
        "levels": {},
        "rank": {},
        "completed_tasks": {},
        "notifications": [],
        "last_login": str(datetime.date.today()),
        "college": college,
        "joined_date": str(datetime.date.today()),
        "shield_paused_until": None,
        "paused_reason": None
    }
    save_db(db)
    
    access_token = create_access_token(identity=username)
    return jsonify({
        "message": "User created successfully",
        "access_token": access_token,
        "user": username
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    db = load_db()
    user = db.get(username)
    
    if not user or not bcrypt.checkpw(password.encode(), user['password'].encode()):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": username
    }), 200

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    username = get_jwt_identity()
    db = load_db()
    user = db.get(username)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_copy = user.copy()
    del user_copy['password']
    return jsonify(user_copy), 200

# ============================================
# DASHBOARD & SKILL MANAGEMENT
# ============================================
@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get available skills"""
    return jsonify(SKILLS), 200

@app.route('/api/skill/<skill>/roadmap', methods=['GET'])
def get_skill_roadmap(skill):
    """Get roadmap for a skill"""
    if skill not in ROADMAPS:
        return jsonify({"error": "Skill not found"}), 404
    
    return jsonify(ROADMAPS[skill]), 200

@app.route('/api/user/select-skill', methods=['POST'])
@jwt_required()
def select_skill():
    """User selects a skill and starting level"""
    username = get_jwt_identity()
    data = request.get_json()
    skill = data.get('skill')
    level = data.get('level', 1)
    
    if skill not in SKILLS:
        return jsonify({"error": "Invalid skill"}), 400
    
    db = load_db()
    user = db[username]
    user['current_skill'] = skill
    user['levels'][skill] = level
    user['rank'][skill] = 1
    user['completed_tasks'][skill] = []
    save_db(db)
    
    return jsonify({"message": "Skill selected", "skill": skill, "level": level}), 200

@app.route('/api/user/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """Get dashboard data"""
    username = get_jwt_identity()
    db = load_db()
    user = db.get(username)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Update streak logic
    today = str(datetime.date.today())
    last_login = user.get('last_login', today)
    days_since = (datetime.date.today() - datetime.datetime.strptime(last_login, '%Y-%m-%d').date()).days
    
    if days_since > 1:
        if user.get('consistency_shields', 0) > 0 and not user.get('shield_paused_until'):
            user['consistency_shields'] -= 1
        else:
            user['streak'] = 0
    
    user['last_login'] = today
    save_db(db)
    
    skill = user.get('current_skill')
    level = user['levels'].get(skill, 1) if skill else 1
    task = ROADMAPS.get(skill, {}).get(level, {})
    
    # Find mentors
    mentors = []
    if skill:
        for name, u in db.items():
            if name != username and u['levels'].get(skill, 0) >= level + 2:
                mentors.append({
                    "name": name,
                    "level": u['levels'].get(skill, 0),
                    "xp": u.get('xp', 0),
                    "college": u.get('college', 'Unknown')
                })
    
    user_copy = user.copy()
    del user_copy['password']
    
    return jsonify({
        "user": user_copy,
        "current_task": task,
        "skill": skill,
        "level": level,
        "mentors": mentors[:5]
    }), 200

# ============================================
# TASK SUBMISSION & XP SYSTEM
# ============================================
@app.route('/api/task/submit', methods=['POST'])
@jwt_required()
def submit_task():
    """Submit code for a task"""
    username = get_jwt_identity()
    data = request.get_json()
    code = data.get('code', '')
    
    db = load_db()
    user = db.get(username)
    
    if not user or not user.get('current_skill'):
        return jsonify({"error": "Please select a skill first"}), 400
    
    skill = user['current_skill']
    level = user['levels'].get(skill, 1)
    task = ROADMAPS.get(skill, {}).get(level)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    # Execute code and test
    buffer = StringIO()
    sys.stdout = buffer
    result = {"success": False, "message": "", "xp_earned": 0}
    
    try:
        exec(code)
        output = buffer.getvalue()
        
        if output == task['expected']:
            xp_earned = 100 if task['is_test'] else 50
            user['xp'] += xp_earned
            user['levels'][skill] += 1
            user['streak'] += 1
            user['completed_tasks'][skill].append(level)
            
            # Award consistency shields every 7-day streak
            if user['streak'] % 7 == 0:
                user['consistency_shields'] += 1
                result['bonus'] = f"Earned consistency shield! Total: {user['consistency_shields']}"
            
            result['success'] = True
            result['message'] = "Quest completed!"
            result['xp_earned'] = xp_earned
            result['new_level'] = user['levels'][skill]
        else:
            result['message'] = f"Output mismatch. Expected: {repr(task['expected'])}, Got: {repr(output)}"
    
    except Exception as e:
        result['message'] = f"Code execution error: {str(e)}"
    
    finally:
        sys.stdout = sys.__stdout__
    
    if result['success']:
        save_db(db)
    
    return jsonify(result), 200 if result['success'] else 400

# ============================================
# CONSISTENCY SHIELD SYSTEM
# ============================================
@app.route('/api/shield/activate', methods=['POST'])
@jwt_required()
def activate_shield():
    """Pause progress with consistency shield during exams/crisis"""
    username = get_jwt_identity()
    data = request.get_json()
    reason = data.get('reason', 'Personal reasons')
    days = int(data.get('days', 7))
    
    if days < 1 or days > 90:
        return jsonify({"error": "Shield duration must be 1-90 days"}), 400
    
    db = load_db()
    user = db[username]
    
    if user.get('consistency_shields', 0) < 1:
        return jsonify({"error": "No consistency shields available"}), 400
    
    user['consistency_shields'] -= 1
    pause_until = datetime.date.today() + datetime.timedelta(days=days)
    user['shield_paused_until'] = str(pause_until)
    user['paused_reason'] = reason
    
    save_db(db)
    
    return jsonify({
        "message": f"Progress paused for {days} days",
        "paused_until": str(pause_until),
        "reason": reason,
        "shields_remaining": user['consistency_shields']
    }), 200

@app.route('/api/shield/resume', methods=['POST'])
@jwt_required()
def resume_progress():
    """Resume progress after shield period"""
    username = get_jwt_identity()
    
    db = load_db()
    user = db[username]
    user['shield_paused_until'] = None
    user['paused_reason'] = None
    user['last_login'] = str(datetime.date.today())
    
    save_db(db)
    
    return jsonify({"message": "Progress resumed!"}), 200

# ============================================
# PEER MENTORSHIP SYSTEM
# ============================================
@app.route('/api/mentors/<skill>', methods=['GET'])
@jwt_required()
def get_mentors(skill):
    """Get available mentors for a skill"""
    username = get_jwt_identity()
    
    db = load_db()
    user = db[username]
    current_level = user['levels'].get(skill, 0)
    
    mentors = []
    for name, u in db.items():
        if (name != username and 
            u['levels'].get(skill, 0) >= current_level + 2 and
            u.get('college') == user.get('college')):
            mentors.append({
                "name": name,
                "level": u['levels'].get(skill, 0),
                "xp": u.get('xp', 0),
                "streak": u.get('streak', 0),
                "can_mentor": True
            })
    
    return jsonify({"mentors": sorted(mentors, key=lambda x: x['level'], reverse=True)}), 200

@app.route('/api/mentorship/request/<mentor_name>', methods=['POST'])
@jwt_required()
def request_mentorship(mentor_name):
    """Send mentorship request to a peer"""
    username = get_jwt_identity()
    data = request.get_json()
    skill = data.get('skill')
    topic = data.get('topic', 'General help')
    
    db = load_db()
    
    if mentor_name not in db:
        return jsonify({"error": "Mentor not found"}), 404
    
    mentorship = load_db(MENTORSHIP_DATA)
    request_id = f"{username}_{mentor_name}_{datetime.datetime.now().timestamp()}"
    
    mentorship[request_id] = {
        "student": username,
        "mentor": mentor_name,
        "skill": skill,
        "topic": topic,
        "created_at": str(datetime.datetime.now()),
        "status": "pending",
        "messages": []
    }
    
    save_db(mentorship, MENTORSHIP_DATA)
    
    return jsonify({
        "message": f"Mentorship request sent to {mentor_name}",
        "request_id": request_id
    }), 201

# ============================================
# LEADERBOARD & RANKINGS
# ============================================
@app.route('/api/leaderboard/<skill>', methods=['GET'])
def get_leaderboard(skill):
    """Get skill-wise leaderboard"""
    db = load_db()
    
    rankings = []
    for username, user in db.items():
        if user['levels'].get(skill, 0) > 0:
            rankings.append({
                "username": username,
                "level": user['levels'].get(skill, 0),
                "xp": user.get('xp', 0),
                "streak": user.get('streak', 0),
                "college": user.get('college', 'Unknown')
            })
    
    rankings.sort(key=lambda x: (x['xp'], x['level']), reverse=True)
    
    return jsonify({
        "skill": skill,
        "leaderboard": rankings[:20]
    }), 200

# ============================================
# SESSION-BASED ROUTES (Traditional HTML)
# ============================================
@app.route('/')
def index():
    if 'user' not in session:
        return render_template('landing.html')
    db = load_db()
    user = db.get(session['user'])
    if not user or not user.get('current_skill'):
        return redirect(url_for('onboarding'))
    return redirect(url_for('dashboard_html'))

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    db = load_db()
    user = db.get(username)
    
    if not user:
        # Auto-register
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        db[username] = {
            "password": hashed,
            "xp": 0,
            "streak": 0,
            "consistency_shields": 1,
            "current_skill": None,
            "levels": {},
            "rank": {},
            "completed_tasks": {},
            "notifications": [],
            "last_login": str(datetime.date.today()),
            "college": request.form.get('college', 'Default College'),
            "joined_date": str(datetime.date.today()),
            "shield_paused_until": None,
            "paused_reason": None
        }
    elif not bcrypt.checkpw(password.encode(), user['password'].encode()):
        flash("Invalid password", "error")
        return redirect(url_for('index'))
    
    session['user'] = username
    save_db(db)
    return redirect(url_for('index'))

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        skill = request.form.get('skill')
        lvl = int(request.form.get('level', 1))
        db = load_db()
        db[session['user']]['current_skill'] = skill
        db[session['user']]['levels'][skill] = lvl
        save_db(db)
        return redirect(url_for('dashboard_html'))
    
    return render_template('onboarding.html', skills=SKILLS)

@app.route('/dashboard')
def dashboard_html():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    db = load_db()
    user = db[session['user']]
    skill = user['current_skill']
    lvl = user['levels'].get(skill, 1)
    
    task = ROADMAPS.get(skill, {}).get(lvl, {"title": "Mastery!", "desc": "Switch skills."})
    mentors = [n for n, d in db.items() if n != session['user'] and d.get('levels', {}).get(skill, 0) >= lvl + 2]
    
    save_db(db)
    return render_template('dashboard.html', user=user, task=task, skill=skill, lvl=lvl, mentors=mentors)

@app.route('/verify', methods=['POST'])
def verify():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    db = load_db()
    user = db.get(session['user'])
    if not user or not user.get('current_skill'):
        return redirect(url_for('onboarding'))
    
    skill = user['current_skill']
    lvl = user['levels'].get(skill, 1)
    if skill not in ROADMAPS or lvl not in ROADMAPS[skill]:
        return redirect(url_for('dashboard_html'))
    
    code = request.form.get('code')
    
    buffer = StringIO()
    sys.stdout = buffer
    try:
        exec(code)
        if buffer.getvalue() == ROADMAPS[skill][lvl]['expected']:
            xp_earned = 100 if ROADMAPS[skill][lvl]['is_test'] else 50
            user['xp'] += xp_earned
            user['levels'][skill] += 1
            user['streak'] += 1
            
            if user['streak'] % 7 == 0:
                user['consistency_shields'] += 1
                flash(f"🎯 Consistency Milestone! Earned Shield! Total: {user['consistency_shields']}", "success")
            else:
                flash(f"Quest Success! +{xp_earned} XP", "success")
        else:
            flash("Try again! Output doesn't match.", "error")
    except Exception as e:
        flash(f"Error: {e}", "error")
    finally:
        sys.stdout = sys.__stdout__
    
    save_db(db)
    return redirect(url_for('dashboard_html'))

@app.route('/leaderboard')
def leaderboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    db = load_db()
    rankings = []
    for username, user in db.items():
        rankings.append({
            "username": username,
            "xp": user.get('xp', 0),
            "streak": user.get('streak', 0),
            "level": max(user['levels'].values()) if user['levels'] else 0
        })
    
    rankings.sort(key=lambda x: x['xp'], reverse=True)
    
    return render_template('leaderboard.html', leaderboard=rankings[:50], current_user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('index'))

# ============================================
# ERROR HANDLERS
# ============================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
