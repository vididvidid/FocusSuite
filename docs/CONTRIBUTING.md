# Contributing to FocusSuite

Thank you for your interest in contributing to FocusSuite! This document provides guidelines and information for developers who want to contribute to the project.

## Table of Contents
- [Quick Start for Contributors](#quick-start-for-contributors)
- [Development Environment Setup](#development-environment-setup)
- [Code Architecture](#code-architecture)
- [Contribution Workflow](#contribution-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Areas Needing Contribution](#areas-needing-contribution)
- [Submitting Changes](#submitting-changes)

## Quick Start for Contributors

### Prerequisites
- Python 3.9+
- Git
- Basic understanding of Python and Tkinter
- Familiarity with API integrations (OpenAI, REST APIs)

### Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/FocusSuite.git
cd FocusSuite
git remote add upstream https://github.com/jassu2244/FocusSuite.git
```

### Development Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black flake8 mypy pytest

# Install Tesseract OCR (see BEGINNER_GUIDE.md)
```

### Test Your Setup
```bash
# Run the application
python FocusSuite/main.py

# Run tests (when available)
pytest tests/

# Format code
black FocusSuite/

# Lint code
flake8 FocusSuite/
```

## Development Environment Setup

### Recommended IDE Configuration

#### Visual Studio Code
Install these extensions:
- Python (Microsoft)
- Python Docstring Generator
- GitLens
- Error Lens
- Pylance

**VS Code Settings (.vscode/settings.json):**
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "files.autoSave": "onFocusChange"
}
```

#### PyCharm
- Configure interpreter to use virtual environment
- Enable PEP 8 code style checking
- Set up automatic formatting with Black

### Development Tools

#### Code Formatting (Black)
```bash
# Format all Python files
black FocusSuite/

# Format specific file
black FocusSuite/core/focus_monitor_manager.py

# Check without formatting
black --check FocusSuite/
```

#### Linting (Flake8)
```bash
# Lint all files
flake8 FocusSuite/

# Custom configuration in setup.cfg:
[flake8]
max-line-length = 88
exclude = venv, __pycache__
ignore = E203, W503
```

#### Type Checking (MyPy)
```bash
# Type check all files
mypy FocusSuite/

# Configuration in mypy.ini:
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

## Code Architecture

### Project Structure Overview
```
FocusSuite/
├── 🚀 main.py              # Entry point
├── 🎛️ app.py               # Central orchestrator
├── ⚙️ config.py            # Configuration manager
│
├── 🌐 api/                 # External API integrations
│   ├── openai_manager.py   # OpenAI GPT-4 API
│   ├── vision_api_manager.py # Vision API for videos
│   └── worker_api.py       # Local LLM worker
│
├── 🧠 core/                # Business logic
│   ├── focus_monitor_manager.py # Screen monitoring
│   ├── video_feature_manager.py # Video orchestration
│   ├── video_processor.py      # Video processing
│   └── models.py               # Data models
│
├── 🎨 ui/                  # User interface
│   ├── main_window.py      # Main window
│   ├── overlay.py          # Blur overlays
│   ├── themed_style.py     # UI themes
│   ├── tabs/               # Feature tabs
│   └── widgets/            # Custom widgets
│
└── 🔧 utils/               # Utilities
    ├── constants.py        # App constants
    ├── logger.py           # Logging setup
    └── windows_utils.py    # OS-specific utils
```

### Key Design Patterns

#### 1. Manager Pattern
Each major feature has a dedicated manager class:
```python
class FeatureManager:
    def __init__(self, dependencies):
        # Initialize with required dependencies
        pass
    
    def start_feature(self):
        # Start the feature
        pass
    
    def stop_feature(self):
        # Clean shutdown
        pass
```

#### 2. Callback-Driven UI
Core logic is headless and communicates via callbacks:
```python
ui_callbacks = {
    'on_start': self._handle_start,
    'on_stop': self._handle_stop,
    'show_message': self._show_message,
    'update_progress': self._update_progress
}
```

#### 3. Configuration Management
Centralized settings with automatic persistence:
```python
# Get setting with default
value = self.config.get('setting_name', default_value)

# Set setting
self.config.set('setting_name', new_value)

# Save to disk
self.config.save()
```

## Contribution Workflow

### 1. Choose an Issue
- Check [GitHub Issues](https://github.com/jassu2244/FocusSuite/issues)
- Look for labels: `good first issue`, `help wanted`, `enhancement`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch
```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 3. Make Changes
Follow the coding guidelines and architecture patterns described below.

### 4. Test Your Changes
```bash
# Test manually
python FocusSuite/main.py

# Run automated tests
pytest tests/

# Check code quality
black --check FocusSuite/
flake8 FocusSuite/
mypy FocusSuite/
```

### 5. Commit and Push
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new blur algorithm for video processing"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Go to GitHub and create a Pull Request
- Fill out the PR template
- Link related issues
- Request review from maintainers

## Code Style Guidelines

### Python Code Style

#### Follow PEP 8 with Black formatting
```python
# Good: Clear function with type hints
def process_screenshot(
    screenshot: Image.Image, 
    focus_topic: str
) -> List[DistractionArea]:
    """
    Process screenshot to find distracting areas.
    
    Args:
        screenshot: PIL Image of the screen
        focus_topic: User's current focus topic
        
    Returns:
        List of detected distraction areas
    """
    # Implementation here
    pass
```

#### Use Type Hints
```python
from typing import List, Dict, Optional, Union

# Function signatures
def analyze_frame(frame_path: str, prompt: str) -> Optional[str]:
    pass

# Class attributes
class VideoProcessor:
    def __init__(self, logger: logging.Logger):
        self.frames: List[Dict[str, Any]] = []
        self.output_path: Optional[str] = None
```

#### Docstring Format
```python
def complex_function(param1: str, param2: int = 10) -> bool:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the algorithm
    or providing usage examples.
    
    Args:
        param1: Description of the first parameter
        param2: Description with default value
        
    Returns:
        Description of return value and its type
        
    Raises:
        ValueError: When param1 is empty
        APIError: When external service fails
        
    Example:
        >>> result = complex_function("test", 20)
        >>> print(result)
        True
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    # Implementation here
    return True
```

#### Error Handling
```python
# Good: Specific exception handling
try:
    response = api_call()
except requests.RequestException as e:
    self.logger.error(f"API request failed: {e}")
    return None
except json.JSONDecodeError as e:
    self.logger.error(f"Invalid JSON response: {e}")
    return None

# Good: Resource cleanup
try:
    with open(file_path, 'r') as f:
        data = f.read()
except FileNotFoundError:
    self.logger.warning(f"File not found: {file_path}")
    return None
```

#### Logging
```python
import logging

class MyClass:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_data(self):
        self.logger.info("Starting data processing")
        try:
            # Processing logic
            self.logger.debug(f"Processed {count} items")
        except Exception as e:
            self.logger.error(f"Processing failed: {e}", exc_info=True)
```

### File Organization

#### Import Order
```python
# 1. Standard library imports
import os
import sys
import threading
from typing import List, Dict, Optional

# 2. Third-party imports
import cv2
import numpy as np
import requests
from PIL import Image

# 3. Local application imports
from core.models import DistractionArea
from utils.logger import setup_logging
from api.openai_manager import OpenAIAPIManager
```

#### Class Organization
```python
class ExampleClass:
    """Class docstring."""
    
    # Class variables
    DEFAULT_TIMEOUT = 30
    
    def __init__(self, param: str):
        """Initialize the class."""
        # Instance variables
        self.param = param
        self._private_var = None
    
    # Public methods
    def public_method(self) -> str:
        """Public method docstring."""
        return self._private_method()
    
    # Private methods
    def _private_method(self) -> str:
        """Private method docstring."""
        return "result"
    
    # Static methods
    @staticmethod
    def utility_function(data: str) -> str:
        """Static utility function."""
        return data.upper()
```

### UI Code Guidelines

#### Tkinter Widget Creation
```python
def _setup_ui(self):
    """Set up the user interface."""
    # Create main frame
    main_frame = ttk.Frame(self.parent)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Create labeled input
    ttk.Label(main_frame, text="Focus Topic:").pack(anchor='w')
    self.focus_entry = ttk.Entry(main_frame, width=50)
    self.focus_entry.pack(fill='x', pady=(0, 10))
    
    # Create button with command
    self.start_button = ttk.Button(
        main_frame, 
        text="Start Monitoring",
        command=self._on_start_clicked
    )
    self.start_button.pack()

def _on_start_clicked(self):
    """Handle start button click."""
    focus_topic = self.focus_entry.get().strip()
    if self.callbacks and 'start_monitoring' in self.callbacks:
        self.callbacks['start_monitoring'](focus_topic)
```

#### Theme Application
```python
def apply_theme(self, theme_colors: Dict[str, str]):
    """Apply theme colors to widgets."""
    # Configure custom styles
    style = ttk.Style()
    style.configure(
        'Custom.TButton',
        background=theme_colors.get('button_bg', '#ffffff'),
        foreground=theme_colors.get('button_fg', '#000000')
    )
    
    # Apply to widgets
    self.start_button.configure(style='Custom.TButton')
```

## Testing Guidelines

### Unit Testing Structure
```python
# tests/test_focus_monitor.py
import unittest
from unittest.mock import Mock, patch
from core.focus_monitor_manager import FocusMonitorManager

class TestFocusMonitorManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mock_root = Mock()
        self.mock_config = Mock()
        self.mock_api = Mock()
        self.mock_overlay = Mock()
        self.mock_callbacks = {}
        self.mock_logger = Mock()
        
        self.manager = FocusMonitorManager(
            self.mock_root,
            self.mock_config,
            self.mock_api,
            self.mock_overlay,
            self.mock_callbacks,
            self.mock_logger
        )
    
    def test_start_monitoring_with_valid_topic(self):
        """Test starting monitoring with valid focus topic."""
        # Arrange
        self.mock_api.is_available.return_value = True
        focus_topic = "work tasks"
        
        # Act
        self.manager.start_monitoring(focus_topic)
        
        # Assert
        self.assertTrue(self.manager.monitoring)
        self.assertEqual(self.manager.focus_topic, focus_topic)
        self.mock_config.set.assert_called_with('last_focus_topic', focus_topic)
    
    def test_start_monitoring_without_topic(self):
        """Test starting monitoring without focus topic."""
        # Arrange
        self.mock_callbacks['show_message'] = Mock()
        
        # Act
        self.manager.start_monitoring("")
        
        # Assert
        self.assertFalse(self.manager.monitoring)
        self.mock_callbacks['show_message'].assert_called_once()
```

### Integration Testing
```python
# tests/test_integration.py
def test_complete_monitoring_workflow():
    """Test the complete monitoring workflow."""
    # Test setup
    config = ConfigManager(test_settings_file)
    api_manager = OpenAIAPIManager(mock_logger)
    
    # Test API configuration
    assert api_manager.configure(test_api_key)
    assert api_manager.is_available()
    
    # Test monitoring cycle
    monitor = FocusMonitorManager(...)
    monitor.start_monitoring("test topic")
    
    # Verify state
    assert monitor.monitoring
    
    # Cleanup
    monitor.stop_monitoring()
    assert not monitor.monitoring
```

### Manual Testing Checklist

Before submitting a PR, test these scenarios:

#### Core Functionality
- [ ] Application starts without errors
- [ ] API key configuration works
- [ ] Monitoring starts and stops correctly
- [ ] Screen changes are detected
- [ ] Overlays appear and disappear
- [ ] Video processing completes successfully

#### Error Handling
- [ ] Invalid API key shows appropriate error
- [ ] Network errors are handled gracefully
- [ ] File not found errors don't crash the app
- [ ] Memory cleanup works correctly

#### UI/UX
- [ ] All buttons respond correctly
- [ ] Settings are saved and loaded
- [ ] Themes apply correctly
- [ ] Console logging works
- [ ] Progress updates appear

## Areas Needing Contribution

### 🔥 High Priority Issues

#### Cross-Platform Support
**Difficulty: Medium-Hard**
- Adapt Windows-specific code for Linux/macOS
- Test Tesseract paths on different systems
- Handle different window management APIs

```python
# Example: utils/cross_platform_utils.py
import platform

def get_tesseract_path():
    system = platform.system()
    if system == "Windows":
        return r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    elif system == "Darwin":  # macOS
        return "/usr/local/bin/tesseract"
    else:  # Linux
        return "/usr/bin/tesseract"
```

#### Performance Optimization
**Difficulty: Medium**
- Optimize SSIM calculation
- Reduce memory usage in video processing
- Implement frame caching

```python
# Example optimization opportunity
def optimized_ssim_check(self, current_frame, last_frame):
    # Resize for faster comparison
    small_current = cv2.resize(current_frame, (64, 36))
    small_last = cv2.resize(last_frame, (64, 36))
    
    # Use faster comparison method
    return cv2.matchTemplate(small_current, small_last, cv2.TM_CCOEFF_NORMED)
```

#### API Integration Expansion
**Difficulty: Easy-Medium**
- Add support for Anthropic Claude
- Implement local Ollama integration
- Add Google Vision API

```python
# Template for new API manager
class ClaudeAPIManager:
    def __init__(self, logger):
        self.logger = logger
        self.client = None
    
    def configure(self, api_key: str) -> bool:
        # Implementation here
        pass
    
    def is_available(self) -> bool:
        # Implementation here
        pass
    
    def analyze_text(self, text: str, focus_topic: str) -> Dict:
        # Implementation here
        pass
```

### 🛠️ Medium Priority Enhancements

#### Plugin System
**Difficulty: Hard**
- Design plugin architecture
- Create plugin loading system
- Develop sample plugins

#### Better Video Formats
**Difficulty: Easy-Medium**
- Add support for more video formats
- Implement video compression options
- Add batch processing

#### UI Improvements
**Difficulty: Easy**
- Add more themes
- Improve accessibility
- Better progress indicators

### 💡 Feature Ideas for New Contributors

#### Easy Tasks (Good First Issues)
- Add new themes to `ui/themed_style.py`
- Improve error messages
- Add configuration validation
- Create example configuration files
- Write additional documentation

#### Medium Tasks
- Implement keyboard shortcuts
- Add system notification support
- Create video preview functionality
- Add configuration export/import

#### Advanced Tasks
- Implement machine learning model training
- Add real-time performance metrics
- Create web-based configuration interface
- Develop mobile companion app

## Submitting Changes

### Pull Request Requirements

#### Before Submitting
1. **Code Quality Checks Pass**
   ```bash
   black --check FocusSuite/
   flake8 FocusSuite/
   mypy FocusSuite/
   ```

2. **Tests Pass**
   ```bash
   pytest tests/
   ```

3. **Manual Testing Completed**
   - Core functionality works
   - No new bugs introduced
   - Performance is acceptable

4. **Documentation Updated**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update this CONTRIBUTING.md if needed

#### PR Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Cross-platform testing (if applicable)

## Screenshots (if applicable)
Add screenshots of UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added for new functionality
```

### Review Process

1. **Automated Checks**: GitHub Actions will run automated tests
2. **Code Review**: Maintainers will review your code
3. **Testing**: Changes will be tested on different configurations
4. **Feedback**: You may be asked to make changes
5. **Merge**: Once approved, your PR will be merged

### After Your PR is Merged

1. **Update your fork**:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

2. **Delete the feature branch**:
   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

3. **Celebrate!** 🎉 You've contributed to FocusSuite!

## Getting Help

### Communication Channels
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: In pull request comments

### Asking for Help
When asking for help, please provide:
1. **Clear description** of what you're trying to do
2. **Steps you've already tried**
3. **Error messages** (full stack traces)
4. **Your environment** (OS, Python version, etc.)
5. **Relevant code snippets**

### Mentorship
New contributors can request mentorship by:
1. Commenting on issues marked `good first issue`
2. Asking for guidance in GitHub Discussions
3. Requesting code review feedback

## Recognition

Contributors will be recognized in:
- Project README.md
- GitHub contributors list
- Release notes for significant contributions

Thank you for contributing to FocusSuite! Your efforts help make productivity tools more accessible and effective for everyone. 🚀