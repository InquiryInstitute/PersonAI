# PersonAI

A personal AI assistant designed for students to fork, customize, and develop throughout their coursework. Built with modern web technologies and compatible with Continue/Cursor MCP tools.

## 🎓 For Students

This repository serves as the base for **Assignment 0** in the Sovereign AI Certificate program. Each student will fork this repo through GitHub Classroom and develop their own PersonAI throughout the semester.

**See [ASSIGNMENT.md](ASSIGNMENT.md) for detailed assignment instructions.**

## ✨ Features

- **Modern Chat Interface**: Clean, responsive UI built with SvelteKit and TailwindCSS
- **Monaco Editor Integration**: View and edit code files directly in the browser
- **GitHub Integration**: Connect to any GitHub repository and browse files
- **MCP Tool Support**: Compatible with Continue's Model Context Protocol (MCP) tools
- **Real-time Fine-tuning**: Learn from your interactions (optional)
- **Privacy First**: All data access is scoped to your authenticated accounts
- **GitHub Pages Deployment**: Deploy your PersonAI as a static site

## 🏗️ Architecture

```
personAI/
├── frontend/              # SvelteKit web interface
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/    # Chat, Editor, Sidebar components
│   │   │   └── mcp/          # MCP client integration
│   │   └── routes/           # Pages and layouts
│   └── static/              # Static assets
├── connectors/           # Backend data connectors
│   ├── github.py        # GitHub API integration
│   ├── drive.py         # Google Drive integration
│   ├── web.py           # Web search
│   └── mcp.py           # MCP server manager
├── finetuning/          # Real-time learning engine
└── main.py              # FastAPI backend server
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ (for frontend)
- **Python** 3.11+ (for backend)
- **Git**
- **GitHub Account** with personal access token

### 1. Clone the Repository

```bash
# For GitHub Classroom students:
# Accept the assignment link, then clone your forked repo

# For direct use:
git clone https://github.com/InquiryInstitute/personAI.git
cd personAI
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start backend server
python main.py
```

Backend runs on **http://localhost:8080**

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on **http://localhost:5173**

### 4. Connect to GitHub

1. Get a GitHub Personal Access Token:
   - Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Scopes: `repo`, `read:user`, `user:email`

2. In PersonAI interface:
   - Enter your token
   - Enter repository (format: `username/repo`)
   - Click Connect

## 📚 Usage Guide

### Chat Interface

Ask PersonAI questions about your code:

```
"What files are in this repository?"
"Explain the main.py file"
"Show me all Python files"
"What does the ChatInterface component do?"
```

### File Editor

- Click any file in the sidebar to open it
- Edit code in the Monaco Editor
- Save changes (coming soon: direct GitHub commits)

### MCP Tools

PersonAI is compatible with Continue's MCP ecosystem. Available tools include:

- **Filesystem**: Read and write local files
- **GitHub**: Advanced repository operations
- **Git**: Version control operations

Configure MCP servers in the backend's `connectors/mcp.py`.

## 🎨 Customization

### Adding Custom Tools

Students will add custom tools as git submodules in future assignments:

```bash
git submodule add <your-tool-repo-url> tools/<tool-name>
```

### Styling

Customize the theme in `frontend/src/app.css`:

```css
:root {
  --color-primary: /* your color */;
}
```

### Backend Extensions

Add new connectors in the `connectors/` directory following the existing patterns.

## 🌐 Deployment

### GitHub Pages

PersonAI automatically deploys to GitHub Pages when you push to main:

1. Enable GitHub Pages in repository settings
2. Source: GitHub Actions
3. Push to main branch
4. Visit: `https://yourusername.github.io/personAI/`

### Local Development

```bash
# Backend
python main.py

# Frontend
cd frontend && npm run dev
```

### Production Build

```bash
# Frontend
cd frontend
npm run build

# Serve with any static file server
npx serve build
```

## 🔧 Configuration

### Environment Variables

Create `.env` in the root directory:

```bash
# API Keys
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Server Configuration
PORT=8080
READ_ONLY_MODE=true

# Fine-tuning (optional)
FINETUNING_ENABLED=false
FINETUNING_BACKEND=mlx
```

### Frontend Configuration

Edit `frontend/svelte.config.js` for deployment settings.

## 📦 Submodules for Future Assignments

Throughout the semester, students will add tools as submodules:

- **Assignment 1**: File operations tool
- **Assignment 2**: Code analysis tool
- **Assignment 3**: Testing automation tool
- **Assignment 4**: Custom AI model fine-tuning

## 🧪 Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

## 🐛 Troubleshooting

### Backend won't start

- Check Python version: `python --version` (need 3.11+)
- Verify virtual environment is activated
- Check port 8080 is available

### Frontend build fails

- Check Node version: `node --version` (need 20+)
- Delete `node_modules` and reinstall: `npm ci`
- Check for Monaco Editor issues

### GitHub connection fails

- Verify token has correct permissions
- Check repository format: `owner/repo`
- Ensure repository exists and is accessible

## 🤝 Contributing

This is an educational project. Students should:

1. Work on their forked repository
2. Submit via GitHub Classroom
3. Share interesting extensions via pull requests

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🎓 Course Information

Part of the [Sovereign AI Certificate](https://github.com/InquiryInstitute/sovereign) program by Inquiry Institute.

### Instructors

- Course website: [Inquiry Institute](https://inquiryinstitute.org)
- GitHub: [@InquiryInstitute](https://github.com/InquiryInstitute)

## 📞 Support

- **Assignment Help**: Check ASSIGNMENT.md
- **Issues**: [GitHub Issues](https://github.com/InquiryInstitute/personAI/issues)
- **Discussions**: Use the class forum
- **Office Hours**: Schedule via course website

## 🗺️ Roadmap

### Current (v0.2.0)
- ✅ Chat interface
- ✅ Monaco Editor
- ✅ GitHub integration
- ✅ MCP compatibility
- ✅ GitHub Pages deployment

### Coming Soon
- 🔄 Direct GitHub commits from editor
- 🔄 Multiple file tabs
- 🔄 Code search and navigation
- 🔄 Voice input support
- 🔄 Team collaboration features

## 🙏 Acknowledgments

- Built with [SvelteKit](https://kit.svelte.dev/)
- Editor by [Monaco Editor](https://microsoft.github.io/monaco-editor/)
- Compatible with [Continue](https://continue.dev/)
- Inspired by [HuggingFace Chat UI](https://github.com/huggingface/chat-ui)

---

**Happy Coding!** 🚀 Build your own AI assistant and make it uniquely yours.
