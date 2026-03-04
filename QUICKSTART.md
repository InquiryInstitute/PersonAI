# PersonAI - Quick Start

## 🚀 For Students (Assignment 0)

### 1. Accept GitHub Classroom Assignment

Click the assignment link provided by your instructor to fork this repository.

### 2. Option A: Use GitHub Pages (Recommended for Mobile)

**Already deployed!** Just visit:
```
https://inquiryinstitute.github.io/PersonAI
```

1. Enter a secure passphrase
2. Get a GitHub token: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Scopes: `repo`, `read:user`, `user:email`
   - Copy the token

3. In PersonAI sidebar:
   - Paste your GitHub token
   - Enter a repository: `yourusername/your-repo`
   - Click "Connect"

4. Start chatting!

**Install as Mobile App:**
- iOS: Safari → Share → Add to Home Screen
- Android: Chrome → Menu → Add to Home Screen

### 2. Option B: Run Locally

**Backend:**
```bash
# Clone your forked repo
git clone https://github.com/YOUR-ORG/YOUR-USERNAME-personAI.git
cd YOUR-USERNAME-personAI

# Setup Python environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure (add your OpenRouter API key)
cp .env.example .env
nano .env  # or use your preferred editor

# Start backend
python main.py
# Backend runs on http://localhost:8080
```

**Frontend** (in a new terminal):
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend runs on http://localhost:5173
```

Open http://localhost:5173 in your browser!

## 🎯 First Steps

### Test the Chat
```
"Hello! What can you help me with?"
"Explain what a Python virtual environment is"
"What is the difference between git and GitHub?"
```

### Connect to a Repository
```
"Show me the files in my repository"
"What does the main.py file do?"
"Explain the README"
```

### Use the Editor
- Click any file in the sidebar
- View code with syntax highlighting
- Edit code (save feature coming soon)

## 📝 Submit Assignment

Create `SUBMISSION.md` with:

```markdown
# Assignment 0 Submission

**Name:** Your Name  
**Date:** Today's Date

## Screenshots

### Chat Interface
![Chat Screenshot](path-to-screenshot.png)

### Monaco Editor
![Editor Screenshot](path-to-screenshot.png)

### Connected Repository
![Repo Screenshot](path-to-screenshot.png)

## Reflection

1. What did you learn from this assignment?
2. What challenges did you face?
3. How do you plan to use PersonAI in future assignments?

## Repository Information

- Connected to: `username/repository`
- Number of files browsed: X
- Favorite feature: [Chat/Editor/GitHub Integration]
```

Then commit and push:
```bash
git add SUBMISSION.md
git commit -m "Complete Assignment 0"
git push
```

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check Python version (need 3.11+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check if port 8080 is available
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows
```

### Frontend build fails
```bash
# Check Node version (need 20+)
node --version

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### GitHub connection fails
- Check token hasn't expired
- Verify repository exists and is accessible
- Check token has correct permissions (`repo` scope)
- Try with a public repository first

### PWA won't install
- Use Safari on iOS (not Chrome)
- Use Chrome on Android
- Ensure you're on HTTPS
- Clear browser cache and try again

## 💡 Tips

1. **Keep your token safe** - Never commit it to git!
2. **Use a strong passphrase** - It encrypts your local data
3. **Try mobile** - Works great on phones and tablets
4. **Ask questions** - The AI is here to help you learn
5. **Explore repos** - Connect to different repositories to learn

## 📚 Learn More

- **Full Documentation**: [README.md](README.md)
- **Assignment Details**: [ASSIGNMENT.md](ASSIGNMENT.md)
- **Mobile & VSCode Setup**: [SETUP.md](SETUP.md)
- **Project Architecture**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 🎓 Next Assignments

In future assignments, you'll:
- Add custom tools as submodules
- Implement file editing with GitHub commits
- Connect to additional data sources
- Fine-tune PersonAI on your coding style

## 🤝 Get Help

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share tips
- **Office Hours**: See course website for schedule
- **Email**: Your instructor's email

## ✅ Success Checklist

- [ ] Backend runs successfully (or using GitHub Pages)
- [ ] Frontend displays chat interface
- [ ] Successfully connected to a GitHub repository
- [ ] Can view files in Monaco Editor
- [ ] Chat responds to queries
- [ ] Created SUBMISSION.md with screenshots
- [ ] Committed and pushed to GitHub

**Estimated Time:** 30-60 minutes

**Have fun building your Personal AI!** 🎉
