# AI Form Filler

An intelligent form processing application that uses AI to automatically fill forms by extracting text from images, understanding form fields, and generating appropriate responses through an interactive chat interface.

## Features

- **OCR Text Extraction**: Extract text from form images using AWS Textract or Tesseract
- **AI-Powered Form Understanding**: Uses AWS Bedrock (Claude) for form understanding
- **Multilingual Support**: Supports English, Hindi, and Marathi
- **Interactive Chat**: Conversational interface to gather user information
- **Form Annotation**: Automatically fills and annotates forms with user-provided data

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **AWS Services**: Textract (OCR), Bedrock (LLM)
- **Google Gemini**: ~~Vision model for form understanding~~ (Deprecated - using AWS Bedrock)
- **Ollama**: Local LLM for text generation (optional)
- **Tesseract**: OCR fallback

### Frontend
- **React**: UI framework
- **React Router**: Navigation
- **Axios**: HTTP client

## Prerequisites

Before setting up the project, ensure you have:

- **Python 3.9+** installed
- **Node.js 18+** installed
- **AWS Account** with required services

## Project Structure

```
AI-FormFiller/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main application
│   │   ├── aws_services.py # AWS Textract & Bedrock
│   │   ├── llm.py          # Ollama LLM integration
│   │   ├── ocr.py          # OCR functionality
│   │   └── annotation.py   # Form annotation
│   ├── uploads/            # Uploaded files
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
│
└── frontend/               # React frontend
    ├── src/
    │   ├── pages/         # Application pages
    │   ├── components/    # UI components
    │   ├── context/       # React context
    │   └── utils/         # Utilities
    └── package.json       # Node dependencies
```

---

## Setup Guide

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd AI-FormFiller
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

#### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# AWS Credentials (Required)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key

# AWS Region (Choose your preferred region)
AWS_REGION=us-east-1

# Ollama Configuration (Optional - for local LLM fallback)
OLLAMA_URL=http://localhost:11434/api/chat
OLLAMA_MODEL=mistral

# Debug Mode
DEBUG=true
```

> **Note**: See the "AWS Credentials Setup" section below for detailed instructions on creating AWS credentials.

#### 2.4 Install Tesseract OCR (Optional - for fallback)

**Windows:**
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH, or set environment variable:
```env
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Mac:**
```bash
brew install tesseract
```

**Linux (Ubuntu):**
```bash
sudo apt-get install tesseract-ocr
```

#### 2.5 Run the Backend

```bash
cd backend
venv\Scripts\uvicorn app.main:app --reload --port 8000
```

The backend will start at `http://localhost:8000`

### Step 3: Frontend Setup

#### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

#### 3.2 Run the Frontend

```bash
npm start
```

The frontend will start at `http://localhost:3000`

---

## AWS Setup Instructions

✅ Great news! Model access is now automatically enabled. Here's what you need to do:

### Step 1: Get AWS Credentials
1. Go to IAM → Users → Create a user (or select existing)
2. Go to Security credentials → Create access key
3. Copy:
   - Access Key ID
   - Secret Access Key

### Step 2: Add IAM Permissions
Attach these policies to your user:
- `AmazonTextractFullAccess` (for OCR)
- `AmazonBedrockFullAccess` (for LLM)

Or create inline policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockInvoke",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### Step 3: For Claude Models (First Time)
If this is your first time using Claude, you may need to:
1. Go to Amazon Bedrock → Model Catalog
2. Search for "Claude 3 Haiku"
3. Click on it → It may ask you to submit use case details
4. Submit a brief description (e.g., "Form analysis and document understanding")
5. Once approved, you can use it

### Step 4: Set Environment Variables
Create `backend/.env` file:
```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
```

Or on Windows command prompt:
```cmd
set AWS_ACCESS_KEY_ID=AKIA...
set AWS_SECRET_ACCESS_KEY=xxxxx...
set AWS_REGION=us-east-1
```

---

## Ollama Setup (Optional - Local LLM Fallback)

For local LLM processing instead of AWS Bedrock:

1. Download Ollama from: https://ollama.ai/
2. Install and run:
   ```bash
   ollama serve
   ```
3. Pull a model:
   ```bash
   ollama pull mistral
   ```

The backend will automatically use Ollama when AWS Bedrock is not configured.

---

## Running the Application

### Start Backend

```bash
cd backend
venv\Scripts\uvicorn app.main:app --reload --port 8000
```

### Start Frontend

```bash
cd frontend
npm start
```

### Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload form image |
| `/extract-text` | POST | Extract text from image |
| `/generate-questions` | POST | Generate questions from fields |
| `/explain-form` | POST | Explain form in user's language |
| `/submit-answers` | POST | Submit user answers |
| `/annotate` | POST | Generate annotated form |
| `/suggest-fields` | POST | Suggest fields from text |

---

## Troubleshooting

### Common Issues

**1. AWS Credentials Not Working**
- Verify credentials are correct in `.env`
- Check AWS region is correct
- Ensure IAM user has required permissions

**2. Textract Not Working**
- Confirm Textract is available in your AWS region
- Check if you've reached service limits
- Verify AWS credentials are correct

**3. Frontend Can't Connect to Backend**
- Verify backend is running on port 8000
- Check CORS settings
- Ensure no firewall blocking

**5. Ollama Connection Error**
- Ensure Ollama is running: `ollama serve`
- Check if model is installed: `ollama list`

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `AWS_ACCESS_KEY_ID` | Yes | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Yes | AWS secret key |
| `AWS_REGION` | Yes | AWS region (e.g., `us-east-1`) |
| `OLLAMA_URL` | No | Ollama server URL for local LLM fallback (default: `http://localhost:11434/api/chat`) |
| `OLLAMA_MODEL` | No | Ollama model name (default: `mistral`) |
| `DEBUG` | No | Debug mode (default: `true`) |
| `TESSERACT_CMD` | No | Path to Tesseract executable |

---

## License

MIT License

---

## Support

For issues and questions, please open an issue on the repository.
