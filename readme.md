# WhatsApp Chat Viewer (Parser)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
<p align="center">
  <img src="assets/WhatsappParser.png" width="100">
</p>


## Overview

WhatsApp Chat Viewer is a cross-platform desktop application built using PyQt6 that parses exported WhatsApp chat text files and renders them in a user interface closely resembling the native WhatsApp chat experience.

The application is designed to work completely offline and efficiently handle real-world chat data, including large files and edge cases.

---
## Screenshot

<p align="center">
  <img src="assets/screenshot.png" width="300">
</p>

## Objective

The goal of this project is to:

- Convert raw `.txt` WhatsApp chat exports into a structured format
- Visually render chats in a WhatsApp-like interface
- Handle real-world edge cases robustly
- Maintain performance even with large chat files (MBs)

---

## Tech Stack

- **Language:** Python  
- **Framework:** PyQt6  
- **UI Design:** Qt Designer (`.ui` → `pyuic6`)  
- **Architecture:** Modular (Parser + UI + Components)

---

## Project Structure

├── app.py  
├── assets  
│   ├── WP.ico  
│   ├── WhatsappParser.png  
│   ├── screenshot.png  
│   └── bg.jpg  
├── components  
│   ├── message_bubble.py  
│   ├── parser.py  
│   ├── menu.py  
│   └── parser_thread.py  
├── readme.md  
├── requirements.txt  
└── ui  
&emsp;&nbsp; ├── main.ui  
&emsp;&nbsp; └── ui_main.py  

## Application Workflow

## Core Features

### 1. Chat Import
- Supports `.txt` files exported from WhatsApp
- File selection via dialog interface

### 2. Smart Parsing Engine

Handles:
- Standard messages
- Multiline messages
- System messages
- ERROR logs
- Blank messages (displayed as `[Blank Message]`)
- Timestamp extraction

### 3. User Detection
- Automatically extracts participants
- Prompts user selection ("Who are you?")
- Determines message alignment (left/right)

### 4. Chat Rendering System

Custom component: `MessageBubble`

Supports:
- Left/right alignment
- Sender name display
- Timestamp display
- Emoji rendering
- Responsive width
- Word wrapping (HTML-based)

### 5. System Message Handling

Special styling:
- Center-aligned messages
- Light grey background
- Black text

Includes:
- User addition/removal messages
- ERROR logs (with prefix)

### 6. UI/UX Features

- WhatsApp-like chat layout  
- Smooth scrolling  
- Static background image  


### 7. Performance Optimization

#### Threaded Parsing
- Uses `QThread` to avoid UI freezing

#### Lazy Loading
- Loads messages in batches (e.g., 100 at a time)
- Supports infinite scroll behavior

#### Efficient Rendering
- Avoids loading entire chat at once
- Scales effectively for large files (2MB+)

---

## Key Design Decisions

- **Qt Widgets over web frameworks:** Lightweight and native performance
- **Custom rendering instead of QTextEdit:** Full control over UI behavior
- **HTML-based wrapping:** Accurate text layout and emoji handling
- **Manual background painting:** Proper scaling and visual consistency

---

## Output Behavior

| Message Type     | Display        |
|-----------------|---------------|
| Your messages   | Right side    |
| Others          | Left side     |
| System messages | Center        |
| Blank messages  | [Blank Message] |
| ERROR logs      | System styled with prefix |

---


## Possible Extensions (Not yet implemented)

- Message grouping (hide repeated sender names)  
- Chat search functionality
- Analytics (message count, activity timeline)
- Export to HTML or PDF  

---

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package manager)

---

## Running Without Compilation (Development Mode)

1. Clone the repository:
```bash
git clone https://github.com/alokhudali/Whatsapp-Chat-Parser
cd Whatsapp-Chat-Parser
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python app.py
```
This will launch the application directly using Python. Recommended for development and testing.

## Building Executable (PyInstaller)

Make sure PyInstaller is installed:

```bash
pip install pyinstaller
```
### Linux / macOS

```bash
pyinstaller app.py \
--onefile \
--windowed \
--add-data "assets:assets"
```
### Windows
```cmd
pyinstaller app.py --onefile --windowed --icon=assets/WP.ico --add-data "assets;assets"
```
### Output

After compilation: Executable will be available in the dist/ folder
- Linux/macOS: dist/app
- Windows: dist/app.exe

### Notes
- `--onefile` bundles everything into a single executable
- `--windowed` disables terminal/console window
- `--add-data` ensures assets (icons, background) are included
