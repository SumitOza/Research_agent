# Quick Start Guide

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ and npm installed

## Quick Setup (5 minutes)

### Step 1: Setup Backend

Open a terminal and run:

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

Backend will start on `http://localhost:8000`

### Step 2: Setup Frontend

Open a **new terminal** and run:

```bash
cd frontend
npm install
npm run dev
```

Frontend will start on `http://localhost:3000`

### Step 3: Use the Application

1. Open your browser and go to `http://localhost:3000`
2. Fill in the form:
   - Enter your Cerebras API key
   - Enter research topic (e.g., "Impact of aging population")
   - Enter target demographic (e.g., "Healthcare professionals aged 30-50")
   - Set sample size (1-20)
   - Set number of questions (1-10)
3. Click "Start Research"
4. Wait for results (this may take a few minutes depending on sample size)
5. View the analysis and optionally click "Show Questions & Answers" for details

## Using Startup Scripts (Windows)

Double-click:
- `start_backend.bat` - Starts the backend server
- `start_frontend.bat` - Starts the frontend (in a new window)

## Using Startup Scripts (Linux/Mac)

Make scripts executable:
```bash
chmod +x start_backend.sh start_frontend.sh
```

Then run:
```bash
./start_backend.sh    # In one terminal
./start_frontend.sh   # In another terminal
```

## Troubleshooting

**Backend won't start:**
- Make sure Python 3.11+ is installed
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Frontend won't start:**
- Make sure Node.js 18+ is installed
- Check if port 3000 is already in use
- Try deleting `node_modules` and running `npm install` again

**API errors:**
- Verify your Cerebras API key is correct
- Check that the backend is running on port 8000
- Check browser console for CORS errors

**Connection errors:**
- Ensure backend is running before starting frontend
- Check firewall settings
- Verify ports 8000 and 3000 are not blocked

