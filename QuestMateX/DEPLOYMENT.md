# QuestMate Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Setup
```bash
# Clone/navigate to project
cd QuestMateX

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Visit `http://localhost:5001`

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

### Build & Run
```bash
docker build -t questmate:latest .
docker run -p 5001:5001 questmate:latest
```

## Heroku Deployment

### Procfile
```
web: gunicorn app:app
```

### Steps
```bash
heroku create questmate-app
git push heroku main
heroku config:set SECRET_KEY=<your-secret-key>
heroku open
```

## AWS Deployment

### EC2 Setup
1. Launch Ubuntu 20.04 instance
2. SSH into instance
3. Install Python and dependencies
4. Clone repository
5. Use supervisor/systemd for process management
6. Set up Nginx reverse proxy

### RDS Database
- Use PostgreSQL for production
- Update connection string in `.env`

## Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Set up proper database (PostgreSQL)
- [ ] Configure environment variables
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure backups
- [ ] Add rate limiting
- [ ] Set up monitoring
- [ ] Test all APIs

## Performance Optimization

- [ ] Enable gzip compression
- [ ] Minify static assets
- [ ] Add CDN for static files
- [ ] Implement caching (Redis)
- [ ] Database indexing on frequently queried fields
- [ ] Load balancing with multiple app instances

## Security Hardening

- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS protection (output encoding)
- [ ] CSRF protection (Flask provides)
- [ ] Rate limiting on APIs
- [ ] Input validation on all endpoints
- [ ] Use HTTPS/TLS
- [ ] Secure headers (Content-Security-Policy, etc.)
- [ ] Regular security audits

## Monitoring & Logging

- [ ] Sentry for error tracking
- [ ] ELK stack for logging
- [ ] Prometheus for metrics
- [ ] CloudWatch for AWS deployments
- [ ] Regular log analysis

## Database Migration (to PostgreSQL)

```python
# Update database config in app.py
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/questmate'
db = SQLAlchemy(app)

# Create models and migrate using Alembic
```

## Scaling Strategies

1. **Horizontal Scaling**: Load balancer + multiple app instances
2. **Database Caching**: Redis for user sessions and leaderboards
3. **Async Tasks**: Celery for background jobs
4. **CDN**: CloudFront for static assets
5. **Microservices**: Separate API, execution engine, notification service

---

For questions or deployment issues, refer to Flask documentation: https://flask.palletsprojects.com/
