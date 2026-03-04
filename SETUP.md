# PersonAI Setup Guide

## 📱 Mobile PWA Setup (iOS & Android)

PersonAI can be installed as a Progressive Web App (PWA) on your mobile device for on-the-go coding assistance.

### iOS (iPhone/iPad)

1. Open Safari and navigate to: `https://inquiryinstitute.github.io/PersonAI`
2. Tap the Share button (square with arrow pointing up)
3. Scroll down and tap "Add to Home Screen"
4. Name it "PersonAI" and tap "Add"
5. PersonAI will now appear as an app icon on your home screen

**First Launch:**
- Enter a secure passphrase (this encrypts your local data)
- Add your GitHub token in the sidebar
- Connect to your repositories

**Security Notes:**
- Your passphrase never leaves your device
- All data is stored encrypted in local storage
- Use Face ID/Touch ID lock on your device for additional security
- GitHub token is stored locally and never sent to external servers (except GitHub API)

### Android

1. Open Chrome and navigate to: `https://inquiryinstitute.github.io/PersonAI`
2. Tap the three-dot menu (⋮) in the top right
3. Tap "Add to Home screen" or "Install app"
4. Name it "PersonAI" and tap "Add"
5. PersonAI will appear in your app drawer

**Security:**
- Same security measures as iOS
- Use device PIN/biometric lock
- Consider using Samsung Secure Folder for extra protection

### Mobile Best Practices

- **Secure Passphrases**: Use a strong, memorable passphrase
- **Token Permissions**: Only grant minimum required GitHub permissions
- **Network Security**: Avoid public WiFi when accessing sensitive repos
- **Regular Logout**: Logout when using shared devices
- **Backup**: Keep your tokens and passphrases in a password manager

## 💻 VSCode Extension (for Codespaces)

PersonAI can be embedded directly in VSCode and GitHub Codespaces.

### Installation

```bash
# Coming soon - the extension will be available at:
code --install-extension inquiryinstitute.personai
```

### For Development (Current)

1. Clone the PersonAI repository
2. Add to your Codespace's `.devcontainer/devcontainer.json`:

```json
{
  "name": "PersonAI Codespace",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    },
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    }
  },
  "forwardPorts": [8080, 5173],
  "postCreateCommand": "pip install -r requirements.txt && cd frontend && npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "svelte.svelte-vscode",
        "ms-python.python"
      ]
    }
  }
}
```

3. Start backend in terminal 1:
```bash
python main.py
```

4. Start frontend in terminal 2:
```bash
cd frontend && npm run dev
```

5. Open the forwarded port 5173 in your browser

### VSCode Extension Features (Coming Soon)

- **Sidebar Panel**: PersonAI chat directly in VSCode sidebar
- **Inline Suggestions**: Get code suggestions as you type
- **File Context**: Automatically includes open files in context
- **Terminal Integration**: Run suggested commands directly
- **Git Integration**: Commit and push with AI-generated messages

## 🔐 Security Architecture

### Client-Side Encryption

```
User Passphrase → SHA-256 Hash → Local Storage Key
                                      ↓
GitHub Token → Encrypted with Key → Local Storage
```

### API Communication

```
Mobile/Desktop → HTTPS → GitHub API (with token)
                     ↓
              OpenRouter API (with separate key)
                     ↓
              Your Backend (optional)
```

### Best Practices

1. **Passphrase Management**
   - Use a strong, unique passphrase
   - Store in password manager
   - Change regularly (quarterly)

2. **Token Scope**
   - Only grant `repo`, `read:user`, `user:email`
   - Create separate tokens for different devices
   - Revoke unused tokens

3. **Network Security**
   - Always use HTTPS
   - Avoid public WiFi
   - Consider VPN for sensitive work

4. **Device Security**
   - Enable biometric locks
   - Use Find My Device features
   - Remote wipe capability

## 🏗️ Backend Options

### Option 1: GitHub Pages (Serverless)

- Frontend only
- Direct API calls to OpenRouter
- Best for: Personal use, students
- Cost: Free (with GitHub token limits)

### Option 2: Personal Backend

- Run backend on local machine/server
- Full control over API keys
- Best for: Development, testing
- Cost: Free (self-hosted)

### Option 3: Cloud Backend (Future)

- Deploy to Cloud Run, Lambda, etc.
- Shared instance for classroom
- Best for: Teams, institutions
- Cost: Pay-per-use

## 📊 Usage on Mobile

### Optimal Workflows

1. **Code Review**
   - Browse files in sidebar
   - Ask questions about code
   - View in Monaco Editor

2. **Quick Fixes**
   - Paste error messages
   - Get explanations and solutions
   - Copy code snippets

3. **Learning**
   - Ask conceptual questions
   - Explore project structure
   - Understand dependencies

### Mobile Limitations

- Monaco Editor works but is small
- Large files may be slow
- Git operations require GitHub token with write access
- Best for reading/reviewing, not heavy editing

## 🆘 Troubleshooting

### Mobile Issues

**PWA won't install:**
- Use Safari on iOS (not Chrome)
- Use Chrome on Android (not other browsers)
- Ensure you're on HTTPS

**Authentication fails:**
- Clear browser cache
- Check passphrase
- Try incognito/private mode first

**GitHub connection fails:**
- Verify token hasn't expired
- Check token permissions
- Ensure repository is accessible

### VSCode Extension Issues

**Extension not loading:**
- Check VSCode version (need 1.85+)
- Reload window (Cmd/Ctrl + Shift + P → Reload Window)
- Check extension host log

**Backend connection fails:**
- Verify port 8080 is forwarded
- Check firewall settings
- Ensure backend is running

## 🔄 Updates

### Mobile PWA

- Updates deploy automatically
- Refresh page to get latest version
- Clear cache if issues persist

### VSCode Extension

```bash
code --update-extensions inquiryinstitute.personai
```

## 📞 Support

- **Issues**: https://github.com/InquiryInstitute/personAI/issues
- **Discussions**: https://github.com/InquiryInstitute/personAI/discussions
- **Email**: support@inquiryinstitute.org
- **Office Hours**: See course website

## 🚀 Future Enhancements

- [ ] Offline mode with cached responses
- [ ] Voice input via Web Speech API
- [ ] Collaborative features (share chats)
- [ ] VS Code extension release
- [ ] Mobile app (React Native wrapper)
- [ ] Biometric authentication
- [ ] End-to-end encryption for cloud sync
