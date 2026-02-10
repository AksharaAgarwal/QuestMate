# QuestMate - Gamified Peer-Powered Learning Platform

🏆 **Built for:** Snowstorm Hackathon organized by Tech4Hack
👥 **Team:** Skillforge

A comprehensive full-stack web application designed for college students to learn programming and technical skills through gamified, peer-mentored micro-tasks.

## 🎮 Features

### 1. **Gamification System**
- **XP Points**: Earn XP for completing tasks (50 XP for regular tasks, 100 XP for milestone tests)
- **Streaks**: Build daily streaks to maintain consistency and motivation
- **Levels**: Progress through structured skill roadmaps
- **Leaderboards**: Compete globally and see rankings by XP, streak, and skill level
- **Milestones**: Unlock special achievements and consistency shields

### 2. **Consistency Shield System** ⭐
- **Pause Without Penalty**: Use consistency shields to pause progress during exams or personal emergencies 
- **Earn Through Streaks**: Earn new shields every 7-day streak milestone
- **Protect Rank**: When shield is active, XP and rank remain frozen (neither gain nor lose)
- **Flexible Duration**: Customize pause duration based on your needs

### 3. **Peer Mentorship (SkillSwap)**
- **Auto-Matching**: System automatically suggests mentors based on:
  - Skill expertise (must be 2+ levels ahead)
  - Same college/institution
  - Availability
- **Request System**: Students can request help from mentors
- **Doubt Resolution**: Real-time chat-based support (MVP shows mentor suggestions)
- **Community Learning**: Learn from peers who've mastered the skill

### 4. **Multi-Skill Learning Paths**
- **Python**: Variables, loops, functions, OOP, data structures
- **Web Development**: HTML, CSS, JavaScript, APIs, backends
- **DSA**: Arrays, linked lists, trees, graphs, DP
- **UI/UX**: Design principles, prototyping, accessibility

### 5. **Micro-Task System**
- **15-30 Minute Tasks**: Perfect for busy student schedules
- **Code Execution**: Write and test Python code directly in browser
- **Instant Feedback**: Get immediate feedback on code output
- **Explanation-Oriented**: Each task teaches a concept, not just drill
- **Milestone Tests**: Comprehensive 20-30 min tests every few levels

### 6. **Progress Tracking**
- **Skill-wise Ranks**: Individual rankings per skill
- **Progress Dashboard**: Visual progress on current skill
- **Task History**: Track all completed tasks
- **Notifications**: Get alerts for mentor requests and achievements

## 📁 Project Structure

```
QuestMateX/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README.md                   # This file
├── data/
│   ├── users.json             # User database (dev)
│   ├── tasks.json             # Task submissions
│   └── mentorship.json        # Mentorship requests
├── templates/
│   ├── landing.html           # Homepage
│   ├── auth.html              # Login/signup
│   ├── onboarding.html        # Skill selection
│   ├── dashboard.html         # Main learning dashboard
│   └── leaderboard.html       # Global rankings
├── static/
│   ├── css/
│   │   └── style.css          # Complete styling
│   └── js/
│       └── main.js            # Frontend logic & API calls
└── backend/
    └── app.py                 # REST API endpoints (optional)
```

## 💻 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Authentication**: bcrypt + JWT tokens
- **Database**: JSON (development) / MongoDB (production-ready)
- **Code Execution**: Python `exec()` with output capture

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients, animations
- **JavaScript**: Interactive modals, API calls, keyboard shortcuts
- **Responsive**: Mobile-friendly design (tested on all breakpoints)

### Production Ready
- REST API endpoints with JWT authentication
- CORS enabled for cross-origin requests
- Environment variable configuration
- Error handling and validation

## 🎯 Core Mechanics

### Task Submission Flow
1. User views daily quest on dashboard
2. Writes Python code in code editor
3. Clicks "Submit Solution"
4. Code executed server-side with output capture
5. Output compared with expected result
6. If correct: XP awarded, level increases, streak continues
7. If incorrect: Error message shown, user can retry

### Consistency Shield Activation
1. User clicks "Consistency Shield" button
2. Selects reason (exam, health, personal) and duration (3-7 days)
3. Shield activated - progress frozen
4. During shield period:
   - Streak doesn't reset even if user doesn't complete tasks
   - XP doesn't increase (frozen)
   - Rank doesn't change
5. User can resume anytime or automatic resume after duration

### Mentor Matching
1. System identifies users 2+ levels ahead in same skill and college
2. Shows top 5 available mentors on dashboard
3. User can request help with one click
4. Mentor receives notification
5. Direct communication initiated

## 📊 Gamification Balance

- **Daily Engagement**: Small tasks (50 XP) encourage daily play
- **Milestone Rewards**: 100 XP tests + shield for every 7-day streak
- **No Burnout**: Consistency shields allow break without penalty
- **Progression**: 10 levels per skill = ~2-3 weeks to mastery
- **Community**: Leaderboards without pay-to-win mechanics

## 🔐 Authentication & Security

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Stateless authentication for APIs
- **Session Management**: Secure flask sessions
- **Data Validation**: Input validation on all endpoints
- **CORS**: Controlled cross-origin requests

## 🌐 API Endpoints

### Authentication
- `POST /api/signup` - Create new account
- `POST /api/login` - Login and get JWT
- `GET /api/user/profile` - Get user profile

### Skills & Learning
- `GET /api/skills` - List all available skills
- `GET /api/skill/<skill>/roadmap` - Get skill roadmap
- `POST /api/user/select-skill` - Choose skill and level
- `POST /api/task/submit` - Submit task solution

### Consistency Shield
- `POST /api/shield/activate` - Pause progress
- `POST /api/shield/resume` - Resume progress

### Mentorship
- `GET /api/mentors/<skill>` - Get available mentors
- `POST /api/mentorship/request/<mentor_name>` - Request mentorship

### Leaderboards
- `GET /api/leaderboard/<skill>` - Get skill-wise rankings

## 📈 Scalability & Future Features

### Short Term (MVP)
- ✅ Python task support
- ✅ Consistency shields
- ✅ Peer mentorship matching
- ✅ Leaderboards
- ✅ Web frontend

### Medium Term (v2.0)
- [ ] Support more languages (Java, C++, JavaScript)
- [ ] Docker-based code execution (sandboxed)
- [ ] Real-time chat for mentor-student
- [ ] PostgreSQL database
- [ ] Email notifications
- [ ] Mobile app (React Native)

### Long Term (v3.0)
- [ ] AI-powered problem suggestions
- [ ] Video explanations for concepts
- [ ] Competitive coding arena
- [ ] Internship recommendations based on skills
- [ ] Company partnerships for job placement
- [ ] Certification system

## 📱 Responsive Design

- **Desktop (1200px+)**: Full layout with sidebar
- **Tablet (768px - 1199px)**: Optimized grid layout
- **Mobile (< 768px)**: Single column, touch-friendly buttons

## 🎨 Design Philosophy

- **Student-First**: Clean, minimal interface without distractions
- **Gamified**: Visual feedback (XP, streaks, badges) for motivation
- **Inclusive**: No payment barriers, pure skill-based progression
  
## 👥 Team Members

- Akshara Agarwal
- Harshita Tyagi
- Om Aggarwal
- Sagar 
