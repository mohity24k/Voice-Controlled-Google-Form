# Voice-Controlled Google Form Filler 🤖

An AI agent that fills out long Google Forms automatically using voice commands. It uses Selenium for browser automation and SpeechRecognition for voice inputs.

## Features
- 🗣️ **Voice Navigation:** Say "Option 1", "Next", or "Back".
- 🦊 **Firefox Support:** Runs natively on Firefox (via GeckoDriver).
- 🛑 **Smart Exit:** Says "Submit" to finish and close the app.
- 🔴 **Visual Feedback:** Highlights the current question being answered.

## Prerequisites
- Python 3.8+
- Firefox Browser installed
- A working Microphone

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   
2. **Create a Virtual Environment (Recommended):**  

**Linux/Mac**
```bash
python3 -m venv venv
source venv/bin/activate
```

 **Windows**
 ```bash
python -m venv venv
venv\Scripts\activate
```
3. **Install Dependencies:**
Note: Linux users may need to install `portaudio19-dev` first (`sudo apt install portaudio19-dev`).
```bash
pip install -r requirements.txt
```

## Usage

1. Open `agent.py` and replace `FORM_URL` with your specific Google Form link.
2. Run the agent:
 ```bash
python agent.py
   ```
3. Speak commands clearly:
   
    "Option 1", "First one"

    "Next", "Skip"

    "Back"

    "Submit"

    "Stop"
   
