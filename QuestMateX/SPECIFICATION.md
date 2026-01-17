# QuestMate - Complete Project Specification & Setup Guide

## 🎯 Project Overview

QuestMate is a **gamified, peer-powered learning platform** designed specifically for college students to master technical skills through:

1. **Daily Micro-Tasks** (15-30 min each)
2. **Gamification** (XP, Streaks, Levels, Leaderboards)
3. **Consistency Shields** (Pause without penalty during exams)
4. **Peer Mentorship** (Auto-matched mentors 2+ levels ahead)
5. **Skill-wise Learning Paths** (Python, Web Dev, DSA, UI/UX)

## 📦 Complete File Structure

```
QuestMateX/
├── app.py                          # Main Flask application (131 lines)
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── README.md                       # Project overview & features
├── DEVELOPER.md                    # Developer guide & architecture
├── DEPLOYMENT.md                   # Deployment instructions
│
├── templates/                      # Jinja2 HTML templates
│   ├── landing.html               # Homepage with features
│   ├── auth.html                  # Login/signup form
│   ├── onboarding.html            # Skill selection
│   ├── dashboard.html             # Main learning dashboard
│   └── leaderboard.html           # Global rankings
│
├── static/
│   ├── css/
│   │   └── style.css              # Complete styling (700+ lines)
│   │                               # - Responsive design (mobile-first)
│   │                               # - Dark theme with gradients
│   │                               # - Animations & transitions
│   │                               # - Modal styling
│   │                               # - Dashboard layout
│   │
│   └── js/
│       └── main.js                # Frontend logic (200+ lines)
│                                   # - Modal management
│                                   # - API helpers
│                                   # - Keyboard shortcuts
│                                   # - Auto-hide alerts
│
├── data/                          # Data storage (dev mode)
│   ├── users.json                 # User database
│   ├── tasks.json                 # Task submissions
│   └── mentorship.json            # Mentorship requests
│
└── backend/                       # Optional REST API
    └── app.py                     # Full REST API with JWT
```

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
cd QuestMateX
pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
```

### 3. Access Platform
- Open: `http://localhost:5001`
- Login/Signup with any username & password
- Select a skill (Python recommended)
- Choose starting level (1, 3, or 5)
- Start completing daily quests!

## 💾 Database Schema

### Users (users.json)
```json
{
  "username": {
    "password": "bcrypt_hash",
    "xp": 0,
    "streak": 0,
    "consistency_shields": 1,
    "current_skill": "Python",
    "levels": {"Python": 1, "Web Development": 0},
    "rank": {"Python": 1},
    "completed_tasks": {"Python": [1, 2, 3]},
    "notifications": [],
    "last_login": "2026-01-17",
    "college": "IIT Delhi",
    "joined_date": "2026-01-17",
    "shield_paused_until": null,
    "paused_reason": null
  }
}
```

### Mentorship (mentorship.json)
```json
{
  "request_id": {
    "student": "alice",
    "mentor": "bob",
    "skill": "Python",
    "topic": "Functions",
    "created_at": "2026-01-17 10:30:00",
    "status": "pending",
    "messages": []
  }
}
```

## 🎮 Core Features Explained

### 1. Gamification System

**XP Points**
- Regular tasks: 50 XP
- Milestone tests: 100 XP
- Leaderboard based on total XP

**Streaks**
- +1 day for each task completed
- Breaks after 1 day without task
- 7-day milestones award consistency shields

**Levels**
- 10 levels per skill (1-10)
- Progress by completing tasks
- Unlock new difficulty as you level up

**Leaderboards**
- Global rankings by XP
- Skill-specific rankings
- Top 3 medal system (🥇🥈🥉)

### 2. Consistency Shield System ⭐

**Purpose**: Allow students to pause during exams without losing rank/XP

**Features**:
- 1 shield per new user
- Earn 1 shield every 7-day streak
- Activate shield for 3-90 days
- Progress frozen (no XP gain/loss, streak protected)
- Can resume anytime

**Flow**:
1. User clicks "Consistency Shield"
2. Selects reason (exam, health, personal)
3. Chooses duration (3/7/14/30 days)
4. Shield activates - progress frozen
5. After duration or manual resume - progress continues

### 3. Peer Mentorship

**Auto-Matching Algorithm**:
- Find users 2+ levels ahead in same skill
- Same college/institution
- Show top 5 available mentors
- One-click request system

**Benefits**:
- No payments (pure peer learning)
- Learn from proven experts
- Direct communication with mentors
- Build community relationships

### 4. Task Submission System

**Code Execution**:
1. User writes Python code in editor
2. Code executed server-side with output capture
3. Output compared with expected result
4. Instant feedback (pass/fail)
5. XP awarded on success

**Example Task**:
```python
Task: Hello World
Expected: print("Hello, World!")
Output: Hello, World!\n
Result: ✅ Pass (+50 XP)
```

### 5. Learning Roadmaps

Each skill has 10 structured levels:

**Python Path**:
1. Hello World → 2. Variables → 3. Operators → 4. Strings → 5. Conditionals → 
6. Loops → **7. MILESTONE TEST** → 8. Lists → 9. Functions → **10. MILESTONE TEST**

**Web Development Path**:
1. HTML Basics → 2. Forms → 3. CSS Styling → 4. JavaScript → 5. DOM Manipulation → 
6. API Calls → 7. Async/Await → 8. Frameworks → 9. Backend → 10. Full Stack

## 📊 API Endpoints

### Public Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Homepage |
| `POST` | `/auth` | Login/Signup |
| `GET` | `/onboarding` | Skill selection |
| `POST` | `/onboarding` | Confirm skill choice |
| `GET` | `/dashboard` | Main dashboard |
| `POST` | `/verify` | Submit task |
| `GET` | `/leaderboard` | View rankings |
| `POST` | `/request_help/<mentor>` | Request mentorship |
| `GET` | `/logout` | Logout |

### REST API Endpoints (Optional)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/signup` | Create account |
| `POST` | `/api/login` | Login |
| `GET` | `/api/user/profile` | Get user data |
| `GET` | `/api/skills` | List skills |
| `POST` | `/api/task/submit` | Submit code |
| `POST` | `/api/shield/activate` | Pause progress |
| `POST` | `/api/shield/resume` | Resume progress |
| `GET` | `/api/mentors/<skill>` | Get available mentors |
| `GET` | `/api/leaderboard/<skill>` | Get skill rankings |

## 🔐 Authentication

**Default Method**: Session-based (Flask sessions)

**Optional JWT**: Fully implemented for REST APIs
- Generate: `create_access_token(identity=username)`
- Validate: `@jwt_required()`
- Header: `Authorization: Bearer <token>`

**Password Security**:
- bcrypt hashing (salt rounds: 10)
- Never stored in plain text
- Verified on each login

## 📱 Frontend Features

### Responsive Design
- ✅ Desktop (1200px+): Full sidebar layout
- ✅ Tablet (768px-1199px): Optimized grid
- ✅ Mobile (<768px): Single column, touch-friendly

### User Interface
- Dark theme (student-friendly)
- Smooth animations & transitions
- Modal dialogs for secondary actions
- Keyboard shortcuts (Escape, Ctrl+Enter)
- Auto-hiding alerts after 5 seconds

### Components
- **Navbar**: Logo, user info, navigation
- **Sidebar**: Stats, actions, skill info
- **Task Panel**: Task description, code editor, submit button
- **Mentor Cards**: Mentor suggestions with request buttons
- **Modal Dialogs**: Task details, shield options, mentor list
- **Leaderboard Table**: Rankings with medals

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **Security**: bcrypt, JWT tokens
- **Database**: JSON (dev) → MongoDB/PostgreSQL (prod)
- **Code Execution**: Python `exec()` with StringIO
- **API**: RESTful + REST API with CORS

### Frontend
- **HTML5**: Semantic markup with Jinja2 templating
- **CSS3**: Custom properties, animations, gradients
- **JavaScript**: ES6+ vanilla (no framework)
- **Responsive**: Mobile-first design

### Development
- **Package Manager**: pip
- **Version Control**: Git
- **Documentation**: Markdown

## 🎓 Learning Outcomes

After completing QuestMate:

**Python Path**:
- Understand basic syntax and data types
- Master control flow (loops, conditionals)
- Work with functions and data structures
- Learn OOP principles
- Handle errors gracefully

**Web Development Path**:
- Build semantic HTML pages
- Style with modern CSS
- Interact with JavaScript
- Call APIs asynchronously
- Deploy full-stack applications

**DSA Path**:
- Master fundamental data structures
- Solve algorithmic problems
- Optimize solutions
- Prepare for interviews

**UI/UX Path**:
- Understand design principles
- Create user-friendly interfaces
- Implement accessible designs
- Prototype interactive systems

## 📈 Growth & Retention Mechanics

**Short-term Engagement**:
- Daily tasks (micro-commitments)
- Immediate XP feedback
- Visible streak counter

**Medium-term Engagement**:
- Leaderboard competition
- 7-day streak milestones
- Shield progression

**Long-term Retention**:
- Peer mentorship relationships
- Skill mastery path
- Community building

## 🐛 Known Limitations (MVP)

- Code execution limited to Python
- No real-time chat (notifications only)
- JSON database (scales to ~10K users)
- No code sandboxing (trust users for now)
- No video explanations
- No mobile app yet

## 🚀 Future Roadmap

**v1.1** (Next Sprint):
- [ ] Add Java/JavaScript task support
- [ ] Email notifications
- [ ] Real-time mentor chat
- [ ] Task difficulty customization

**v2.0** (Quarter 2):
- [ ] Docker-based code execution (sandboxed)
- [ ] PostgreSQL database
- [ ] Mobile app (React Native)
- [ ] Advanced analytics & insights
- [ ] Video explanations library

**v3.0** (Quarter 3):
- [ ] AI-powered problem suggestions
- [ ] Competitive coding arena
- [ ] Company partnerships
- [ ] Internship recommendations
- [ ] Certification system

## 📚 Resources

### Documentation
- [README.md](README.md) - Quick start & features
- [DEVELOPER.md](DEVELOPER.md) - Architecture & customization
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

### External Links
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/3/)
- [MDN Web Docs](https://developer.mozilla.org/)

## 🎯 Success Metrics

**User Metrics**:
- Daily Active Users (DAU)
- Monthly Retention Rate
- Average Tasks per Session
- Streak Completion Rate

**Learning Metrics**:
- Task Success Rate
- Average Time per Task
- Skills Completed per User
- Mentor Request Success Rate

**Platform Metrics**:
- Server Response Time
- Code Execution Speed
- Error Rate
- Database Query Time

## 💡 Hackathon Demo Notes

**What to Highlight**:
1. 🎮 Gamification (streaks, XP, shields, leaderboards)
2. 🛡️ Consistency Shield unique value prop
3. 👥 Peer mentorship auto-matching
4. ⚡ Fast task submission & feedback
5. 📱 Responsive, student-friendly UI

**Demo Flow**:
1. Signup as new user
2. Select Python skill
3. Complete 2-3 tasks successfully
4. Show leaderboard
5. Demonstrate consistency shield
6. Show mentor matching

**Expected Feedback**:
- "Love the shield idea for exam season!"
- "Auto-mentorship matching is brilliant!"
- "Perfect for college students"
- "So much better than boring tutorials"

---

**QuestMate v1.0** | MVP Ready | 2026 Hackathon Submission

Built with ❤️ for college students. No payments, no tracking, just learning together.
