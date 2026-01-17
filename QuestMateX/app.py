import os, json, sys, datetime
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "questmate_final_rescue"

# Auto-setup data directory
os.makedirs('data', exist_ok=True)
USER_DATA = 'data/users.json'

def load_db():
    if not os.path.exists(USER_DATA): return {}
    with open(USER_DATA, 'r') as f: return json.load(f)

def save_db(data):
    with open(USER_DATA, 'w') as f: json.dump(data, f, indent=4)

# Multi-Skill Roadmaps with Real Coding Challenges
ROADMAPS = {
    "Python": {
        1: {
            "title": "Hello World",
            "desc": "Write a program to print 'Hello, World!'",
            "expected": "Hello, World!\n",
            "is_test": False,
            "hint": "Use the print() function"
        },
        2: {
            "title": "Odd or Even",
            "desc": "Write a program that takes a number and prints whether it is odd or even.\nExample: For input 5, print 'Odd'\nFor input 4, print 'Even'",
            "expected": "Odd\n",
            "is_test": False,
            "test_input": "n = 5",
            "hint": "Use modulo operator (%) to check divisibility by 2"
        },
        3: {
            "title": "Sum of Numbers",
            "desc": "Write a program to find the sum of first n natural numbers.\nExample: For n=5, output should be 15 (1+2+3+4+5)",
            "expected": "15\n",
            "is_test": False,
            "test_input": "n = 5",
            "hint": "Use a loop or the formula n*(n+1)/2"
        },
        4: {
            "title": "MILESTONE TEST - Factorial",
            "desc": "Write a program to find the factorial of a number.\nExample: For n=5, output should be 120 (5*4*3*2*1)",
            "expected": "120\n",
            "is_test": True,
            "test_input": "n = 5",
            "hint": "Use a loop to multiply numbers from 1 to n"
        },
        5: {
            "title": "Prime Number Checker",
            "desc": "Check if a number is prime.\nExample: For 7, print 'Prime'\nFor 4, print 'Not Prime'",
            "expected": "Prime\n",
            "is_test": False,
            "test_input": "n = 7",
            "hint": "A prime number is only divisible by 1 and itself"
        },
        6: {
            "title": "Fibonacci Series",
            "desc": "Print first n Fibonacci numbers.\nExample: For n=5, print: 0 1 1 2 3",
            "expected": "0 1 1 2 3\n",
            "is_test": False,
            "test_input": "n = 5",
            "hint": "Each number is the sum of the previous two numbers"
        },
        7: {
            "title": "MILESTONE TEST - Palindrome Checker",
            "desc": "Check if a string is a palindrome.\nExample: For 'racecar', print 'Palindrome'\nFor 'hello', print 'Not Palindrome'",
            "expected": "Palindrome\n",
            "is_test": True,
            "test_input": "s = 'racecar'",
            "hint": "Compare the string with its reverse"
        },
        8: {
            "title": "List Operations",
            "desc": "Create a list [1,2,3,4,5] and find the sum of all elements",
            "expected": "15\n",
            "is_test": False,
            "hint": "Use the sum() function or a loop"
        },
        9: {
            "title": "String Reversal",
            "desc": "Reverse a string 'Python' and print it",
            "expected": "nohtyP\n",
            "is_test": False,
            "hint": "Use string slicing [::-1]"
        },
        10: {
            "title": "MASTERY - Word Counter",
            "desc": "Count the number of words in a string.\nExample: 'Hello World Python' should output 3",
            "expected": "3\n",
            "is_test": True,
            "test_input": "text = 'Hello World Python'",
            "hint": "Use split() method to break the string into words"
        }
    },
    "HTML": {
        1: {
            "title": "Basic HTML Structure",
            "desc": "Create a simple HTML page with a heading 'Welcome'",
            "expected": "<h1>Welcome</h1>\n",
            "is_test": False,
            "hint": "Use <h1> tags"
        },
        2: {
            "title": "Paragraphs and Text",
            "desc": "Create a paragraph tag with text 'Learning HTML'",
            "expected": "<p>Learning HTML</p>\n",
            "is_test": False,
            "hint": "Use <p> tags"
        },
        3: {
            "title": "MILESTONE TEST - Lists",
            "desc": "Create an unordered list with items: Apple, Banana, Cherry",
            "expected": "<ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul>\n",
            "is_test": True,
            "hint": "Use <ul> and <li> tags"
        },
        4: {
            "title": "Links and Anchors",
            "desc": "Create a hyperlink to 'https://example.com' with text 'Click Here'",
            "expected": "<a href=\"https://example.com\">Click Here</a>\n",
            "is_test": False,
            "hint": "Use <a> tags with href attribute"
        },
        5: {
            "title": "Form Elements",
            "desc": "Create an input field for email",
            "expected": "<input type=\"email\">\n",
            "is_test": False,
            "hint": "Use <input> tag with type attribute"
        }
    }
}

# Skills with metadata for onboarding
SKILLS = {
    "Python": {
        "description": "Master Python programming from basics to advanced",
        "icon": "🐍"
    },
    "HTML": {
        "description": "Learn HTML markup and web structure",
        "icon": "🌐"
    }
}

@app.route('/')
def index():
    if 'user' not in session: return render_template('auth.html')
    db = load_db()
    user = db.get(session['user'])
    if not user or not user.get('current_skill'): return redirect(url_for('onboarding'))
    return redirect(url_for('dashboard'))

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    # Validate inputs
    if not username or len(username) < 3:
        flash("Username must be at least 3 characters long!", "error")
        return redirect(url_for('index'))
    
    if not password or len(password) < 4:
        flash("Password must be at least 4 characters long!", "error")
        return redirect(url_for('index'))
    
    db = load_db()
    
    if username not in db:
        # New user - create account
        db[username] = {
            "xp": 0, "streak": 0, "shields": 1, "current_skill": None, 
            "levels": {}, "notifications": [], "last_login": str(datetime.date.today()),
            "password": password,  # Store password (in production, use bcrypt)
            "college": request.form.get('college', '')
        }
        session['user'] = username
        save_db(db)
        flash(f"Account created! Welcome, {username}!", "success")
        return redirect(url_for('onboarding'))
    else:
        # Existing user - verify password
        stored_password = db[username].get('password')
        
        # If no password exists (old account), set it now
        if not stored_password:
            db[username]['password'] = password
            session['user'] = username
            save_db(db)
            flash(f"Password set! Welcome back, {username}!", "success")
            return redirect(url_for('index'))
        
        # Check password
        if stored_password == password:
            session['user'] = username
            save_db(db)
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Incorrect password!", "error")
            return redirect(url_for('index'))

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        skill = request.form.get('skill', '').strip()
        level_str = request.form.get('level', '1').strip()
        
        # Validate skill
        if skill not in SKILLS:
            flash("Please select a valid skill!", "error")
            return render_template('onboarding.html', skills=SKILLS)
        
        # Validate level
        try:
            lvl = int(level_str)
            if lvl < 1 or lvl > 10:
                flash("Level must be between 1 and 10!", "error")
                return render_template('onboarding.html', skills=SKILLS)
        except ValueError:
            flash("Invalid level selection!", "error")
            return render_template('onboarding.html', skills=SKILLS)
        
        db = load_db()
        db[session['user']]['current_skill'] = skill
        db[session['user']]['levels'][skill] = lvl
        save_db(db)
        flash(f"Great! You've selected {skill} at level {lvl}.", "success")
        return redirect(url_for('dashboard'))
    return render_template('onboarding.html', skills=SKILLS)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('index'))
    db = load_db()
    user = db[session['user']]
    skill = user['current_skill']
    lvl = user['levels'].get(skill, 1)
    
    # Shield & Streak Logic
    today = datetime.date.today()
    last_login = datetime.datetime.strptime(user['last_login'], '%Y-%m-%d').date()
    if (today - last_login).days > 1:
        if user['shields'] > 0:
            user['shields'] -= 1
            flash("Shield saved your streak! 🛡️", "info")
        else:
            user['streak'] = 0
    user['last_login'] = str(today)
    
    task = ROADMAPS[skill].get(lvl, {"title": "Mastery!", "desc": "Switch skills."})
    
    # Peer Connect Logic: Find people 2+ levels ahead
    mentors = [n for n, d in db.items() if n != session['user'] and d['levels'].get(skill, 0) >= lvl + 2]
    
    save_db(db)
    return render_template('dashboard.html', user=user, task=task, skill=skill, lvl=lvl, mentors=mentors)

@app.route('/verify', methods=['POST'])
def verify():
    db = load_db()
    user = db[session['user']]
    skill = user['current_skill']
    lvl = user['levels'][skill]
    code = request.form.get('code')
    
    buffer = StringIO()
    sys.stdout = buffer
    try:
        exec(code)
        if buffer.getvalue() == ROADMAPS[skill][lvl]['expected']:
            user['xp'] += 50
            user['levels'][skill] += 1
            user['streak'] += 1
            if user['streak'] % 5 == 0: user['shields'] += 1
            flash("Quest Success!", "success")
        else: flash("Try again!", "error")
    except Exception as e: flash(f"Error: {e}", "error")
    finally: sys.stdout = sys.__stdout__
    
    save_db(db)
    return redirect(url_for('dashboard'))

@app.route('/request_help/<m>')
def request_help(m):
    if 'user' not in session: return redirect(url_for('index'))
    db = load_db()
    
    # Check if mentor exists
    if m not in db:
        flash("Mentor not found!", "error")
        return redirect(url_for('dashboard'))
    
    # Create mentorship connection
    if 'mentorship_requests' not in db[m]:
        db[m]['mentorship_requests'] = []
    
    requester = session['user']
    if requester not in db[m]['mentorship_requests']:
        db[m]['mentorship_requests'].append(requester)
    
    # Store in requester's profile too
    if 'mentor_connections' not in db[requester]:
        db[requester]['mentor_connections'] = []
    
    if m not in db[requester]['mentor_connections']:
        db[requester]['mentor_connections'].append(m)
    
    save_db(db)
    flash(f"Request sent to {m}! Waiting for acceptance...", "info")
    return redirect(url_for('dashboard'))

@app.route('/mentor/chat/<mentor_name>')
def mentor_chat(mentor_name):
    if 'user' not in session: return redirect(url_for('index'))
    db = load_db()
    
    # Check if user has connection with this mentor
    current_user = session['user']
    if mentor_name not in db:
        flash("Mentor not found!", "error")
        return redirect(url_for('dashboard'))
    
    # Get or initialize chat history
    if 'chat_history' not in db[current_user]:
        db[current_user]['chat_history'] = {}
    
    if mentor_name not in db[current_user]['chat_history']:
        db[current_user]['chat_history'][mentor_name] = []
    
    chat_messages = db[current_user]['chat_history'][mentor_name]
    save_db(db)
    
    return render_template('mentor_chat.html', mentor=mentor_name, current_user=current_user, messages=chat_messages)

@app.route('/mentor/send_message/<mentor_name>', methods=['POST'])
def send_message(mentor_name):
    if 'user' not in session: return redirect(url_for('index'))
    db = load_db()
    
    current_user = session['user']
    message = request.form.get('message', '').strip()
    
    if not message:
        flash("Message cannot be empty!", "error")
        return redirect(url_for('mentor_chat', mentor_name=mentor_name))
    
    # Initialize chat history if needed
    if 'chat_history' not in db[current_user]:
        db[current_user]['chat_history'] = {}
    if mentor_name not in db[current_user]['chat_history']:
        db[current_user]['chat_history'][mentor_name] = []
    
    # Add message
    db[current_user]['chat_history'][mentor_name].append({
        'sender': current_user,
        'message': message,
        'timestamp': str(datetime.datetime.now())
    })
    
    # Also store in mentor's side
    if 'chat_history' not in db[mentor_name]:
        db[mentor_name]['chat_history'] = {}
    if current_user not in db[mentor_name]['chat_history']:
        db[mentor_name]['chat_history'][current_user] = []
    
    db[mentor_name]['chat_history'][current_user].append({
        'sender': current_user,
        'message': message,
        'timestamp': str(datetime.datetime.now())
    })
    
    save_db(db)
    return redirect(url_for('mentor_chat', mentor_name=mentor_name))

@app.route('/mentor/video_call/<mentor_name>')
def video_call(mentor_name):
    if 'user' not in session: return redirect(url_for('index'))
    db = load_db()
    
    if mentor_name not in db:
        flash("Mentor not found!", "error")
        return redirect(url_for('dashboard'))
    
    current_user = session['user']
    return render_template('video_call.html', mentor=mentor_name, current_user=current_user)

@app.route('/activate_shield', methods=['POST'])
def activate_shield():
    if 'user' not in session: return redirect(url_for('index'))
    db = load_db()
    user = db[session['user']]
    reason = request.form.get('reason', 'Personal')
    days = int(request.form.get('days', 7))
    
    if user['shields'] > 0:
        user['shields'] -= 1
        from datetime import timedelta
        pause_until = (datetime.date.today() + timedelta(days=days)).isoformat()
        user['shield_paused_until'] = pause_until
        flash(f"Shield activated for {days} days! Your progress is paused.", "success")
    else:
        flash("No shields available!", "error")
    
    save_db(db)
    return redirect(url_for('dashboard'))

@app.route('/resume_progress', methods=['POST'])
def resume_progress():
    if 'user' not in session: return redirect(url_for('index'))
    db = load_db()
    user = db[session['user']]
    
    if 'shield_paused_until' in user:
        del user['shield_paused_until']
        flash("Progress resumed! Keep grinding!", "success")
    else:
        flash("No paused progress found!", "error")
    
    save_db(db)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You've logged out. See you next time!", "info")
    return redirect(url_for('index'))

@app.route('/leaderboard')
def leaderboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    db = load_db()
    
    # Create leaderboard entries sorted by XP
    leaderboard_data = []
    for username, user_data in db.items():
        if username != 'users':  # Skip metadata
            skill = user_data.get('current_skill', 'N/A')
            level = user_data.get('levels', {}).get(skill, 1) if skill != 'N/A' else 1
            leaderboard_data.append({
                'username': username,
                'xp': user_data.get('xp', 0),
                'streak': user_data.get('streak', 0),
                'level': level,
                'skill': skill
            })
    
    # Sort by XP descending
    leaderboard_data.sort(key=lambda x: x['xp'], reverse=True)
    
    return render_template('leaderboard.html', leaderboard=leaderboard_data, current_user=session.get('user'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)