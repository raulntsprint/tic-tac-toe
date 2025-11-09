# 🎮 Tic Tac Toe - Advanced AI Game

An advanced Tic-Tac-Toe game featuring dual AI opponents, built with modern web technologies and containerized for easy deployment.

## 🌟 Features

### Dual AI Modes
- 🤖 **Minimax Algorithm**: Unbeatable AI using Minimax with alpha-beta pruning
- 🧠 **Groq AI**: Advanced LLM-powered opponent using Groq's API (Llama 3.1 70B)

### Modern Architecture
- **Backend**: FastAPI (Python 3.9+) with async/await support
- **Frontend**: React 18 + Vite for lightning-fast development
- **Containerization**: Docker & Docker Compose for seamless deployment
- **Session Management**: Server-side state management for multiple concurrent games
- **Type Safety**: Full type hints with Pydantic models

### Code Quality
- ✅ PEP8 compliant Python code
- ✅ SOLID principles applied
- ✅ Design patterns (Strategy, Singleton, Repository)
- ✅ Responsive and accessible UI
- ✅ Clean and maintainable architecture

## 📋 Prerequisites

Choose one of the following:

### Option A: Docker (Recommended)
- Docker 20.10+
- Docker Compose 1.29+

### Option B: Local Development
- Python 3.9+
- Node.js 18+
- npm or yarn

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
```bash
git clone <repository-url>
cd tic-tac-toe
```

2. **Set up environment variables** (optional, for Groq AI):
```bash
cp backend/env.example backend/.env
# Edit backend/.env and add your GROQ_API_KEY
```

3. **Start the application**:
```bash
docker-compose up --build
```

4. **Access the application**:
   - 🎮 Frontend: http://localhost:3000
   - 🔌 Backend API: http://localhost:8000
   - 📚 API Docs: http://localhost:8000/docs

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 🔑 Groq AI Setup (Optional)

The game works perfectly with the Minimax algorithm by default. To enable Groq AI:

1. **Get a free API key**:
   - Visit https://console.groq.com
   - Sign up with Google/GitHub (no credit card required)
   - Create an API key from the dashboard

2. **Configure the environment**:
```bash
# In backend/.env
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
```

3. **Restart the application**:
```bash
docker-compose restart backend
```

## 🏗️ Project Structure

```
tic-tac-toe/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic models
│   │   ├── game_logic.py        # Core game logic
│   │   ├── session_manager.py   # Session management
│   │   └── ai_players/
│   │       ├── __init__.py
│   │       ├── algorithmic.py   # Minimax AI
│   │       └── grok_ai.py       # Groq AI integration
│   ├── requirements.txt
│   ├── Dockerfile
│   └── env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Board.jsx        # Game board component
│   │   │   ├── Board.css
│   │   │   ├── Cell.jsx         # Individual cell component
│   │   │   ├── Cell.css
│   │   │   ├── GameControls.jsx # Game controls
│   │   │   └── GameControls.css
│   │   ├── api/
│   │   │   └── gameApi.js       # API client
│   │   ├── App.jsx              # Main application
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   ├── nginx.conf
│   └── index.html
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

## 🎯 API Endpoints

### Health Check
```
GET /api/health
```

### Create New Game
```
POST /api/game/new
Body: { "mode": "algorithmic" | "grok_ai" }
Response: { "session_id": "uuid", "state": {...}, "message": "..." }
```

### Make a Move
```
POST /api/game/{session_id}/move
Body: { "row": 0-2, "col": 0-2 }
Response: { "state": {...}, "message": "..." }
```

### Get Game State
```
GET /api/game/{session_id}/state
Response: { "session_id": "uuid", "state": {...} }
```

### Delete Game
```
DELETE /api/game/{session_id}
Response: { "message": "Game session deleted successfully" }
```

## 🧠 AI Implementation

### Minimax Algorithm
- **Algorithm**: Minimax with alpha-beta pruning
- **Performance**: O(b^d) with pruning optimization
- **Behavior**: Always plays optimally (unbeatable)
- **Use Case**: Perfect opponent for testing and challenge

### Groq AI
- **Model**: Llama 3.1 70B Versatile
- **Strategy**: LLM-based decision making
- **Fallback**: Automatically uses Minimax if API unavailable
- **Validation**: Server-side move validation
- **Use Case**: More human-like gameplay with advanced reasoning

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern async web framework
- **Pydantic**: Data validation with type hints
- **Uvicorn**: ASGI server
- **httpx**: Async HTTP client for API calls
- **python-dotenv**: Environment variable management

### Frontend
- **React 18**: UI library with hooks
- **Vite**: Next-generation build tool
- **Axios**: HTTP client
- **CSS3**: Modern styling with animations

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Production-ready web server
- **Multi-stage builds**: Optimized Docker images

## 📊 Design Patterns & Principles

### SOLID Principles
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible without modification
- **Liskov Substitution**: AI players are interchangeable
- **Interface Segregation**: Focused interfaces
- **Dependency Inversion**: Depend on abstractions

### Design Patterns
- **Strategy Pattern**: Interchangeable AI implementations
- **Singleton Pattern**: Session manager instance
- **Repository Pattern**: Data access abstraction
- **Facade Pattern**: Simplified API interface

## 🧪 Testing

Run backend tests:
```bash
cd backend
pytest
```

## 🎨 UI Features

- 🌈 Modern dark theme with gradient effects
- 📱 Fully responsive design (mobile-friendly)
- ✨ Smooth animations and transitions
- ♿ Accessible with ARIA labels
- 🎯 Clear visual feedback for game states
- 🔄 Loading states for async operations

## 📝 License

MIT License - see LICENSE file for details

## 👤 Author

Built for SSE Code Screen Challenge

## 🤝 Contributing

This is a coding challenge project. For improvements or suggestions, please open an issue.

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Docker Documentation](https://docs.docker.com/)

## 🐛 Troubleshooting

### Docker Issues
```bash
# Clean up Docker resources
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build --force-recreate
```

### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### Groq API Not Working
- ✅ Verify API key is correct (starts with `gsk_`)
- ✅ Check environment variables are loaded
- ✅ Restart Docker containers after changing .env
- ✅ Game will automatically fall back to Minimax algorithm

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Modern Python web development with FastAPI
- ✅ React hooks and state management
- ✅ Docker containerization and orchestration
- ✅ RESTful API design
- ✅ AI algorithm implementation (Minimax)
- ✅ LLM API integration (Groq)
- ✅ Full-stack application architecture
- ✅ Clean code principles and best practices

---

**Enjoy playing! 🎮**
