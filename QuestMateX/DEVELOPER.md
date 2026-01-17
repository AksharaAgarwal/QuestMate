# QuestMate Developer Guide

## Project Architecture

### Frontend Layer
- **Templates**: Jinja2 templates for server-side rendering
- **Styling**: Modern CSS with CSS variables for theming
- **JavaScript**: Vanilla JS (no framework) for simplicity
- **Assets**: Optimized images, fonts, icons

### Backend Layer
- **Flask**: Lightweight WSGI application
- **Routes**: RESTful API + traditional routes
- **Authentication**: bcrypt + JWT
- **Database**: JSON (dev) → MongoDB/PostgreSQL (prod)

### Data Flow

```
User Input → Flask Route → Validation → Business Logic → Database → Response → Frontend
```

## Database Schema

### Users Collection
```json
{
  "username": "string",
  "password": "hashed_bcrypt",
  "xp": "integer",
  "streak": "integer",
  "consistency_shields": "integer",
  "current_skill": "string",
  "levels": {
    "Python": 5,
    "Web Development": 3
  },
  "rank": {
    "Python": 1,
    "Web Development": 2
  },
  "completed_tasks": {
    "Python": [1, 2, 3, 4, 5],
    "Web Development": [1, 2]
  },
  "notifications": ["array of strings"],
  "last_login": "YYYY-MM-DD",
  "college": "string",
  "joined_date": "YYYY-MM-DD",
  "shield_paused_until": "YYYY-MM-DD or null",
  "paused_reason": "string or null"
}
```

## Key Functions

### Code Execution Engine
```python
buffer = StringIO()
sys.stdout = buffer
try:
    exec(user_code)
    output = buffer.getvalue()
    # Compare with expected output
finally:
    sys.stdout = sys.__stdout__
```

### Mentor Matching Algorithm
```python
mentors = [
    name for name, user in db.items()
    if (user['levels'].get(skill, 0) >= current_level + 2 
        and user['college'] == student_college)
]
```

### Streak & Shield Logic
```python
days_since_login = (today - last_login).days
if days_since_login > 1:
    if user['consistency_shields'] > 0 and not user['shield_paused_until']:
        user['consistency_shields'] -= 1  # Consume shield
    else:
        user['streak'] = 0  # Reset streak
```

## API Documentation

### Authentication Endpoints

#### POST /api/signup
Create new account
```json
{
  "username": "string",
  "password": "string",
  "college": "string"
}
```

#### POST /api/login
Login and get JWT
```json
{
  "username": "string",
  "password": "string"
}
```

### Learning Endpoints

#### GET /api/skills
List all skills with metadata

#### POST /api/user/select-skill
Choose skill and starting level
```json
{
  "skill": "Python",
  "level": 1
}
```

#### POST /api/task/submit
Submit solution code
```json
{
  "code": "print('Hello')"
}
```

### Consistency Shield Endpoints

#### POST /api/shield/activate
Pause progress
```json
{
  "reason": "exam",
  "days": 7
}
```

#### POST /api/shield/resume
Resume progress immediately

### Mentor Endpoints

#### GET /api/mentors/<skill>
Get available mentors for a skill

#### POST /api/mentorship/request/<mentor_name>
Send mentorship request

## Testing

### Unit Tests
```bash
python -m pytest tests/test_auth.py
python -m pytest tests/test_tasks.py
python -m pytest tests/test_shield.py
```

### Integration Tests
```bash
python -m pytest tests/test_integration.py
```

### Load Testing
```bash
locust -f locustfile.py
```

## Common Customizations

### Change Task Difficulty
Edit `ROADMAPS` in `app.py`:
```python
ROADMAPS["Python"][5] = {
    "title": "New Title",
    "desc": "Task description",
    "expected": "Expected output\n",
    "is_test": False
}
```

### Change XP Rewards
```python
xp_earned = 150 if ROADMAPS[skill][lvl]['is_test'] else 75  # Higher rewards
```

### Change Shield Duration
In `html`:
```html
<option value="14">2 weeks (was 1 week)</option>
```

### Add New Skill
```python
SKILLS["Machine Learning"] = {
    "description": "...",
    "icon": "🤖",
    "difficulty_progression": {1: "...", 2: "..."}
}

ROADMAPS["Machine Learning"] = {
    1: {"title": "...", "desc": "...", ...}
}
```

## Performance Tips

1. **Database Queries**: Cache frequently accessed data
2. **Code Execution**: Set timeout for user code
3. **Large Files**: Stream responses instead of loading entire dataset
4. **Caching**: Use Flask-Cache for view caching
5. **Compression**: Enable gzip for API responses

## Debugging

### Enable Flask Debug Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Interactive Shell
```bash
flask shell
```

## Version Control

### Branch Strategy
- `main`: Production-ready
- `develop`: Integration branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches

### Commit Messages
```
feat: Add consistency shield feature
fix: Correct streak calculation logic
docs: Update README with deployment guide
test: Add test for mentor matching
chore: Update dependencies
```

## Code Style

- **Python**: Follow PEP 8
- **JavaScript**: Use ES6+ syntax
- **CSS**: Use custom properties, follow mobile-first
- **Naming**: camelCase for JS, snake_case for Python

## Documentation

- **README.md**: Quick start and feature overview
- **DEPLOYMENT.md**: Deployment instructions
- **DEVELOPER.md**: This file
- **Inline Comments**: Complex business logic

---

For more details, see:
- Flask Docs: https://flask.palletsprojects.com/
- Python Docs: https://docs.python.org/3/
- JavaScript MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/
