# GitHub Codespaces Setup

PersonAI is designed to run seamlessly in GitHub Codespaces, providing a complete development environment in your browser.

## Quick Start

### 1. Open in Codespaces

Click the green "Code" button on GitHub → "Codespaces" → "Create codespace on main"

Or use this URL:
```
https://github.com/InquiryInstitute/PersonAI/codespaces
```

### 2. Configure Environment

The Codespace will automatically:
- Install Python dependencies
- Install Node.js dependencies
- Forward ports 8080 (backend) and 5173 (frontend)

Add your GitHub OAuth credentials to `.env`:
```bash
GITHUB_CLIENT_ID=Ov23liDA7zxsT4FkKh5Y
GITHUB_CLIENT_SECRET=your_secret_here
```

### 3. Start PersonAI

Run the startup script:
```bash
./start-codespace.sh
```

Or start services manually:
```bash
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4. Access the App

1. Click the "Ports" tab in VS Code
2. Find port 5173 (Frontend)
3. Click the globe icon to open in browser
4. The frontend will automatically connect to the backend on port 8080

## Port Forwarding

Codespaces automatically forwards these ports:

- **8080**: Backend API (FastAPI)
  - Public visibility for OAuth callbacks
  - URL format: `https://username-repo-xxxx.preview.app.github.dev`

- **5173**: Frontend (Vite)
  - Opens automatically in browser
  - URL format: `https://username-repo-xxxx.preview.app.github.dev`

## GitHub OAuth in Codespaces

The frontend automatically detects Codespace URLs and configures the API endpoint.

### Update OAuth App Callback

For device flow, no callback URL changes needed! Just ensure your OAuth app is configured with:
- Homepage URL: Your GitHub Pages URL
- Callback URL: `http://localhost` (required but unused for device flow)

## Environment Variables

Create `.env` in the root:

```bash
# GitHub OAuth (Device Flow)
GITHUB_CLIENT_ID=Ov23liDA7zxsT4FkKh5Y
GITHUB_CLIENT_SECRET=your_secret_here

# LLM Configuration (optional)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=qwen/qwen2.5-coder-7b-instruct

# Application Settings
PORT=8080
LOG_LEVEL=INFO
```

## Codespace Features

### Pre-installed Extensions
- Python
- Pylance
- Ruff (Python linter)
- Svelte
- Tailwind CSS

### Auto-configuration
- Python 3.11
- Node.js 20
- GitHub CLI
- Port forwarding
- Format on save

## Development Workflow

### Making Changes

1. Edit code in the Codespace
2. Changes auto-reload in both frontend and backend
3. Test using the forwarded URLs
4. Commit and push when ready

### Testing OAuth

1. Start the services
2. Open the frontend URL from Ports tab
3. Click "Continue with GitHub"
4. Copy the device code
5. Authorize on GitHub
6. You're authenticated!

### Debugging

View logs in the terminal:
```bash
# Backend logs
# Shows in Terminal 1

# Frontend logs  
# Shows in Terminal 2
```

## Codespace Lifecycle

### Stopping
Codespaces auto-stop after 30 minutes of inactivity (configurable)

### Restarting
When you reopen a Codespace:
1. Dependencies are already installed
2. Run `./start-codespace.sh` to start services
3. Ports are automatically forwarded

### Deleting
Codespaces are free for public repos. Delete unused ones from:
https://github.com/codespaces

## Tips & Tricks

### Multiple Terminals
Use VS Code's split terminal feature:
- `Ctrl+Shift+5` (Windows/Linux)
- `Cmd+Shift+5` (Mac)

### Port Visibility
Make ports public for external access:
1. Right-click port in Ports tab
2. Select "Port Visibility" → "Public"

### Environment Secrets
Store secrets in GitHub Codespaces settings:
1. Go to repository Settings → Secrets → Codespaces
2. Add secrets (they'll be available as environment variables)

### Prebuilds
Enable prebuilds for faster Codespace startup:
1. Repository Settings → Codespaces
2. Set up prebuild configuration
3. Codespaces will start in seconds!

## Troubleshooting

### Backend not starting
```bash
# Check if port 8080 is in use
lsof -i :8080

# Restart backend
pkill -f "python main.py"
python main.py
```

### Frontend can't connect to backend
1. Check Ports tab - ensure 8080 is forwarded
2. Verify API_URL in browser console
3. Make port 8080 public if needed

### OAuth not working
1. Ensure `.env` has correct credentials
2. Check backend logs for errors
3. Verify GitHub OAuth app is configured

### Dependencies missing
```bash
# Reinstall Python deps
pip install -r requirements.txt

# Reinstall Node deps
cd frontend
rm -rf node_modules
npm install
```

## For Students

### Assignment Workflow

1. Accept GitHub Classroom assignment
2. Open your forked repo in Codespaces
3. Add your OAuth credentials to `.env`
4. Start developing!
5. Test in the Codespace
6. Push changes to deploy to GitHub Pages

### Collaboration

Share your Codespace URL with instructors:
1. Make ports public
2. Share the forwarded URL
3. They can test your app without cloning

## Resources

- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [VS Code in Browser](https://code.visualstudio.com/docs/remote/codespaces)
- [Codespaces Pricing](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)
