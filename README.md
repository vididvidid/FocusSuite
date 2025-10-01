# FocusSuite

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)](https://github.com/jassu2244/FocusSuite/releases)

**An intelligent desktop productivity tool to eliminate distractions and streamline video editing.**

</div>

FocusSuite is a Python-based desktop application designed to help users maintain focus. It has two main features:

1. **🎯 Focus Monitor**: Watches your screen in real-time, using AI to identify and blur distracting text automatically
2. **🎬 Focus Video**: Processes video files, automatically blurring elements based on simple descriptive prompts

<div align="center">

### 📚 Documentation Quick Links

**[🚀 Beginner's Guide](docs/BEGINNER_GUIDE.md)** | **[📖 Complete Documentation](docs/DOCUMENTATION.md)** | **[🛠️ Contributing Guide](docs/CONTRIBUTING.md)**

</div>

> **New to programming?** Start with our [Beginner's Guide](docs/BEGINNER_GUIDE.md) for step-by-step setup instructions!

<br>

<div align="center">

_You can replace this text with a GIF or video of FocusSuite once you've created it!_

</div>

---

## Key Features ✨

### Focus Monitor (Distraction Blocker)

- **Real-time Screen Analysis**: Employs **Tesseract OCR** to extract on-screen text for analysis.
- **Intelligent Obscuring**: Uses **OpenAI's gpt-4o** (or a local LLM alternative) to intelligently find and blur distracting content.
- **Efficient Performance**: A smart monitoring loop uses **SSIM image comparison** to detect screen changes, preventing redundant analysis and saving system resources.

### Focus Video (Automated Blurring)

- **Prompt-Based Editing**: Simply describe what you want blurred, and FocusSuite handles the rest.
- **Flicker-Free Results**: It generates a definitive **"blur timeline"** after analyzing keyframes, ensuring the blur is smooth and consistent without the flickering common in frame-by-frame AI analysis.
- **Audio Preservation**: The original audio track is perfectly preserved and re-attached to the final edited video using **MoviePy**.

---

## Tech Stack 🛠️

| Category             | Technology                                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------------------- |
| **UI Framework**     | **Tkinter** (with modern themed widgets)                                                                   |
| **AI & LLM**         | **OpenAI (gpt-4o)**, **Tesseract OCR**, Local LLM via Worker Endpoint                                      |
| **Video Processing** | **OpenCV**, **MoviePy**                                                                                    |
| **Image Analysis**   | **Pillow**, **scikit-image**                                                                               |
| **System Tools**     | **pystray** (for system tray icon), **keyboard** (for global hotkeys), **pywin32** (for Windows functions) |

---

## 🚀 Quick Start

### For Beginners

👋 **New to programming?** Follow our step-by-step [Beginner's Guide](docs/BEGINNER_GUIDE.md)!

### For Developers

```bash
git clone https://github.com/jassu2244/FocusSuite.git
cd FocusSuite
pip install -r requirements.txt
python FocusSuite/main.py
```

### Prerequisites

- **Python 3.9+** ([Download here](https://python.org/downloads/))
- **Tesseract OCR** ([Installation guide](docs/BEGINNER_GUIDE.md#step-2-install-tesseract-text-recognition-️))
- **OpenAI API Key** (optional but recommended)

> **💡 Tip**: The complete setup takes about 30 minutes for beginners, 5 minutes for experienced developers.

---

## Architecture Highlights 🏗️

This project is built on a foundation of clean, maintainable code principles.

- **Separation of Concerns (SoC)**: The application is strictly modularized. The UI (`ui/`), core logic (`core/`), and external API communication (`api/`) are completely decoupled, making the system easy to scale and test.
- **Callback-Driven UI**: The core application logic is headless and has no direct knowledge of the UI. It communicates with the Tkinter front-end via a dictionary of callback functions, meaning the user interface can be completely replaced without affecting the backend.
- **Encapsulated Feature Managers**: Each major feature is orchestrated by a dedicated manager (e.g., `FocusMonitorManager`, `VideoFeatureManager`). The main `app.py` orchestrator simply delegates tasks, keeping the central logic clean and readable.

---

## Contributing 🤝

We welcome contributions from developers of all skill levels!

### Quick Start for Contributors

1. **Read the [Contributing Guide](docs/CONTRIBUTING.md)** - Complete guide for developers
2. **Check [open issues](https://github.com/jassu2244/FocusSuite/issues)** - Look for `good first issue` labels
3. **Fork the repository** and create a feature branch
4. **Submit a pull request** with your improvements

### Areas We Need Help With

- 🌍 **Cross-platform support** (Linux/macOS)
- ⚡ **Performance optimizations**
- 🎨 **UI/UX improvements**
- 🧪 **Testing and documentation**
- 🔌 **New API integrations**

**New to open source?** Check out issues labeled `good first issue` - they're perfect for getting started!

---

## Documentation 📚

| Document                                            | Purpose                           | Audience                     |
| --------------------------------------------------- | --------------------------------- | ---------------------------- |
| **[Beginner's Guide](docs/BEGINNER_GUIDE.md)**      | Step-by-step setup for newcomers  | New users, non-programmers   |
| **[Complete Documentation](docs/DOCUMENTATION.md)** | Comprehensive technical guide     | Developers, advanced users   |
| **[Contributing Guide](docs/CONTRIBUTING.md)**      | Development and contribution info | Contributors, maintainers    |
| **[Project Overview](docs/PROJECT_OVERVIEW.md)**    | Complete project understanding    | Project owners, stakeholders |
| **[README.md](README.md)**                          | Project overview and quick start  | Everyone                     |

---

## License 📜

Distributed under the MIT License. See `LICENSE` for more information.
