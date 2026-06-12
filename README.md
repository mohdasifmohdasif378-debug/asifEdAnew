# AsifEdA AI — Smart Exam Preparation Platform
An AI-powered educational platform for competitive exam preparation (UPSC, SSC, NDA, NEET, JEE, JKSSB). Features secure JWT auth, local/cloud AI chat, responsive design, and 100% privacy.

## Features
✅ **Secure Authentication** — JWT tokens + bcrypt password hashing  
✅ **Smart Chat** — Optional Anthropic Claude AI, or local code-analysis fallback  
✅ **Responsive UI** — Works on mobile, tablet, desktop  
✅ **Docker Ready** — One-command deployment  
✅ **Privacy First** — API keys stay on your server, never leave  
✅ **Rate Limited** — Built-in protection against abuse  
✅ **Production Ready** — CORS, input validation, error handling  

## Quick Start (Local Development)

### Prerequisites
- **Docker** & **Docker Compose** installed
- **Git** to clone the repo

### Setup
```bash
# Clone the repository
git clone https://github.com/mohdasifmohdasif378-debug/asifEdAnew.git
cd asifEdAnew

# Copy environment template
cp .env.example .env

# Start the app (builds & runs in one command)
docker compose up --build

# Visit the app
open http://localhost:3000
# or: http://127.0.0.1:3000
```

### First Time Use
1. **Register** — create a new account (username + password)
2. **Login** — enter credentials
3. **Chat** — ask questions about the codebase or AI features
   - Without `ANTHROPIC_API_KEY`: local code-analysis assistant (studies your project)
   - With `ANTHROPIC_API_KEY`: uses Anthropic Claude for smarter answers

## Configuration

Edit `.env` to customize:

```bash
# Generate a secure SECRET_KEY (Linux/Mac):
openssl rand -hex 16

# Add your Anthropic key (optional)
ANTHROPIC_API_KEY=sk-ant-...

# Restrict frontend origins (security)
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Enable rate limiting
RATE_LIMIT_PER_MINUTE=60
```

## API Endpoints

### Authentication
- `POST /api/auth/register` — Create account
- `POST /api/auth/login` — Get JWT token
- `GET /api/auth/me` — Validate token

### Chat
- `POST /api/chat` — Send message (requires valid JWT)

### Health
- `GET /api/health` — Server status

## Deployment (Production)

### Option 1: Render.com (Recommended for beginners)
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New → Web Service → Connect repo → Deploy
4. Add `.env` secrets in dashboard
5. Done — app lives at your Render URL

### Option 2: Railway.app
1. Connect GitHub repo at [railway.app](https://railway.app)
2. Add `.env` variables
3. Deploy (auto-detects `docker-compose.yml`)

### Option 3: Self-hosted (VPS)
```bash
# On your server:
ssh user@your-server.com
git clone ...
cd asifEdAnew
cp .env.example .env
# Edit .env with your domain
nano .env

# Start with systemd or supervisord:
docker compose up -d

# Or use an nginx reverse proxy for HTTPS
```

## Performance Tips

- **Database**: For production, switch from SQLite to PostgreSQL:
  ```bash
  DATABASE_URL=postgresql://user:pass@host/dbname
  ```
- **Rate Limiting**: Adjust `RATE_LIMIT_PER_MINUTE` based on load
- **Caching**: Add Redis for token caching (future feature)

## Security

✅ Passwords hashed with bcrypt  
✅ JWT tokens expire in 24h  
✅ CORS restricted by `FRONTEND_ORIGINS`  
✅ Input validation on all endpoints  
✅ Rate limiting enabled  
✅ API key never logged or exposed  

## Troubleshooting

### Login not working?
- Check backend logs: `docker compose logs backend`
- Ensure `FRONTEND_ORIGINS` includes your URL

### Chat returning no results?
- Without Anthropic key: assistant searches project files (expected)
- With key: check `ANTHROPIC_API_KEY` is set correctly

### Port 3000 already in use?
```bash
# Change in docker-compose.yml:
ports:
  - "8080:80"  # Use 8080 instead
```

## Architecture

```
┌─────────────────┐
│ Frontend (nginx)│  :3000
└────────┬────────┘
         │ HTTP requests
┌────────▼────────┐
│ Backend (FastAPI)│ :8000
│  - Auth (JWT)   │
│  - Chat API     │
│  - Local AI *   │
└────────┬────────┘
         │ SQLite
    ┌────▼────┐
    │Database │
    └─────────┘

* Runs Claude API (if key set) or local code analysis (fallback)
```

## Development

### Run locally without Docker
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
python -m http.server 8000
```

### Run tests
```bash
# Coming soon
```

## License
MIT

## Founder
**Muhammad Asif** — [GitHub](https://github.com/mohdasifmohdasif378-debug)
