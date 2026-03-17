# 🧠 DEV.BG Job Hunter (.NET)

A Python-based job scraper and matcher that scans DEV.BG for .NET jobs and intelligently ranks them based on how well they match your personal tech stack.

Perfect for developers who want to automate job searching and quickly identify the most relevant opportunities.

---

## 🚀 Features

- 🔍 Scrapes .NET job listings from DEV.BG (including remote jobs)
- 📄 Opens each job and extracts full description
- 🧠 Matches jobs against your real CV tech stack
- 📊 Calculates a realistic match percentage
- 🧾 Shows matched skills for each job
- 🆕 Tracks only new job listings
- 📁 Saves daily logs of results
- 🔔 Sends Windows notifications

---

## 🧩 How It Works

Instead of naive keyword matching, the script:

1. Extracts job descriptions
2. Detects which technologies are mentioned
3. Compares them against your actual skills
4. Scores based on overlap

### ✅ Example

Job requires:
.NET, C#, SQL, Docker

You have:
.NET, C#, SQL

Match = 3 / 4 = 75%

---

## 🛠️ Tech Stack

- Python 3
- requests
- BeautifulSoup (bs4)
- win10toast

---

## 📦 Installation

pip install requests beautifulsoup4 win10toast

---

## ⚙️ Configuration

### 🔗 Job Search URL

BASE_URL = "https://dev.bg/company/jobs/net/?_job_location=remote"

---

### 🏷️ Tag

TAG = "devbg_net_remote"

---

### 🧠 Your Skills

Customize this list:

SKILLS = [
    ".net",
    "c#",
    "asp.net",
    "asp.net core",
    "web api",
    "entity framework",
    "dapper",
    "sql",
    "mssql",
    "postgres",
    "react",
    "javascript",
    "typescript",
    "html",
    "css",
    "nodejs",
    "docker",
    "git",
    "github"
]

---

## ▶️ Usage

python job_scraper.py

---

## 📊 Example Output

72% match
Senior .NET Developer | SAP
Matched skills: .net, c#, entity framework, docker, sql

---

## 📁 Output Files

seen_devbg_net_remote.json

daily_logs/jobs_YYYY-MM-DD.txt

---

## 🔔 Notifications

Windows toast notification when new jobs are found.

---

## 🧠 Matching Logic

match % = (matched skills) / (skills found in job description)

---

## ⚡ Future Improvements

- AI-based job matching
- Telegram notifications
- Multi-platform scraping
- Auto-run scheduler

---
