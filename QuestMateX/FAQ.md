# QuestMate - FAQ & Troubleshooting

## ❓ Frequently Asked Questions

### General Questions

**Q: Is QuestMate free?**
A: Yes! QuestMate is completely free. No payments, no premium features. Pure peer learning.

**Q: Can I use it on my phone?**
A: Yes! The platform is fully responsive and works on all devices. Web-based, no app needed yet.

**Q: What skills can I learn?**
A: Currently: Python, Web Development, DSA, UI/UX. More coming in future versions.

**Q: How long does it take to master a skill?**
A: ~2-3 weeks if you complete one task daily. Faster if you dedicate more time.

### Features

**Q: What is the Consistency Shield?**
A: It lets you pause your progress for 3-90 days without losing your rank or XP. Perfect for exam season! You earn one shield per 7-day streak.

**Q: How does mentorship work?**
A: The system automatically suggests mentors who are 2+ levels ahead of you in the same skill and college. You can request help with one click!

**Q: Can I switch skills anytime?**
A: Yes! Click "Switch Skill" in the dashboard. Your progress in other skills is saved.

**Q: What happens if I don't complete a task?**
A: Your streak will break after 1 day. Use a Consistency Shield if you need a break!

**Q: How much XP do I get per task?**
A: Regular tasks: 50 XP. Milestone tests: 100 XP. Leaderboards rank by total XP.

## 🔧 Troubleshooting

### Installation Issues

**Problem: `ModuleNotFoundError: No module named 'flask'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt

# If that doesn't work:
pip install Flask==2.3.2 Flask-CORS==4.0.0 Flask-JWT-Extended==4.4.4 bcrypt==4.0.1
```

**Problem: Python version not compatible**
```bash
# Check your Python version
python --version

# QuestMate requires Python 3.8+
# If you have multiple versions:
python3.9 app.py  # or python3.10, python3.11
```

**Problem: `pip` command not found**
```bash
# Use pip3 instead
pip3 install -r requirements.txt
python3 app.py
```

### Running the App

**Problem: `Address already in use` error**
```bash
# Port 5001 is already being used
# Option 1: Kill the process
# Linux/Mac: lsof -ti:5001 | xargs kill
# Windows: netstat -ano | findstr :5001, then taskkill /PID <PID> /F

# Option 2: Use a different port
# Edit app.py, change: app.run(debug=True, port=5002)
python app.py
```

**Problem: App starts but page shows error 404**
```bash
# Make sure you're accessing the correct URL
# Should be: http://localhost:5001
# NOT: http://localhost:5001/dashboard (start at home page)

# Check that Flask is actually running (should see):
# "WARNING in app.run()" or "Running on http://127.0.0.1:5001"
```

**Problem: CSS/JS files not loading**
```bash
# Ensure static folder structure exists:
# QuestMateX/
#   └── static/
#       ├── css/
#       │   └── style.css
#       └── js/
#           └── main.js

# Hard refresh browser:
# Windows/Linux: Ctrl + Shift + R
# Mac: Cmd + Shift + R
```

### Login/Authentication

**Problem: Can't login, always returns to login page**
```
# Possible causes:
1. Password mismatch - Try different password
2. Username not created - Signup form creates account automatically
3. Session cookie issue - Clear browser cookies and try again
4. Browser privacy mode - Try in normal mode
```

**Problem: `bcrypt` import error**
```bash
# Solution: Install bcrypt
pip install bcrypt==4.0.1

# Or on Windows, if it fails:
pip install --only-binary :all: bcrypt
```

### Task Submission

**Problem: Code submission always fails**
```
# Possible causes:
1. Output doesn't match exactly (including whitespace)
2. Missing newline at end of output
3. Syntax error in code

# Debug: Copy expected output and compare character by character
# Expected: "Hello, World!\n"
# Got:      "Hello, World!"
# ^^^ Missing \n at end
```

**Problem: `Error: <the error message>`**
```python
# This means your code has a syntax/runtime error
# Common errors:

# NameError - variable not defined
x = 5
print(y)  # NameError: y is not defined

# TypeError - wrong data type
print(5 + "hello")  # TypeError: can't concatenate int and str

# IndentationError - wrong indentation
if True:
print("hello")  # IndentationError: expected an indented block
```

### Database Issues

**Problem: Data not persisting between sessions**
```
# In development, QuestMate uses JSON files:
# data/users.json, data/tasks.json, data/mentorship.json

# Make sure the data/ folder exists and is writable
# If data folder is missing:
mkdir data
# Files will be created automatically on first run
```

**Problem: Can't see other users on leaderboard**
```
# Leaderboard shows users who have selected a skill
# Steps to populate leaderboard:
1. Create multiple accounts
2. Each account selects a skill and starting level
3. Each account completes at least 1 task
4. Now leaderboard will show rankings
```

**Problem: Reset all data**
```bash
# To reset database (careful!):
# Option 1: Delete data folder
rm -rf data/  # Linux/Mac
rmdir /s data  # Windows

# Option 2: Delete specific file
rm data/users.json  # Removes all users
rm data/tasks.json  # Removes task history

# App will recreate files on next run
```

### Mentor & Shield Issues

**Problem: No mentors shown on dashboard**
```
# Reasons:
1. You're the first user in your college - no one 2+ levels ahead yet
2. No one is at least 2 levels higher - complete more tasks!
3. Mentors are from same college - check your college name

# Solution: Create test accounts with higher levels to test feature
```

**Problem: Can't activate Consistency Shield**
```
# Possible causes:
1. You've used all your shields - earn more by 7-day streaks
2. Shield already active - resume first before activating again
3. No reason provided - fill in the reason field

# Check console for error message
```

**Problem: Shield countdown incorrect**
```
# Shields are based on calendar days, not task completion days
# Shield paused until 2026-01-24 means:
# - Current date: 2026-01-17
# - Can resume any time after 2026-01-24
# - Even if you don't complete tasks during this period
```

## 🖥️ Browser Compatibility

**Tested & Working**:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile Safari (iOS 12+)
- ✅ Chrome Mobile (Android 6+)

**Known Issues**:
- ❌ IE11: Not supported (too old)
- ⚠️ Firefox Private Mode: Session issues (use normal mode)

**Browser Tips**:
- Clear cache if styles don't update
- Use Dev Tools (F12) to check console for errors
- Check Network tab if API calls fail

## 🔍 Debug Mode

### Enable Debug Logging
```python
# In app.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Flask Shell
```bash
flask shell
>>> from app import *
>>> db = load_db()
>>> list(db.keys())  # See all users
>>> db['username']   # See user details
```

### Browser Console
```javascript
// Open Dev Tools (F12) > Console
// Check for JavaScript errors
console.log(localStorage)  // View stored data
```

## 📞 Getting Help

### Before asking for help:
1. ✅ Check the error message carefully
2. ✅ Search this FAQ
3. ✅ Clear browser cache & restart app
4. ✅ Check that all files exist
5. ✅ Try a fresh installation

### Still stuck?
1. Check the terminal output for error messages
2. Look in browser console (F12) for JS errors
3. Verify file permissions (data folder writable)
4. Try on a different browser
5. Ask for help with full error message and steps to reproduce

## 🎓 Learning Resources

### Python Tasks Getting Hard?
- Try YouTube tutorials for specific topics
- Use Python documentation: python.org/docs
- Practice on codewars.com or leetcode.com
- Ask mentor for guidance

### Can't Find a Mentor?
- Mentor will appear once someone reaches 2+ levels ahead
- Or invite a friend to play and help each other!
- Feature will show suggestions once more users join

### Want to Learn Faster?
- Complete one task daily to build streak
- Milestone tests are worth more XP
- Use Consistency Shield strategically
- Learn alongside a study buddy

---

**Still have questions?** 

Check these files:
- README.md - Features & quick start
- SPECIFICATION.md - Detailed explanation
- DEVELOPER.md - Architecture & API
- DEPLOYMENT.md - Production setup

Happy Learning! 🚀

