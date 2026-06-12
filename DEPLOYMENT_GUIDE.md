# 🎓 AsifEdA - Competitive Exam AI Brain | Deployment Guide

## ✅ What's Been Fixed

### 1. **Public Ports Configuration**
- ✅ Backend: `8001` (publicly accessible)
- ✅ Frontend: `3001` (publicly accessible)
- ✅ Docker networking bridge configured
- ✅ CORS origins updated to support new ports
- ✅ Corrupted docker-compose YAML fixed

### 2. **AI Knowledge Base Enhanced**
The system now handles:
- 🎯 **UPSC** - History, Geography, Economics, Constitution, Environment
- 📚 **SSC** - English, Maths, Reasoning, General Awareness (CGL, CHSL, MTS)
- 🪖 **NDA** - General Knowledge, Maths, Military Studies
- 💼 **Banking** - IBPS, SBI, RBI, NABARD exams

### 3. **System Configuration Updated**
- `config.py` - CORS origins updated to 3001 & 8001
- `chat_router.py` - Enhanced knowledge base with exam-specific responses
- `docker-compose.yml` - Fixed and optimized for public access

---

## 🚀 Quick Start

### Option 1: **With Anthropic API (FULL AI Power)**

```bash
# Set your API key
export ANTHROPIC_API_KEY=your-actual-key-here
export SECRET_KEY=your-secure-key

# Build and start
docker-compose up -d

# Check status
docker-compose ps
docker logs asifeda-backend
docker logs asifeda-frontend
```

**Access:**
- Frontend: `http://localhost:3001`
- Backend API: `http://localhost:8001/api`
- Health Check: `http://localhost:8001/api/health`

### Option 2: **Without API Key (Local Fallback)**

```bash
# Works without API key - uses local assistant
docker-compose up -d
```

---

## 📱 Access from External Devices

### On Same Network:
```
Frontend: http://<YOUR_COMPUTER_IP>:3001
Backend:  http://<YOUR_COMPUTER_IP>:8001/api
```

**Find your IP:**
```bash
hostname -I
```

### On Different Network (Cloud/Server):
```
Frontend: http://<SERVER_PUBLIC_IP>:3001
Backend:  http://<SERVER_PUBLIC_IP>:8001
```

**Requirements:**
1. Firewall allows ports 3001 & 8001
2. Docker containers running
3. Network connectivity established

---

## 🔐 Security Setup (Production)

```bash
# 1. Generate secure keys
export SECRET_KEY=$(openssl rand -hex 32)
export ANTHROPIC_API_KEY=your-actual-key

# 2. Set environment file
cat > .env << EOF
SECRET_KEY=$SECRET_KEY
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
FRONTEND_ORIGINS=http://yourdomain.com,https://yourdomain.com
DATABASE_URL=postgresql://user:pass@db:5432/asifeda
EOF

# 3. Deploy
docker-compose up -d
```

---

## 🎯 Usage Examples

### Login & Chat
1. **Register/Login** at `http://localhost:3001`
2. **Ask Questions:**
   - "What is GST and how does it work?"
   - "Explain Monetary Policy in simple terms"
   - "Give me 5 UPSC history questions"
   - "What are RBI functions?"
   - "NDA General Knowledge tips"

### Exam-Specific Queries
```
UPSC Topics:    Indian Constitution, Mughal Empire, GDP, Environment
SSC Topics:     Percentage Calculations, Synonyms, Reasoning Puzzles
NDA Topics:     General Knowledge, Military Terms, Defense
Banking Topics: Banking Regulations, RBI Guidelines, Financial Products
```

---

## 🔧 Troubleshooting

### Ports Not Accessible?
```bash
# Check if containers running
docker ps

# Check port bindings
docker port asifeda-backend
docker port asifeda-frontend

# View logs
docker logs asifeda-backend
docker logs asifeda-frontend
```

### CORS Errors?
```bash
# Already configured but verify:
docker exec asifeda-backend cat app/config.py | grep FRONTEND_ORIGINS
```

### Database Issues?
```bash
# Check data volume
docker volume ls | grep asifeda

# Clean restart (removes old data)
docker-compose down -v
docker-compose up -d
```

### API Not Responding?
```bash
# Test health check
curl http://localhost:8001/api/health

# Check backend logs
docker logs asifeda-backend -f
```

---

## 📊 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild images
docker-compose build --no-cache

# Access backend shell
docker exec -it asifeda-backend bash

# Access frontend shell
docker exec -it asifeda-frontend bash
```

---

## 📈 Performance Tips

1. **API Key Setup**: Connect ANTHROPIC_API_KEY for instant comprehensive answers
2. **Caching**: Frontend caches CSS/JS for 7 days (faster loads)
3. **Network**: Use bridge network for optimal container communication
4. **Database**: SQLite for development; use PostgreSQL for production

---

## 🌐 Production Deployment

### On Cloud (AWS, GCP, Azure):
```yaml
# Update docker-compose.yml:
ports:
  - "80:80"    # Frontend via HTTPS proxy
  - "8000:8000" # Backend via HTTPS proxy
```

### With Nginx Reverse Proxy:
```bash
# Install nginx on host
# Route traffic: yourdomain.com → 127.0.0.1:3001
# Route traffic: api.yourdomain.com → 127.0.0.1:8001
```

---

## ✨ Features

✅ **100% Public Access** - Ports 3001 & 8001 fully exposed
✅ **Competitive Exam Brain** - Handles UPSC, SSC, NDA, Banking queries
✅ **AI-Powered** - Uses Claude Haiku for intelligent responses (with API key)
✅ **Local Fallback** - Works without API key (limited mode)
✅ **User Authentication** - Register, login, persistent sessions
✅ **Real-time Chat** - Instant responses to exam questions
✅ **Docker Ready** - One-command deployment
✅ **CORS Configured** - Cross-origin requests allowed
✅ **Data Persistent** - Volumes preserve user data

---

## 🎓 System Architecture

```
┌─────────────────────────────────────┐
│         Frontend (Port 3001)        │
│    nginx + React/Vanilla JS         │
│  ✅ Public Access: http://IP:3001   │
└────────────────┬────────────────────┘
                 │ (API calls)
┌────────────────▼────────────────────┐
│         Backend (Port 8001)         │
│      FastAPI + SQLAlchemy           │
│  ✅ Public Access: http://IP:8001   │
│  AI: Claude Haiku + Local Fallback  │
└────────────────┬────────────────────┘
                 │ (ORM)
┌────────────────▼────────────────────┐
│     Database (SQLite in Volume)     │
│    Users, Chat History Stored       │
└─────────────────────────────────────┘
```

---

## 🆘 Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Verify ports: `netstat -tuln | grep 3001`
3. Test health: `curl localhost:8001/api/health`
4. Restart: `docker-compose restart`

---

**Ready to Deploy! 🚀**
Your AsifEdA competitive exam AI is now 100% public and ready to handle any UPSC, SSC, NDA, or Banking question!
