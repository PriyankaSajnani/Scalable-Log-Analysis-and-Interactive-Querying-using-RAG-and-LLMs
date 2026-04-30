# 🔍 LogLens – AI-Powered Windows System Log Analyzer (RAG + LLaMA)

LogLens is an automated Windows Event Log analysis tool that fetches, cleans, and analyzes system logs using Python and Retrieval-Augmented Generation (RAG).  
It provides AI-generated summaries, root cause hints, risk identification, and interactive chat-based troubleshooting using a locally hosted LLM (LLaMA via Ollama).

---

## 🚀 Key Features
- Automated Windows Event Log collection (System logs)
- Severity-based filtering (Error / Warning / Critical)
- Duplicate log removal and preprocessing pipeline
- Retrieval using TF-IDF + cosine similarity (RAG approach)
- AI-powered log explanation and summarization using LLaMA (Ollama)
- Interactive CLI-based log assistant for queries and troubleshooting
- Offline AI support (runs locally, no cloud dependency)
- Packaged Windows installer available via GitHub Releases

---

## 🛠️ Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn (TF-IDF, cosine similarity)
- PyWin32 (Windows Event Logs)
- Ollama (LLaMA 3.2)
- Tkinter (GUI for file selection)
- PowerShell (launcher automation)

---

## 📌 Project Workflow
LogLens works in a complete pipeline:

1. **fetching.py** → Fetches Windows System Event Logs and exports to CSV  
2. **processing.py** → Cleans logs (filtering, duplicate removal, preprocessing)  
3. **analysis.py** → Applies RAG + LLM to generate insights and interactive log chat

---
## 🎥 Demo Video
📌 Watch the working demo here:  
[LogLens Project Demo](https://www.youtube.com/watch?v=vJXvizxYr3Y)

---

## 📸 Screenshots

### 1️⃣ Log Fetching + Processing
![Log Fetching](assets/fetching_processing.jpeg)

### 2️⃣ AI Summary Report Generation
![AI Summary](assets/Summary.jpeg)

### 3️⃣ Interactive Log Chat
![Interactive Chat](assets/Interactive-log_chat.png)

---

## ⚙️ Installation

### Option 1: Install using Windows Installer (Recommended)
Download the latest installer from GitHub Releases:

➡️ [Download LogLens Installer](../../releases)

---

### Option 2: Run from Source Code

#### 1. Clone the repository
```bash
git clone https://github.com/your-username/LogLens.git
cd LogLens
