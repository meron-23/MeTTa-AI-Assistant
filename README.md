# MeTTa-AI-Assistant

## Running the Backend

### 1. Clone the repository

```bash
git clone https://github.com/iCog-Labs-Dev/MeTTa-AI-Assistant
cd MeTTa-AI-Assistant/Backend
```

### 2. Set up environment

```bash
cp .env.example .env
# Update .env with your values
```

### 3. Build and run using Docker

```bash
docker-compose up --build
```

This will start the FastAPI server on http://localhost:8000.

### 4. Run locally (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```

Note: Remove the --reload flag in production.
