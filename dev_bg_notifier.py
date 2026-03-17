import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
from win10toast import ToastNotifier

# -------------------------------
# CONFIG
# -------------------------------

BASE_URL = "https://dev.bg/company/jobs/net/?_job_location=remote"
TAG = "devbg_net_remote"

HEADERS = {"User-Agent": "Mozilla/5.0"}

DATA_FILE = f"seen_{TAG}.json"
LOG_FOLDER = "daily_logs"

# Skills extracted from your CV
SKILLS = [
".net",
"c#",
"asp.net",
"asp.net core",
"web api",
"rest api",
"entity framework",
"dapper",
"sql",
"mssql",
"postgres",
"postgresql",
"sqlite",
"react",
"reactjs",
"javascript",
"typescript",
"html",
"css",
"node",
"nodejs",
"docker",
"git",
"github"
]

# -------------------------------
# FETCH JOB LIST
# -------------------------------

def fetch_jobs(page):

    url = f"{BASE_URL}&_paged={page}"

    response = requests.get(url, headers=HEADERS, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    cards = soup.find_all("div", class_="job-list-item")

    for card in cards:

        title_tag = card.find("h6", class_="job-title")
        company_tag = card.find("span", class_="company-name")
        link_tag = card.find("a", class_="overlay-link")
        date_tag = card.find("span", class_="date")

        if not title_tag or not link_tag:
            continue

        jobs.append({
            "title": title_tag.text.strip(),
            "company": company_tag.text.strip() if company_tag else "N/A",
            "date": date_tag.text.strip() if date_tag else "N/A",
            "link": link_tag["href"]
        })

    return jobs


# -------------------------------
# FETCH JOB DESCRIPTION
# -------------------------------

def fetch_job_description(url):

    try:

        r = requests.get(url, headers=HEADERS, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        article = soup.find("article")

        if article:
            return article.get_text(" ", strip=True).lower()

        return soup.get_text(" ", strip=True).lower()

    except:
        return ""


# -------------------------------
# MATCH SCORING
# -------------------------------

def score_job(text):

    text = text.lower()

    job_skills = []
    matched_skills = []

    for skill in SKILLS:
        if skill in text:
            job_skills.append(skill)

            # since skills list represents your CV skills
            matched_skills.append(skill)

    if len(job_skills) == 0:
        return 0, []

    score = int((len(matched_skills) / len(job_skills)) * 100)

    return score, matched_skills

# -------------------------------
# SCRAPE ALL PAGES
# -------------------------------

def scrape_all_pages():

    page = 1
    all_jobs = []
    last_page = None

    while True:

        print(f"Fetching page {page}")

        jobs = fetch_jobs(page)

        if not jobs:
            break

        if last_page and jobs == last_page:
            break

        all_jobs.extend(jobs)

        last_page = jobs

        page += 1

        time.sleep(1)

    print("Total jobs found:", len(all_jobs))

    return all_jobs


# -------------------------------
# SEEN JOBS
# -------------------------------

def load_seen():

    if os.path.exists(DATA_FILE):

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return []


def save_seen(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -------------------------------
# LOGGING
# -------------------------------

def save_daily_log(jobs):

    os.makedirs(LOG_FOLDER, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    filename = os.path.join(LOG_FOLDER, f"jobs_{today}.txt")

    with open(filename, "a", encoding="utf-8") as f:

        for job in jobs:

            f.write(
                f"{job['match']}% | {job['title']} | {job['company']}\n"
            )

            f.write(f"Skills: {', '.join(job['skills'])}\n")

            f.write(f"{job['link']}\n\n")


# -------------------------------
# WINDOWS NOTIFICATION
# -------------------------------

def notify(title, message):

    toaster = ToastNotifier()

    toaster.show_toast(title, message, duration=10, threaded=True)

    while toaster.notification_active():
        time.sleep(0.1)


# -------------------------------
# MAIN
# -------------------------------

def main():

    seen = load_seen()

    seen_links = {j["link"] for j in seen}

    jobs = scrape_all_pages()

    new_jobs = [j for j in jobs if j["link"] not in seen_links]

    if not new_jobs:

        print("No new jobs.")
        return

    print(f"\nNew jobs: {len(new_jobs)}")

    results = []

    for job in new_jobs:

        print("Analyzing:", job["title"])

        desc = fetch_job_description(job["link"])

        score, skills = score_job(desc)

        job["match"] = score
        job["skills"] = skills

        results.append(job)

        time.sleep(1)

    results.sort(key=lambda x: x["match"], reverse=True)

    print("\nBEST JOB MATCHES\n")

    for job in results[:10]:

        print(f"{job['match']}% match")
        print(job["title"], "|", job["company"])
        print("Matched skills:", ", ".join(job["skills"]))
        print(job["link"])
        print()

    save_daily_log(results)

    seen.extend(new_jobs)

    save_seen(seen)

    notify("DEV.BG Job Hunter", f"{len(new_jobs)} new jobs analyzed")


# -------------------------------

if __name__ == "__main__":
    main()