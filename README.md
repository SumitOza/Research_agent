# Research Agent Web Application

A dynamic web application for conducting AI-powered research interviews using Cerebras API. The application allows users to input research topics, configure interview parameters, and receive comprehensive analysis with persona-based responses.

## Features

- **Cerebras API Integration**: Secure API key input for Cerebras LLM
- **Research Configuration**: 
  - Research topic input
  - Target demographic specification
  - Sample size (number of interviews)
  - Number of questions per interview
- **AI-Powered Interviews**: Automated persona generation and interview conduction
- **Comprehensive Analysis**: Synthesis of insights from all interviews
- **Detailed Results**: View questions, answers, and persona details

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── agent_workflow.py    # Core workflow logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styles
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: 
    `Set-ExecutionPolicy Bypass -Scope Process`
    `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the FastAPI server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Start the Backend**: Run the FastAPI server (port 8000)
2. **Start the Frontend**: Run the React development server (port 3000)
3. **Open Browser**: Navigate to `http://localhost:3000`
4. **Fill the Form**:
   - Enter your Cerebras API key
   - Input research topic
   - Specify target demographic
   - Set sample size (1-20 interviews)
   - Set number of questions (1-10 per interview)
5. **Run Research**: Click "Start Research" and wait for results
6. **View Results**: 
   - See the synthesis/analysis automatically
   - Click "Show Questions & Answers" to view detailed interview data

## API Endpoints

### POST `/api/research`

Execute research workflow.

**Request Body:**
```json
{
  "api_key": "your-cerebras-api-key",
  "research_topic": "Impact of aging population",
  "target_demographic": "Healthcare professionals aged 30-50",
  "sample_size": 4,
  "num_questions": 4
}
```

**Response:**
```json
{
  "success": true,
  "message": "Research completed successfully",
  "synthesis": "Analysis text...",
  "interviews": [...],
  "questions": [...]
}
```

## Technologies Used

- **Backend**: FastAPI, LangChain, LangGraph, Cerebras API
- **Frontend**: React, Vite, Axios
- **Styling**: CSS3 with modern gradients and responsive design

## Notes

- The application uses the Cerebras `llama3.3-70b` model
- Sample size is limited to 1-20 interviews for performance
- Questions per interview are limited to 1-10
- Processing time depends on sample size and number of questions

## Troubleshooting

- **CORS Errors**: Ensure backend CORS is configured for frontend origin
- **API Key Issues**: Verify your Cerebras API key is valid if you don't have a key get a free one at https://cloud.cerebras.ai/
- **Connection Errors**: Ensure backend is running before starting frontend
- **Port Conflicts**: Change ports in `main.py` (backend) or `vite.config.js` (frontend) if needed

