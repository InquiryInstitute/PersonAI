# PersonAI - Project Summary

## 🎯 What We Built

PersonAI is a student-focused AI assistant designed for GitHub Classroom assignments. It provides:

1. **Web-based Chat Interface** - SvelteKit + TailwindCSS
2. **Monaco Code Editor** - View and edit files in browser
3. **GitHub Integration** - Connect to any repository
4. **MCP Tool Support** - Compatible with Continue/Cursor tools
5. **PWA Support** - Install on mobile devices
6. **Secure Authentication** - Passphrase-based local encryption
7. **OpenRouter Integration** - Baseline with Qwen 2.5 Coder 7B

## 📁 Project Structure

```
personAI/
├── frontend/                    # SvelteKit application
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/     # UI components
│   │   │   │   ├── ChatInterface.svelte
│   │   │   │   ├── ChatMessage.svelte
│   │   │   │   ├── Sidebar.svelte
│   │   │   │   ├── MonacoEditor.svelte
│   │   │   │   └── Auth.svelte
│   │   │   ├── mcp/           # MCP client
│   │   │   │   └── client.ts
│   │   │   └── auth.ts        # Authentication
│   │   ├── routes/            # Pages
│   │   │   ├── +layout.svelte
│   │   │   ├── +layout.ts
│   │   │   └── +page.svelte
│   │   └── app.css           # Global styles
│   ├── static/               # Static assets
│   │   ├── manifest.json     # PWA manifest
│   │   ├── service-worker.js # Service worker
│   │   └── .nojekyll        # GitHub Pages
│   ├── svelte.config.js      # SvelteKit config
│   ├── tailwind.config.js    # Tailwind config
│   └── package.json
│
├── connectors/                # Backend integrations
│   ├── __init__.py
│   ├── llm.py                # LLM providers (OpenRouter, OpenAI, Ollama)
│   ├── mcp.py                # MCP server manager
│   ├── github.py             # GitHub connector
│   ├── drive.py              # Google Drive connector
│   └── web.py                # Web search connector
│
├── finetuning/               # Real-time learning
│   ├── __init__.py
│   └── engine.py
│
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml        # GitHub Pages deployment
│   │   └── classroom.yml     # Autograding
│   └── classroom/
│       └── autograding.json  # Test configuration
│
├── docs/                     # Documentation
├── main.py                   # FastAPI backend
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── README.md                # Main documentation
├── ASSIGNMENT.md            # Student instructions
├── SETUP.md                 # Setup guide (mobile, VSCode)
└── LICENSE
```

## 🔑 Key Features

### Chat Interface
- Modern, responsive UI
- Markdown rendering with syntax highlighting
- Message history
- Streaming support (ready)
- Dark mode support

### Code Editor
- Monaco Editor integration
- Syntax highlighting for 30+ languages
- Read and edit files
- Save to GitHub (coming soon)

### GitHub Integration
- Browse repository files
- View file contents
- Connect to any public/private repo
- Token-based authentication

### Security
- Client-side passphrase encryption
- Local token storage
- No server-side credential storage
- PWA security model

### MCP Compatibility
- Compatible with Continue's MCP servers
- Filesystem tools
- GitHub tools
- Git operations
- Extensible architecture

## 🚀 Deployment

### GitHub Pages
- **URL**: https://inquiryinstitute.github.io/PersonAI
- **Status**: ✅ Enabled
- **Auto-deploy**: On push to main

### Mobile PWA
- Install from browser
- Offline-capable
- App-like experience
- Secure local storage

### Backend Options
1. **Serverless** (current) - Direct API calls
2. **Local** - Run `python main.py`
3. **Cloud** (future) - Deploy to Cloud Run, etc.

## 🎓 GitHub Classroom Integration

### Assignment 0
- Students fork the repository
- Set up frontend and backend
- Connect to GitHub
- Test chat and editor
- Submit screenshots

### Autograding
- Backend dependencies install
- Frontend builds successfully
- Submission file exists
- All checked via GitHub Actions

### Future Assignments
Students will add:
- Assignment 1: File operations tool (submodule)
- Assignment 2: Code analysis tool
- Assignment 3: Testing automation
- Assignment 4: Custom fine-tuning

## 🧠 LLM Configuration

### Baseline: Qwen 2.5 Coder 7B via OpenRouter

**Why this model:**
- Excellent for coding tasks
- 7B parameters = fast responses
- Cost-effective via OpenRouter
- Strong context understanding
- Good at following instructions

**Configuration:**
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=qwen/qwen2.5-coder-7b-instruct
```

**Alternatives supported:**
- OpenAI (GPT-4, GPT-3.5)
- Ollama (local models)
- Any OpenAI-compatible API

## 📱 Mobile Usage

### Supported Features
- ✅ Chat interface
- ✅ File browsing
- ✅ Code viewing
- ✅ Monaco Editor
- ✅ Markdown rendering
- ⚠️ Large file editing (limited)

### Installation
1. Visit URL in mobile browser
2. "Add to Home Screen"
3. Enter passphrase
4. Add GitHub token
5. Start coding!

## 🔧 Development

### Local Development

**Backend:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py  # Port 8080
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev  # Port 5173
```

### Production Build

```bash
cd frontend
npm run build
# Output: frontend/build/
```

## 📊 Tech Stack

### Frontend
- **Framework**: SvelteKit 2.x
- **Styling**: TailwindCSS 4.x
- **Editor**: Monaco Editor
- **Markdown**: Marked + DOMPurify
- **GitHub**: Octokit REST
- **Build**: Vite

### Backend
- **Framework**: FastAPI
- **LLM**: OpenRouter, OpenAI, Ollama
- **HTTP**: httpx
- **GitHub**: PyGithub
- **Google**: google-api-python-client
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers

## 🎯 Next Steps

### Immediate
1. Test deployment on GitHub Pages
2. Verify mobile PWA installation
3. Add placeholder icons (192x192, 512x512)
4. Test with students

### Short Term
1. VSCode extension development
2. Streaming chat responses
3. File save to GitHub
4. Multiple file tabs
5. Search across files

### Long Term
1. Voice input support
2. Collaborative features
3. Offline mode
4. End-to-end encryption
5. Native mobile apps

## 📈 Success Metrics

For students:
- Time to first successful chat: < 10 minutes
- Repository connection success rate: > 90%
- Mobile usability score: > 4/5
- Assignment completion rate: > 85%

For instructors:
- Deployment success: 100% automated
- Grading accuracy: 100% via autograding
- Support tickets: < 10% of students
- Student satisfaction: > 4/5

## 🤝 Contributing

Students can contribute:
- Bug reports and fixes
- Feature requests
- Documentation improvements
- Tool submodules
- UI/UX enhancements

## 📄 License

MIT License - Students can fork, modify, and extend freely.

## 🙏 Credits

- Built with SvelteKit, TailwindCSS, Monaco Editor
- Compatible with Continue's MCP architecture
- Inspired by HuggingFace Chat UI
- Part of Inquiry Institute's Sovereign AI Certificate

---

**Ready to deploy!** 🚀

URL: https://inquiryinstitute.github.io/PersonAI
