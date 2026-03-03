# personAI

A secure personal AI assistant that interacts with your own data across GitHub repositories, Google Shared Drive, and the web. Built with safety and privacy in mind.

## Overview

personAI enables you to ask questions and interact with your personal data using AI, similar to OpenClaw but with enhanced security controls. Your data stays under your control while being accessible to your personal AI assistant.

## Features

- **GitHub Integration**: Query and interact with files in your personal GitHub repositories
- **Google Drive Integration**: Access and search documents in your Google Shared Drive
- **Web Search**: Retrieve information from the web to augment your personal knowledge base
- **Privacy First**: All data access is scoped to your authenticated accounts
- **Secure by Design**: Built-in safety controls and permission management

## Deployment Options

### Primary: M4 Mac Mini (Recommended)
Run personAI on your own M4 Mac Mini for true data sovereignty. Leverages Apple Silicon for:
- Local LLM inference (Ollama, MLX)
- Zero cloud compute costs
- Complete privacy - data never leaves your hardware
- High performance with Apple Silicon optimizations

### Alternative: GitHub Codespaces
Deploy and run personAI in GitHub Codespaces for development and testing.

### Alternative: Google Cloud Run (GCR)
Deploy personAI as a serverless application on Google Cloud Run if cloud deployment is preferred.

## Getting Started

### Prerequisites

- M4 Mac Mini (or other Apple Silicon Mac)
- macOS 15+ (Sequoia)
- Python 3.11+ (included with macOS or via Homebrew)
- GitHub account with personal repositories
- Google Cloud account (for Drive access only)

### M4 Mac Mini Setup

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Clone the repository
git clone https://github.com/InquiryInstitute/personAI.git
cd personAI

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama for local LLM (optional but recommended)
brew install ollama

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Run as a service (stays running)
python main.py
```

### Run as Background Service (macOS)

Create a LaunchAgent to keep personAI running:

```bash
# See docs/macos-service.md for detailed instructions
```

### Alternative Deployments

**Codespaces**: Click "Code" → "Create codespace on main"  
**Google Cloud Run**: See `docs/gcr-deployment.md`

## Architecture

personAI uses:
- **LangChain** for AI orchestration and retrieval augmented generation (RAG)
- **GitHub API** for repository access
- **Google Drive API** for file access
- **Vector database** for efficient semantic search across your documents
- **Safety guardrails** to prevent unintended actions

## Security

- All API credentials are stored securely and never logged
- Fine-grained permission controls for data access
- Read-only mode by default for file operations
- Audit logging for all AI actions

## Certificate Program

This project is part of the [Sovereign AI Certificate](https://github.com/InquiryInstitute/sovereign) program offered by Inquiry Institute.

## License

MIT License - see LICENSE file for details
