# Project Structure

## Overview
This is a full-stack web application for conducting AI-powered research interviews using Cerebras API. The application consists of a FastAPI backend and a React frontend.

## Directory Structure

```
.
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI application and API endpoints
│   ├── agent_workflow.py      # Core workflow logic (extracted from notebook)
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # Component styles
│   │   ├── main.jsx          # React entry point
│   │   └── index.css         # Global styles
│   ├── index.html            # HTML template
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
│
├── start_backend.bat          # Windows script to start backend
├── start_frontend.bat         # Windows script to start frontend
├── start_backend.sh           # Linux/Mac script to start backend
├── start_frontend.sh          # Linux/Mac script to start frontend
├── README.md                  # Main documentation
├── QUICKSTART.md             # Quick start guide
└── .gitignore                # Git ignore file

```

## Key Components

### Backend (`backend/`)

1. **main.py**
   - FastAPI application setup
   - CORS middleware configuration
   - API endpoint: `/api/research` (POST)
   - Request/Response models

2. **agent_workflow.py**
   - Extracted logic from Jupyter notebook
   - State management (InterviewState)
   - Node functions:
     - `config_node`: Generates interview questions
     - `persona_generation_node`: Creates personas
     - `interview_node`: Conducts interviews
     - `synthesis_node`: Analyzes results
   - Workflow builder and executor

### Frontend (`frontend/`)

1. **App.jsx**
   - Main React component
   - Form handling for user inputs
   - API integration with axios
   - Results display with toggle for details

2. **Styling**
   - Modern gradient design
   - Responsive layout
   - Clean UI with cards and sections

## Data Flow

1. User fills form in React frontend
2. Frontend sends POST request to `/api/research`
3. Backend executes workflow:
   - Generates questions
   - Creates personas
   - Conducts interviews
   - Synthesizes results
4. Backend returns JSON response
5. Frontend displays results

## API Endpoint

**POST** `/api/research`

Request:
```json
{
  "api_key": "string",
  "research_topic": "string",
  "target_demographic": "string",
  "sample_size": 1-20,
  "num_questions": 1-10
}
```

Response:
```json
{
  "success": true,
  "message": "string",
  "synthesis": "string",
  "interviews": [...],
  "questions": [...]
}
```

## Technologies

- **Backend**: FastAPI, LangChain, LangGraph, Cerebras API
- **Frontend**: React, Vite, Axios
- **Language**: Python 3.11+, JavaScript (ES6+)

