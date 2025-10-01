# FocusSuite - Complete Developer Documentation

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)](https://github.com/jassu2244/FocusSuite/releases)

**An intelligent desktop productivity tool to eliminate distractions and streamline video editing.**

</div>

## Table of Contents
- [Quick Start Guide](#quick-start-guide)
- [What is FocusSuite?](#what-is-focussuite)
- [Features Overview](#features-overview)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Project Architecture](#project-architecture)
- [Code Structure](#code-structure)
- [API Integration](#api-integration)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Troubleshooting](#troubleshooting)

---

## Quick Start Guide

### For Users
1. **Install Python 3.9+** from [python.org](https://python.org)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Install Tesseract OCR** (see [installation guide](#tesseract-setup))
4. **Configure API keys** in Settings tab
5. **Run**: `python FocusSuite/main.py`

### For Developers
1. **Clone the repository**: `git clone https://github.com/jassu2244/FocusSuite.git`
2. **Set up virtual environment**: `python -m venv venv && venv\Scripts\activate`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Read the [Project Architecture](#project-architecture)** section
5. **Check [Contributing Guidelines](#contributing-guidelines)**

---

## What is FocusSuite?

FocusSuite is a Python-based desktop application that helps users maintain focus through two main features:

### 🎯 Focus Monitor (Real-time Distraction Blocker)
- **Monitors your screen** in real-time using Optical Character Recognition (OCR)
- **Identifies distracting text** using AI (OpenAI GPT-4 or local LLM)
- **Blurs distractions** with transparent overlays
- **Smart detection** only processes screen changes (using SSIM image comparison)

### 🎬 Focus Video (AI-Powered Video Editor)
- **Analyzes video frames** to identify objects/elements you want to blur
- **Uses natural language prompts** ("blur all faces", "hide license plates")
- **Creates smooth blur effects** without flickering
- **Preserves original audio** perfectly

---

## Features Overview

| Feature | Technology | Description |
|---------|------------|-------------|
| **Real-time Screen Monitoring** | Tesseract OCR + SSIM | Efficient screen change detection and text extraction |
| **AI-Powered Analysis** | OpenAI GPT-4o + Local LLM | Intelligent identification of distracting content |
| **Smart Overlay System** | Tkinter + Windows API | Non-intrusive blur overlays that don't interfere with work |
| **Video Processing** | OpenCV + MoviePy | Frame-by-frame analysis with smooth timeline reconstruction |
| **Cross-API Support** | Multiple APIs | Supports OpenAI, Vision API, and local Worker endpoints |
| **Modern UI** | Themed Tkinter | Clean, professional interface with multiple themes |
| **System Integration** | System Tray + Hotkeys | Seamless desktop integration |

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11 (primary), Linux/macOS (experimental)
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for application + dependencies

### Required External Software
- **Tesseract OCR**: For text recognition
- **FFmpeg**: For video processing (automatically installed with moviepy)

### Optional Requirements
- **OpenAI API Key**: For GPT-4 analysis (recommended)
- **Local LLM**: Alternative to OpenAI for privacy-focused users

---

## Installation Guide

### Step 1: Install Python
```bash
# Windows: Download from python.org
# Or using chocolatey:
choco install python

# Verify installation
python --version  # Should show 3.9+
```

### Step 2: Clone Repository
```bash
git clone https://github.com/jassu2244/FocusSuite.git
cd FocusSuite
```

### Step 3: Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv focussuite_env

# Activate it
# Windows:
focussuite_env\Scripts\activate
# Linux/macOS:
source focussuite_env/bin/activate
```

### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API integration
- `opencv-python` - Video processing
- `moviepy` - Video editing and audio handling
- `pytesseract` - OCR functionality
- `Pillow` - Image processing
- `scikit-image` - Image analysis and SSIM
- `requests` - API communication
- `pystray` - System tray integration
- `keyboard` - Global hotkey support
- And more...

### Step 5: Install Tesseract OCR {#tesseract-setup}

#### Windows
```bash
# Option 1: Download installer from GitHub
# https://github.com/UB-Mannheim/tesseract/wiki

# Option 2: Using chocolatey
choco install tesseract

# Option 3: Using conda
conda install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

**Important**: Update the Tesseract path in `utils/constants.py` if installed in a non-standard location.

### Step 6: Verify Installation
```bash
# Test Tesseract
tesseract --version

# Test Python dependencies
python -c "import cv2, PIL, pytesseract; print('All dependencies installed successfully!')"
```

---

## Configuration

### Environment Variables (.env file)
Create a `.env` file in the project root:
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Worker API Configuration (for local LLM)
WORKER_API_URL=https://your-worker-endpoint.workers.dev

# Optional: Logging level
LOG_LEVEL=INFO
```

### Settings File (settings.json)
The application creates a `settings.json` file automatically:
```json
{
    "api_key": "your-openai-key",
    "worker_url": "your-worker-endpoint",
    "last_focus_topic": "work tasks",
    "theme": "scholarly_light",
    "whitelist": ["notepad.exe", "code.exe"],
    "provider": "OpenAI"
}
```

### API Keys Setup

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to the Settings tab in the application
4. **Cost**: ~$0.01-0.05 per hour of monitoring

#### Local LLM (Worker API)
- Deploy your own LLM using Cloudflare Workers
- See `api/worker_api.py` for expected endpoint format
- **Cost**: Free (your own infrastructure)

---

## Usage Guide

### Starting the Application
```bash
# Navigate to project directory
cd FocusSuite

# Run the application
python FocusSuite/main.py
```

### Using Focus Monitor
1. **Open the "Distraction Blocker" tab**
2. **Enter your focus topic** (e.g., "Python programming", "writing report")
3. **Select API provider** (OpenAI or Local Worker)
4. **Click "Start Monitoring"**
5. **Work normally** - distractions will be automatically blurred

#### Example Focus Topics
- "Writing my thesis"
- "Learning Python programming"
- "Working on project presentation"
- "Reading technical documentation"

### Using Focus Video
1. **Open the "Focus Video" tab**
2. **Click "Select Video"** and choose your video file
3. **Enter a blur prompt** (e.g., "blur all faces", "hide license plates")
4. **Click "Start Processing"**
5. **Wait for completion** - the processed video will be saved automatically

#### Example Blur Prompts
- "blur all human faces"
- "hide license plates"
- "obscure text on screens"
- "blur background people"

### Settings Configuration
1. **Open the "Settings" tab**
2. **Configure API keys** for your chosen provider
3. **Set application whitelist** (apps that won't trigger monitoring)
4. **Choose your preferred theme**
5. **Test API connections**

---

## Project Architecture

FocusSuite follows a **modular, separation-of-concerns architecture** that makes it easy to understand, maintain, and extend.

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Core Logic     │    │  API Layer      │
│                 │    │                 │    │                 │
│ • Main Window   │◄──►│ • App Manager   │◄──►│ • OpenAI API    │
│ • Tabs          │    │ • Focus Monitor │    │ • Vision API    │
│ • Overlay       │    │ • Video Proc.   │    │ • Worker API    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Utils Layer    │    │  Data Models    │    │  Configuration  │
│                 │    │                 │    │                 │
│ • Logging       │    │ • Distraction   │    │ • Settings      │
│ • Constants     │    │   Area          │    │ • API Keys      │
│ • Windows Utils │    │ • Other Models  │    │ • Preferences   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Design Principles

#### 1. Separation of Concerns (SoC)
- **UI Layer**: Only handles user interaction and display
- **Core Logic**: Contains business logic and feature management
- **API Layer**: Manages external service communication
- **Utils**: Shared utilities and configuration

#### 2. Callback-Driven Architecture
The core application is **headless** and communicates with the UI through callbacks:
```python
# UI callbacks passed to core managers
ui_callbacks = {
    'on_start': self._on_monitoring_started,
    'on_stop': self._on_monitoring_stopped,
    'show_message': self.show_ui_message,
}
```

#### 3. Manager Pattern
Each major feature has a dedicated manager:
- `FocusMonitorManager`: Handles screen monitoring
- `VideoFeatureManager`: Orchestrates video processing  
- `ConfigManager`: Manages settings and preferences

---

## Code Structure

### Directory Layout
```
FocusSuite/
├── main.py                 # 🚀 Application entry point
├── app.py                  # 🎛️ Central orchestrator
├── config.py              # ⚙️ Settings management
├── requirements.txt        # 📦 Python dependencies
├── about.txt              # 📝 Technical documentation
├── ai.txt                 # 🤖 AI integration notes
│
├── api/                   # 🌐 External API integrations
│   ├── openai_manager.py  #   └── OpenAI GPT-4 integration
│   ├── vision_api_manager.py # └── Vision API for video analysis
│   └── worker_api.py      #   └── Local LLM worker endpoint
│
├── core/                  # 🧠 Core business logic
│   ├── focus_monitor_manager.py # └── Screen monitoring logic
│   ├── video_feature_manager.py # └── Video processing orchestration
│   ├── video_processor.py       # └── Video analysis and editing
│   └── models.py               # └── Data structures
│
├── ui/                    # 🎨 User interface components
│   ├── main_window.py     #   └── Main application window
│   ├── overlay.py         #   └── Transparent overlay system
│   ├── themed_style.py    #   └── UI themes and styling
│   │
│   ├── tabs/              #   📁 Main application tabs
│   │   ├── distraction_tab.py    # └── Focus monitor controls
│   │   ├── video_tab.py          # └── Video processing interface
│   │   └── settings_tab.py       # └── Configuration panel
│   │
│   └── widgets/           #   📁 Custom UI components
│       └── custom_widgets.py     # └── Specialized widgets
│
└── utils/                 # 🔧 Utilities and helpers
    ├── constants.py       #   └── Application constants
    ├── logger.py          #   └── Logging configuration
    └── windows_utils.py   #   └── Windows-specific functions
```

### Key Files Explained

#### 🚀 Entry Points
- **`main.py`**: Application startup, DPI awareness, root window creation
- **`app.py`**: Central coordinator that connects all components

#### 🧠 Core Logic
- **`focus_monitor_manager.py`**: 
  - Manages the monitoring loop
  - Handles SSIM-based change detection
  - Coordinates with overlay system
  
- **`video_processor.py`**:
  - Extracts unique frames using SSIM
  - Manages parallel API calls for frame analysis
  - Reconstructs video with smooth blur timeline

#### 🌐 API Integration
- **`openai_manager.py`**: OpenAI GPT-4 integration with retry logic
- **`vision_api_manager.py`**: Worker-based vision API for video frames
- **`worker_api.py`**: Local LLM endpoint integration

#### 🎨 User Interface
- **`main_window.py`**: Main window with tabbed interface
- **`overlay.py`**: Transparent, click-through overlay for blur effects
- **Tab files**: Individual feature interfaces with themed styling

---

## API Integration

### OpenAI Integration

FocusSuite uses OpenAI's GPT-4 for intelligent text analysis:

```python
# Example API call structure
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": screen_text}
    ],
    response_format={"type": "json_object"},
    temperature=0.2
)
```

**Features**:
- JSON-structured responses
- Retry logic for transient failures
- Connection testing and validation
- Rate limiting awareness

### Vision API Integration

For video processing, FocusSuite uses a custom vision API:

```python
# Video frame analysis
files = {
    'image': (filename, image_file, 'image/jpeg'),
    'text': (None, analysis_prompt),
}
response = requests.post(api_url, files=files, timeout=30)
```

**Features**:
- Parallel frame processing
- Image format optimization
- Error handling and retry logic
- Progress tracking

### Local LLM Support

For privacy-conscious users, FocusSuite supports local LLM endpoints:

```python
# Worker API payload structure
payload = {
    "system": system_prompt,
    "user": user_input
}
response = requests.post(worker_url, json=payload)
```

---

## Development Setup

### Development Environment

#### Recommended IDE Setup
```bash
# Visual Studio Code with extensions:
# - Python
# - Python Docstring Generator
# - GitLens
# - Error Lens

# PyCharm (alternative)
# - Built-in Python support
# - Integrated debugging
# - Code analysis
```

#### Code Quality Tools
```bash
# Install development tools
pip install black flake8 mypy pytest

# Format code
black FocusSuite/

# Lint code
flake8 FocusSuite/

# Type checking
mypy FocusSuite/

# Run tests
pytest tests/
```

### Adding New Features

#### 1. Creating a New API Integration
```python
# Create new file: api/new_service_manager.py
class NewServiceManager:
    def __init__(self, logger):
        self.logger = logger
        
    def configure(self, api_key: str) -> bool:
        # Implementation here
        pass
        
    def is_available(self) -> bool:
        # Implementation here
        pass
        
    def analyze_text(self, text: str) -> dict:
        # Implementation here
        pass
```

#### 2. Adding UI Components
```python
# Add to ui/tabs/ or ui/widgets/
class NewFeatureTab:
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks
        self._setup_ui()
        
    def _setup_ui(self):
        # Create widgets here
        pass
```

#### 3. Extending Core Features
```python
# Create new manager in core/
class NewFeatureManager:
    def __init__(self, root, config, api_manager, ui_callbacks, logger):
        # Initialize manager
        pass
        
    def start_feature(self):
        # Feature logic here
        pass
```

### Testing

#### Unit Tests
```python
# tests/test_focus_monitor.py
import unittest
from core.focus_monitor_manager import FocusMonitorManager

class TestFocusMonitor(unittest.TestCase):
    def test_monitoring_start(self):
        # Test implementation
        pass
```

#### Integration Tests
```python
# tests/test_integration.py
def test_full_monitoring_cycle():
    # Test complete monitoring workflow
    pass
```

#### Manual Testing Checklist
- [ ] API key validation
- [ ] Screen monitoring accuracy
- [ ] Video processing quality
- [ ] UI responsiveness
- [ ] Error handling
- [ ] Resource cleanup

---

## Contributing Guidelines

### Getting Started
1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Read the code style guide** below
4. **Make your changes** following the architecture patterns
5. **Add tests** for new functionality
6. **Update documentation** as needed
7. **Submit a pull request**

### Code Style Guide

#### Python Code Standards
```python
# Follow PEP 8
# Use type hints
def process_text(text: str, config: dict) -> List[str]:
    pass

# Use docstrings
def complex_function(param: str) -> bool:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When parameter is invalid
    """
    pass
```

#### File Organization
```python
# Standard import order:
# 1. Standard library
import os
import threading
from typing import List, Dict

# 2. Third-party packages
import cv2
import numpy as np
from PIL import Image

# 3. Local imports
from core.models import DistractionArea
from utils.logger import setup_logging
```

#### Commit Messages
```bash
# Use conventional commit format:
feat: add new video blur algorithm
fix: resolve memory leak in monitor loop
docs: update installation instructions
refactor: simplify API manager interface
test: add unit tests for video processor
```

### Areas Needing Contribution

#### 🚀 High Priority
- **Cross-platform support** (Linux/macOS)
- **Performance optimizations** for large videos
- **Additional AI model support** (Anthropic Claude, local models)
- **Automated testing suite**
- **Documentation translations**

#### 🔧 Medium Priority
- **Plugin system** for custom blur algorithms
- **Configuration GUI improvements**
- **Video format support expansion**
- **Accessibility features**
- **Dark mode themes**

#### 💡 Enhancement Ideas
- **Mobile companion app**
- **Browser extension integration**
- **Productivity analytics**
- **Custom hotkey configuration**
- **Cloud sync for settings**

### Pull Request Process

1. **Ensure all tests pass**
2. **Update README.md** with changes
3. **Add entry to CHANGELOG.md**
4. **Request review** from maintainers
5. **Address feedback** promptly
6. **Squash commits** before merge

---

## Troubleshooting

### Common Issues

#### Installation Problems

**Issue**: `pytesseract.TesseractNotFoundError`
```bash
# Solution: Install Tesseract OCR
# Windows: choco install tesseract
# Linux: sudo apt install tesseract-ocr
# macOS: brew install tesseract

# Update path in utils/constants.py if needed
TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Issue**: `ImportError: No module named 'cv2'`
```bash
# Solution: Install OpenCV
pip install opencv-python

# For development version:
pip install opencv-contrib-python
```

#### Runtime Issues

**Issue**: High CPU usage during monitoring
```python
# Check SSIM threshold in focus_monitor_manager.py
# Increase threshold for less sensitivity:
if score > 0.99:  # Was 0.98
    continue
```

**Issue**: API rate limiting errors
```python
# Increase delay between API calls
time.sleep(3)  # Instead of 2 seconds

# Or implement exponential backoff
import time
for attempt in range(max_retries):
    time.sleep(2 ** attempt)
```

**Issue**: Video processing fails
```bash
# Check FFmpeg installation
ffmpeg -version

# Install if missing:
# Windows: choco install ffmpeg
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

#### UI Issues

**Issue**: Overlay not appearing
```python
# Check Windows DPI settings
# Ensure high DPI awareness is enabled in main.py:
ctypes.windll.shcore.SetProcessDpiAwareness(2)
```

**Issue**: Application crashes on startup
```bash
# Run with debug logging
python FocusSuite/main.py --debug

# Check logs in app.log
tail -f app.log
```

### Performance Optimization

#### Memory Usage
```python
# Monitor memory in video processing
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
```

#### CPU Usage
```python
# Optimize monitoring frequency
time.sleep(3)  # Increase from 2 seconds

# Use smaller screenshot sizes
screenshot.resize((128, 72))  # Instead of (256, 144)
```

### Getting Help

#### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Wiki**: Community-maintained documentation

#### Developer Resources
- **Code Documentation**: Inline comments and docstrings
- **Architecture Docs**: `about.txt` and `ai.txt`
- **API Documentation**: Comments in `api/` modules

#### Contact Information
- **Maintainer**: [Your GitHub Profile]
- **Email**: [Your Contact Email]
- **Discord**: [Community Server Link]

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI**: For providing the GPT-4 API
- **Tesseract OCR**: For text recognition capabilities
- **OpenCV Community**: For computer vision tools
- **Python Community**: For the excellent ecosystem
- **Contributors**: Everyone who helps improve FocusSuite

---

<div align="center">

**[⬆ Back to Top](#focussuite---complete-developer-documentation)**

Made with ❤️ by the FocusSuite community

</div>