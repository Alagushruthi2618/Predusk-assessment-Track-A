# Me-API Playground

A simple, production-ready backend API and minimal frontend that stores and showcases personal profile information, projects, and skills via a clean REST API.

## Project Overview

This project is a personal portfolio API built with FastAPI that allows you to:
- Store and retrieve your professional profile information
- Manage your technical skills with proficiency levels
- Showcase your projects with associated skills
- Search across projects and skills
- Access everything through a clean REST API

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.10+
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic schemas
- **CORS**: Enabled for frontend access
- **Auto-documentation**: Available at `/docs` endpoint

### Frontend (Vanilla Web Technologies)
- **HTML5**: Semantic markup
- **CSS3**: Basic styling for readability
- **JavaScript (ES6+)**: Fetch API for backend communication
- **No frameworks**: Pure vanilla JavaScript as specified

### Database Schema
- **profiles**: Single row storing personal information
- **skills**: Technical skills with proficiency levels
- **projects**: Portfolio projects with descriptions
- **project_skills**: Many-to-many relationship table

## API Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "ok"}`

### Profile Management
```
GET /profile
PUT /profile
```
**Authentication:**
- `GET /profile` - Public access (no authentication required)
- `PUT /profile` - Requires API key in `X-API-Key` header

**Example PUT request with API key:**
```bash
curl -X PUT http://localhost:8000/profile \
  -H "Content-Type: application/json" \
  -H "X-API-Key: supersecret123" \
  -d '{"name": "Your Name", "email": "your.email@example.com"}'
```
**Profile fields:**
- `name` (string, required)
- `email` (string, required)
- `education` (string, optional)
- `bio` (text, optional)
- `github` (string, optional)
- `linkedin` (string, optional)
- `portfolio` (string, optional)

**Example GET response:**
```json
{
  "id": 1,
  "name": "YOUR NAME HERE",
  "email": "your.email@example.com",
  "education": "Bachelor of Science in Computer Science",
  "bio": "Passionate software developer...",
  "github": "https://github.com/yourusername",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "portfolio": "https://yourportfolio.com"
}
```

### Skills
```
GET /skills
GET /skills/top
```
**Example response:**
```json
[
  {
    "id": 1,
    "name": "Python",
    "level": "Expert"
  }
]
```

### Projects
```
GET /projects
GET /projects?skill=<skill_name>
GET /projects?limit=<limit>&offset=<offset>
```
**Pagination Parameters:**
- `limit`: Number of projects per page (1-100, default: 10)
- `offset`: Number of projects to skip (default: 0)

**Example with pagination:**
```
GET /projects?limit=3&offset=0  # First page, 3 projects
GET /projects?limit=3&offset=3  # Second page, 3 projects
```
**Example response:**
```json
[
  {
    "id": 1,
    "title": "E-Commerce Platform",
    "description": "A full-stack e-commerce platform...",
    "github_url": "https://github.com/yourusername/ecommerce-platform",
    "live_url": "https://ecommerce-demo.com",
    "skills": [
      {
        "id": 1,
        "name": "React",
        "level": "Advanced"
      }
    ]
  }
]
```

### Search
```
GET /search?q=<query>
```
Searches across project titles, descriptions, and skill names.
**Example response:**
```json
[
  {
    "type": "project",
    "id": 1,
    "title": "E-Commerce Platform",
    "description": "A full-stack e-commerce platform..."
  },
  {
    "type": "skill",
    "id": 1,
    "title": "React",
    "description": "Skill level: Advanced"
  }
]
```

## Local Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if needed (defaults to SQLite).

5. **Run the backend:**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

6. **Access API documentation:**
   Open `http://localhost:8000/docs` in your browser

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Open the HTML file:**
   ```bash
   # Simply open index.html in your browser
   # Or use a simple HTTP server
   python -m http.server 3000
   ```
   Then open `http://localhost:3000`

3. **Configure API URL:**
   Edit `frontend/script.js` and update `API_BASE_URL` if your backend runs on a different port or URL.

## Deployment Instructions (Render)

### Backend Deployment

1. **Create a new Web Service on Render**
2. **Connect your GitHub repository**
3. **Set the following environment variables:**
   - `PYTHON_VERSION`: `3.10.0` (or newer)
4. **Configure Build Command:**
   ```bash
   cd backend && pip install -r requirements.txt
   ```
5. **Configure Start Command:**
   ```bash
   cd backend && python main.py
   ```
6. **Set the instance type to Free (or paid for production)**

### Frontend Deployment

1. **Create a new Static Site on Render**
2. **Connect your GitHub repository**
3. **Set Publish Directory to:** `frontend`
4. **Add Build Command (optional):**
   ```bash
   # No build step needed for vanilla HTML/JS
   echo "No build required"
   ```

### Important Notes for Production

1. **Update frontend API URL:**
   - Edit `frontend/script.js`
   - Change `API_BASE_URL` to your deployed backend URL
   - Commit and push the changes

2. **CORS Configuration:**
   - The backend allows all origins (`*`) for simplicity
   - For production, consider restricting to your frontend domain

3. **Database Persistence:**
   - Render's free tier uses ephemeral storage
   - Consider upgrading to paid tier for persistent SQLite storage
   - Or migrate to PostgreSQL for production

## Advanced Features

### 🔐 API Key Authentication
The API implements simple authentication for write operations:
- **Public endpoints**: All GET endpoints (profile, skills, projects, search)
- **Protected endpoints**: PUT /profile (requires API key)
- **API Key**: Set via `API_KEY` environment variable
- **Header**: `X-API-Key: your-api-key`

This demonstrates real-world security patterns while keeping the implementation simple.

### 📄 Pagination
Projects endpoint supports efficient pagination for large datasets:
- **Parameters**: `limit` (1-100), `offset` (0+)
- **Default**: 10 projects per page
- **Frontend**: "Load More" button for smooth UX
- **Use Case**: Handles thousands of projects efficiently

**Examples:**
```bash
GET /projects?limit=5&offset=0    # First 5 projects
GET /projects?limit=5&offset=5    # Next 5 projects
GET /projects?skill=Python&limit=3 # Filtered + paginated
```

## Known Limitations

- **No Authentication**: API is completely open as per requirements
- **Single Profile**: System designed for one person's profile only
- **SQLite Limitations**: Not ideal for high-concurrency production use
- **No File Uploads**: Profile images or project assets not supported
- **Basic Search**: Simple text search without advanced ranking
- **No Rate Limiting**: API endpoints are not rate-limited
- **Ephemeral Data**: Database resets on each deployment (free tier)

## Customization

### Updating Personal Information

1. **Edit the seed data:**
   - Open `backend/seed.py`
   - Replace placeholder values with your actual information
   - Redeploy or restart the backend

2. **Or use the API:**
   ```bash
   # Update profile via API
   curl -X PUT http://localhost:8000/profile \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Your Name",
       "email": "your.email@example.com",
       "education": "Your Education",
       "bio": "Your bio",
       "github": "https://github.com/yourusername",
       "linkedin": "https://linkedin.com/in/yourprofile",
       "portfolio": "https://yourportfolio.com"
     }'
   ```

### Adding Custom Skills or Projects

1. **Via API:**
   - Use the FastAPI docs at `/docs` to interact with endpoints
   - Currently requires direct database manipulation for adding new skills/projects

2. **Via Database:**
   - Access the SQLite database directly
   - Add records to `skills` and `projects` tables
   - Link them in `project_skills` table

## Live Deployment Links

### Backend API
🔗 **https://predusk-assessment-track-a.onrender.com**

- **API Documentation**: https://predusk-assessment-track-a.onrender.com/docs
- **Health Check**: https://predusk-assessment-track-a.onrender.com/health

### Frontend
🔗 **https://predusk-assessment-track-a-1.onrender.com**

Interactive web interface to explore profile, projects, skills, and search functionality.

## Resume Link

📄 [Resume - Alagu Shruthi](https://drive.google.com/file/d/1wabhV-XT5r353DX4HyIGkwbMrTWI9Sqz/view?usp=sharing)

## Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the error messages in browser console
3. Verify backend is running and accessible
4. Ensure CORS is properly configured

---

**Built with ❤️ for the internship assessment**
