# FocusSuite

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)](https://github.com/your-username/FocusSuite/releases)

**An intelligent desktop productivity tool to eliminate distractions and streamline video editing.**

</div>

FocusSuite is a Python-based desktop application designed to help users maintain focus. It has two main features:

1. **Focus Monitor**: It actively watches your screen, using AI to identify and obscure distracting text in real-time.
2. **Focus Video**: It processes video files, automatically blurring elements based on a simple descriptive prompt you provide.

<br>

<div align="center">

*You can replace this text with a GIF or video of FocusSuite once you've created it!*

</div>

---
## Key Features ✨

### Focus Monitor (Distraction Blocker)
* **Real-time Screen Analysis**: Employs **Tesseract OCR** to extract on-screen text for analysis.
* **Intelligent Obscuring**: Uses **OpenAI's gpt-4o** (or a local LLM alternative) to intelligently find and blur distracting content.
* **Efficient Performance**: A smart monitoring loop uses **SSIM image comparison** to detect screen changes, preventing redundant analysis and saving system resources.

### Focus Video (Automated Blurring)
* **Prompt-Based Editing**: Simply describe what you want blurred, and FocusSuite handles the rest.
* **Flicker-Free Results**: It generates a definitive **"blur timeline"** after analyzing keyframes, ensuring the blur is smooth and consistent without the flickering common in frame-by-frame AI analysis.
* **Audio Preservation**: The original audio track is perfectly preserved and re-attached to the final edited video using **MoviePy**.

---
## Tech Stack 🛠️

| Category            | Technology                                                                                                  |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| **UI Framework** | **Tkinter** (with modern themed widgets)                                                          |
| **AI & LLM** | **OpenAI (gpt-4o)**, **Tesseract OCR**, Local LLM via Worker Endpoint          |
| **Video Processing**| **OpenCV**, **MoviePy**                                                                           |
| **Image Analysis** | **Pillow**, **scikit-image**                                                                      |
| **System Tools** | **pystray** (for system tray icon), **keyboard** (for global hotkeys), **pywin32** (for Windows functions) |

---
## 🚀 Getting Started

Follow these instructions to get FocusSuite running on your local machine.

### Prerequisites
* **Python 3.9+**
* **Tesseract OCR**
* **FFmpeg**

### Installation & Configuration
1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/FocusSuite.git
    cd FocusSuite
    ```

2.  **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    This will install all necessary packages like `openai`, `opencv-python`, `moviepy`, and others.

3.  **Configure your environment variables:**
    * Create a copy of the example environment file and name it `.env`:
        ```sh
        cp .env.example .env
        ```
    * Open the new `.env` file and add your secret API keys and URLs.

### Running the Application
Once the installation and configuration are complete, you can start the application with:
```sh
python FocusSuite/main.py
```

---
## Architecture Highlights 🏗️
This project is built on a foundation of clean, maintainable code principles.

- **Separation of Concerns (SoC)**: The application is strictly modularized. The UI (`ui/`), core logic (`core/`), and external API communication (`api/`) are completely decoupled, making the system easy to scale and test.
- **Callback-Driven UI**: The core application logic is headless and has no direct knowledge of the UI. It communicates with the Tkinter front-end via a dictionary of callback functions, meaning the user interface can be completely replaced without affecting the backend.
- **Encapsulated Feature Managers**: Each major feature is orchestrated by a dedicated manager (e.g., `FocusMonitorManager`, `VideoFeatureManager`). The main `app.py` orchestrator simply delegates tasks, keeping the central logic clean and readable.

---
## Contributing 🤝
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
## License 📜
Distributed under the MIT License. See `LICENSE` for more information.

