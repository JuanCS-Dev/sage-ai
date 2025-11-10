# 🧠 MAXIMUS Personal Assistant

**The TRUE AI Personal Assistant - A Hybrid with Consciousness**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/JuanCS-Dev/maximus-personal-assistant)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/JuanCS-Dev/maximus-personal-assistant)

---

## 🎯 What Is This?

MAXIMUS Personal Assistant is **NOT just another AI assistant**.

It's a **revolutionary hybrid** that combines:

| Component | Source | Capability |
|-----------|--------|------------|
| 📝 **Organization** | Traditional AI assistants | Memory, notes, tasks |
| 💪 **Execution** | Real-life PAs | **DOING**, not just suggesting |
| 🧠 **Consciousness** | Max AI (MAXIMUS Core) | Ethics, safety, deep reasoning |
| ⚡ **Performance** | Monitoring system | High performance guaranteed |

---

## ⚡ Quick Start (< 5 minutes)

### 1. Install

```bash
git clone https://github.com/JuanCS-Dev/maximus-personal-assistant.git
cd maximus-personal-assistant
pip install -e .
```

### 2. Configure

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 3. Run

```bash
sage
# or short alias:
mpa
```

### 4. Use!

```
Você: status                    # Check status
Você: What should I do today?   # Daily planning
Você: execute roadmap.md        # Execute roadmap
```

**That's it! 🎉**

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for detailed instructions.

---

## 🔥 Key Features

### 1. 🧠 Hybrid Reasoning (Claude + Max AI)

```python
# User asks something
user: "Delete all old log files"

# 1. Claude understands intent
claude_response = "I'll delete logs older than 30 days..."

# 2. Max AI validates consciousness & safety
consciousness_check = await max_core.check_consciousness(action)

# 3. If dangerous, BLOCKS
if consciousness_check.safety_tier == SafetyTier.RISKY:
    return "⚠️ Potentially dangerous action. Requires approval."

# 4. If approved, EXECUTES
result = await execute_action(action)
```

**Result:** Assistant that THINKS before acting.

---

### 2. ⚡ Autonomous Execution

Can **EXECUTE tasks autonomously**:

```python
# Load and execute a complete roadmap
await assistant.load_and_execute_roadmap("launch_plan.md")

# What happens:
# 1. Claude analyzes the roadmap
# 2. Identifies automatable tasks
# 3. Max Core validates each task
# 4. MABA executes web navigation
# 5. ClickUp syncs progress
# 6. Saves notes automatically
```

**Supported execution types:**

| Type | Tool | Example |
|------|------|---------|
| 🌐 **Web Navigation** | MABA | Publish blog post, fill form |
| 📝 **File Operations** | File system | Create, edit, organize files |
| 🔌 **API Calls** | Requests | Integrate external services |
| 💬 **Communication** | ClickUp, GitHub | Create issues, tasks, comments |

---

### 3. 🛡️ Constitutional Validation

**Every action goes through multiple validation layers:**

#### Layer 1: Safety Check (Core)
```python
# Detects dangerous actions
dangerous_keywords = ["delete", "rm -rf", "sudo", "format", "drop"]
if any(keyword in action for keyword in dangerous_keywords):
    safety_tier = SafetyTier.RISKY
    requires_approval = True
```

#### Layer 2: Virtue Validation (Penelope)
```python
# Validates against 7 Virtues
guidance = await penelope.get_virtue_guidance(
    situation="Delete user's important file"
)
# Returns: { "virtue": "Prudence", "recommendation": "Ask first" }
```

#### Layer 3: Ethics Review (THEMIS)
```python
# Validates legality and ethics
ethics_check = await themis.validate_action(action)
# Ensures legal compliance
```

**Consciousness Levels:**

| Level | Description | Example |
|-------|-------------|---------|
| 🟢 **LOW** | Simple tasks, no impact | Search note, list tasks |
| 🟡 **MEDIUM** | Important tasks | Create ClickUp task |
| 🟠 **HIGH** | Critical decisions | Execute deploy script |
| 🔴 **CRITICAL** | Requires human approval | Delete data, destructive ops |

---

### 4. 📊 Performance Monitoring

**Real-time metrics:**

```python
# Performance Report
{
    "tasks_completed": 47,
    "tasks_failed": 2,
    "success_rate": "95.9%",
    "avg_task_time": "3.42s",
    "consciousness_checks": {
        "passed": 45,
        "failed": 2
    }
}
```

**Performance guarantees:**
- ✅ Average response < 5s
- ✅ Success rate > 95%
- ✅ Automatic fallback if services offline
- ✅ Graceful degradation

---

### 5. 💾 Deep Long-Term Memory

**Unlike traditional assistants:**

| Traditional Assistants | MAXIMUS PA |
|----------------------|------------|
| Session memory only | ✅ Persistent SQLite |
| No context between conversations | ✅ Complete context always |
| Forget projects | ✅ Knows all projects deeply |
| Don't learn | ✅ Learns from each interaction |

---

## 🔌 Integrations

### MAXIMUS Ecosystem (8 Services)

| Service | Port | Function | Use in PA |
|---------|------|----------|-----------|
| 🧠 **Core** | 8150 | Consciousness & Safety | Validation of all actions |
| 🍎 **Penelope** | 8151 | 7 Virtues & Healing | Ethical guidance |
| 🌐 **MABA** | 8152 | Browser Automation | Web execution |
| ⚖️ **THEMIS** | 8153 | Legal & Ethics | Compliance |
| 🔒 **NIS** | 8154 | Intel & Security | Security analysis |
| 🚀 **HERA** | 8155 | DevOps | Deploy and infra |
| 🔧 **Eureka** | 8156 | Auto-Remediation | Automatic fixes |
| 🎭 **Fryda** | 8157 | Personas | Behavior adaptation |

### External Services

| Service | Use |
|---------|-----|
| 📋 **ClickUp** | Task and project management |
| 🐙 **GitHub** | Repository and code tracking |
| 🤖 **Claude API** | Reasoning and natural language |

---

## 📖 Documentation

- **[Quick Start](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Architecture](docs/ARCHITECTURE.md)** - Complete documentation
- **[Base Agent](docs/BASE_AGENT.md)** - Base agent documentation
- **[Examples](examples/)** - Usage examples

---

## 🎓 Evolution of Assistants

```
Generation 1: Simple Chatbots (2010-2018)
├─ Answer questions
└─ No context

Generation 2: AI Assistants (2019-2023)
├─ Natural conversation
├─ Generate text and code
└─ No real execution

Generation 3: AI Agents (2024)
├─ Use tools
├─ Execute simple tasks
└─ No real consciousness

⭐ Generation 4: MAXIMUS Personal Assistant (2025)
├─ 🧠 Consciousness (Max AI Core)
├─ ⚡ Autonomous Execution (MABA)
├─ 🛡️ Constitutional Validation
├─ 💾 Deep Memory
├─ 🔌 Complete Integration
└─ 📊 High Performance
```

---

## 🚀 Usage Examples

### Example 1: Daily Planning

```
You: Good morning! What should I do today?

🧠 MAXIMUS: Good morning! Based on your priorities, I suggest:

1. 🔴 URGENT: Implement Tree of Thoughts in Max-Code
   (You added the import yesterday, but the module is missing)

2. 🟡 IMPORTANT: Review 3 Maximus-BOT issues on GitHub
   (They've been open for 5 days)

3. 🟢 DOCUMENTATION: Update V-rtice README
   (Last commit was 10 days ago)

Want me to create tasks in ClickUp for these actions?
```

### Example 2: Roadmap Execution

```
You: execute roadmaps/launch_typecraft.md

📋 Loading roadmap: roadmaps/launch_typecraft.md
🧠 Analyzing roadmap with Claude...

✅ Roadmap analyzed: 12 steps identified

🤖 Automatable steps: 8
👤 Manual steps: 4

🚀 Starting automatic execution...

🧠 Executing consciously: Create landing page
✅ Validation approved. Executing...
🤖 Executing: Create landing page
   📍 Step 1/5: navigate
   📍 Step 2/5: fill_form
   📍 Step 3/5: click
   📍 Step 4/5: screenshot
   📍 Step 5/5: extract
   ✅ Completed!

...

✅ Execution complete: 12 steps (8 automated, 4 marked for manual action)
```

---

## 🛠️ Development

### Setup Development Environment

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

# Run tests
pytest

# Format code
black maximus_pa/

# Type checking
mypy maximus_pa/
```

### Project Structure

```
maximus-personal-assistant/
├── maximus_pa/              # Main package
│   ├── core/               # Core modules
│   │   ├── secretary_agent.py
│   │   ├── secretary_executor.py
│   │   └── maximus_pa.py
│   ├── integrations/       # External integrations
│   ├── utils/              # Utilities
│   └── cli.py              # CLI interface
├── docs/                   # Documentation
├── tests/                  # Tests
├── examples/               # Usage examples
├── data/                   # Data directory
├── setup.py               # Setup script
├── requirements.txt       # Dependencies
└── README.md              # This file
```

---

## 🤝 Contributing

Want to improve MAXIMUS PA? Areas that need help:

1. **Integrations**: Notion, Trello, Linear, Jira
2. **Execution**: More automation types
3. **UI**: Modern web interface
4. **ML**: User need prediction
5. **Tests**: More coverage, integration tests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** for Claude API
- **MAXIMUS AI Team** for the ecosystem
- **Open Source Community** for inspiration

---

## 📞 Support

**Common Issues:**

1. **"ANTHROPIC_API_KEY not configured"**
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

2. **"Core not available"**
   - Not an error! Assistant works without Core
   - Use fallback mode
   - Start Core when needed

3. **"Low performance"**
   ```bash
   # Check metrics
   mpa --performance
   ```

**Need help?** Open an issue on [GitHub](https://github.com/JuanCS-Dev/maximus-personal-assistant/issues)

---

## 🎯 Roadmap

### Q1 2026
- [ ] Web interface (React + FastAPI)
- [ ] Mobile app (React Native)
- [ ] Voice commands (Speech-to-Text)
- [ ] Multi-user support

### Q2 2026
- [ ] Machine Learning for prediction
- [ ] Auto-complete repetitive tasks
- [ ] Calendar integration
- [ ] Email automation

### Q3 2026
- [ ] Collaborative mode
- [ ] Plugin system
- [ ] Automation marketplace
- [ ] Enterprise features

---

**Created by:** MAXIMUS AI
**Version:** 2.0.0
**Status:** Beta Production ✅
**Date:** November 10, 2025

*Soli Deo Gloria* 🙏

---

**NOT just another AI assistant. The FUTURE of Personal Assistants.** 🚀
