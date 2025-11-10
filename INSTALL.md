# 📦 Installation Guide - MAXIMUS Personal Assistant

Complete installation instructions for all platforms.

---

## 🚀 Quick Install (Recommended)

### Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Anthropic API key

### Steps

```bash
# 1. Clone repository
cd "/home/maximus/MAXIMUS AI"
cd maximus-personal-assistant

# 2. Install package
pip install -e .

# 3. Configure API key
export ANTHROPIC_API_KEY="your-api-key-here"

# 4. Run!
maximus-pa
```

---

## 🐧 Linux Installation

### Ubuntu/Debian

```bash
# Install Python 3.8+
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Clone repository
cd "/home/maximus/MAXIMUS AI"
cd maximus-personal-assistant

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install package
pip install -e .

# Configure
export ANTHROPIC_API_KEY="your-api-key"

# Run
maximus-pa
```

### Fedora/RHEL/CentOS

```bash
# Install Python
sudo dnf install python3 python3-pip git

# Rest is same as Ubuntu
cd "/home/maximus/MAXIMUS AI/maximus-personal-assistant"
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Arch Linux

```bash
# Install Python
sudo pacman -S python python-pip git

# Same as above
cd "/home/maximus/MAXIMUS AI/maximus-personal-assistant"
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## 🍎 macOS Installation

### Using Homebrew

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3 git

# Clone and install
cd ~/MAXIMUS-AI
cd maximus-personal-assistant
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Configure
export ANTHROPIC_API_KEY="your-api-key"

# Run
maximus-pa
```

---

## 🪟 Windows Installation

### Using PowerShell

```powershell
# Install Python from python.org
# Download: https://www.python.org/downloads/

# Clone repository
cd C:\MAXIMUS-AI
cd maximus-personal-assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install
pip install -e .

# Configure (PowerShell)
$env:ANTHROPIC_API_KEY = "your-api-key"

# Run
maximus-pa
```

### Using Command Prompt

```cmd
cd C:\MAXIMUS-AI\maximus-personal-assistant
python -m venv venv
venv\Scripts\activate.bat
pip install -e .
set ANTHROPIC_API_KEY=your-api-key
maximus-pa
```

---

## 🐳 Docker Installation (Optional)

```bash
# Build image
docker build -t maximus-pa .

# Run container
docker run -it \
  -e ANTHROPIC_API_KEY="your-api-key" \
  -v $(pwd)/data:/app/data \
  maximus-pa
```

---

## 📋 Detailed Installation Options

### Option 1: Development Installation (Recommended for contributors)

```bash
# Clone repository
git clone https://github.com/JuanCS-Dev/maximus-personal-assistant.git
cd maximus-personal-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install with dev dependencies
pip install -e ".[dev]"

# Install additional tools
pip install pre-commit
pre-commit install

# Run tests
pytest
```

### Option 2: User Installation (For end users)

```bash
# Install directly from GitHub
pip install git+https://github.com/JuanCS-Dev/maximus-personal-assistant.git

# Or install from PyPI (when published)
pip install maximus-personal-assistant

# Run
maximus-pa
```

### Option 3: Minimal Installation (Core only)

```bash
# Install minimal dependencies
pip install anthropic requests aiohttp

# Clone repository
git clone https://github.com/JuanCS-Dev/maximus-personal-assistant.git
cd maximus-personal-assistant

# Run directly
python3 -m maximus_pa.cli
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional
CLICKUP_API_TOKEN=pk_...
GITHUB_USERNAME=YourUsername
MAXIMUS_CORE_URL=http://localhost:8150
MABA_URL=http://localhost:8152
```

### Or export directly:

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="your-key"
export CLICKUP_API_TOKEN="your-token"

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your-key"
$env:CLICKUP_API_TOKEN = "your-token"

# Windows CMD
set ANTHROPIC_API_KEY=your-key
set CLICKUP_API_TOKEN=your-token
```

### Persistent Configuration (Linux/Mac)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# MAXIMUS Personal Assistant
export ANTHROPIC_API_KEY="your-key-here"
export CLICKUP_API_TOKEN="your-token-here"
export GITHUB_USERNAME="YourUsername"

# Optional: Alias
alias mpa="maximus-pa"
```

---

## ✅ Verify Installation

```bash
# Check version
maximus-pa --version

# Check status
maximus-pa --status

# Run tests
pytest tests/

# Or run simple test
python3 -c "from maximus_pa import MaximusPersonalAssistant; print('✅ Import successful!')"
```

---

## 🔧 Troubleshooting

### Problem: "command not found: maximus-pa"

**Solution:**
```bash
# Make sure you installed with pip
pip install -e .

# Or run directly
python3 -m maximus_pa.cli
```

### Problem: "No module named 'anthropic'"

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt
```

### Problem: "ANTHROPIC_API_KEY not configured"

**Solution:**
```bash
# Set environment variable
export ANTHROPIC_API_KEY="your-key"

# Or pass as argument
maximus-pa --api-key "your-key"
```

### Problem: "Permission denied"

**Solution:**
```bash
# Make CLI executable
chmod +x maximus_pa/cli.py

# Or use --break-system-packages on some Linux distros
pip install -e . --break-system-packages
```

### Problem: "Core/MABA not available"

**Solution:**
This is NOT an error! The assistant works perfectly without Core or MABA.
It will use fallback mode with basic validation.

To enable Core:
```bash
# Start MAXIMUS Core
cd "../services/core"
python3 -m uvicorn main:app --port 8150
```

To enable MABA:
```bash
# Start MABA
cd "../services/maba"
python3 -m uvicorn main:app --port 8152
```

---

## 📦 Updating

### Update from Git

```bash
cd maximus-personal-assistant
git pull origin main
pip install -e . --upgrade
```

### Update from PyPI (when published)

```bash
pip install --upgrade maximus-personal-assistant
```

---

## 🗑️ Uninstallation

```bash
# Uninstall package
pip uninstall maximus-personal-assistant

# Remove data (optional)
rm -rf data/*.db

# Remove virtual environment (if used)
rm -rf venv/
```

---

## 🆘 Get Help

- **Documentation:** [docs/](docs/)
- **GitHub Issues:** https://github.com/JuanCS-Dev/maximus-personal-assistant/issues
- **Quick Start:** [docs/QUICKSTART.md](docs/QUICKSTART.md)

---

**Installation complete! Ready to use your TRUE Personal Assistant!** 🎉

Run `maximus-pa` to get started!
