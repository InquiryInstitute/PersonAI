# PersonAI - Assignment 0

Welcome to PersonAI! This is your personal AI assistant that you'll develop throughout the semester.

## Assignment Overview

In this assignment, you will:

1. Fork this repository through GitHub Classroom
2. Set up your development environment
3. Configure your PersonAI instance
4. Test the chat interface
5. Connect to your first GitHub repository

## Setup Instructions

### Prerequisites

- Node.js 20 or higher
- Python 3.11 or higher
- A GitHub personal access token
- Git installed on your machine

### Step 1: Clone Your Repository

After accepting the assignment, clone your forked repository:

```bash
git clone https://github.com/YOUR-CLASSROOM-ORG/YOUR-USERNAME-personAI.git
cd YOUR-USERNAME-personAI
```

### Step 2: Set Up the Backend

1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Start the backend server:

```bash
python main.py
```

The backend should now be running on http://localhost:8080

### Step 3: Set Up the Frontend

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

4. Open your browser to http://localhost:5173

### Step 4: Connect to GitHub

1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a name like "PersonAI"
   - Select scopes: `repo`, `read:user`, `user:email`
   - Copy the token

2. In PersonAI:
   - Paste your token in the "GitHub Token" field
   - Enter a repository name (format: `username/repo`)
   - Click "Connect"

### Step 5: Test Your Setup

1. Try asking PersonAI a question:
   - "What files are in this repository?"
   - "Explain what the main.py file does"

2. Open a file in the Monaco Editor:
   - Click on a file in the sidebar
   - View and edit the code

## Submission

To submit your assignment:

1. Make sure both frontend and backend are working
2. Take screenshots of:
   - Your PersonAI chat interface
   - A file open in the Monaco Editor
   - The chat showing a response about your connected repository

3. Create a file called `SUBMISSION.md` with:
   - Your name
   - Screenshots
   - Brief description of what you learned

4. Commit and push:

```bash
git add SUBMISSION.md
git commit -m "Complete Assignment 0"
git push
```

## Grading Criteria

- [ ] Backend server runs successfully (20 points)
- [ ] Frontend loads and displays chat interface (20 points)
- [ ] Successfully connected to a GitHub repository (20 points)
- [ ] Can view files in Monaco Editor (20 points)
- [ ] Chat responds to queries (20 points)

## Getting Help

- Check the [README.md](README.md) for more details
- Post questions in the class discussion forum
- Attend office hours
- Check the [GitHub Issues](https://github.com/InquiryInstitute/personAI/issues)

## Next Steps

In future assignments, you'll:
- Add custom tools as submodules
- Implement file editing capabilities
- Connect to additional data sources
- Train PersonAI on your coding patterns

Good luck! 🚀
