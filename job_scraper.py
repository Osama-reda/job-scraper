# Job Scraper - python.org/jobs
# pip install requests beautifulsoup4 pandas openpyxl lxml

import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

BASE_URL = "https://www.python.org/jobs/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

print("=" * 45)
print("      Python.org Jobs Scraper")
print("=" * 45)

keyword = input("\nEnter a keyword to filter jobs (or press Enter for all): ").strip()

# Fetch all pages
print("\nConnecting to python.org/jobs ...")
response = requests.get(BASE_URL, headers=HEADERS)
first_page = response.text

soup = BeautifulSoup(first_page, "lxml")
page_numbers = []
for link in soup.select("ul.pagination a"):
    text = link.get_text(strip=True)
    if text.isdigit():
        page_numbers.append(int(text))

total_pages = max(page_numbers) if page_numbers else 1
print(f"Found {total_pages} page(s) of jobs.")

all_pages_html = [first_page]
for page_num in range(2, total_pages + 1):
    time.sleep(1)
    response = requests.get(f"{BASE_URL}?page={page_num}", headers=HEADERS)
    all_pages_html.append(response.text)
    print(f"  Fetched page {page_num}/{total_pages}")

# Parse jobs
jobs_list = []

for page_html in all_pages_html:
    soup = BeautifulSoup(page_html, "lxml")

    for card in soup.select("ol.list-recent-jobs li"):
        title_tag = card.select_one("h2.listing-company a")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        href = title_tag["href"] if title_tag else ""
        link = "https://www.python.org" + href if href else "N/A"

        company_span = card.select_one("span.listing-company-name")
        company = "N/A"
        if company_span:
            for tag in company_span.find_all(True):
                tag.extract()
            company = company_span.get_text(strip=True)

        location_tag = card.select_one("span.listing-location a")
        location = location_tag.get_text(strip=True) if location_tag else "N/A"

        job_type_tags = card.select("span.listing-job-type a")
        job_type = ", ".join(tag.get_text(strip=True) for tag in job_type_tags)

        date_tag = card.select_one("span.listing-posted time")
        posted = date_tag.get_text(strip=True) if date_tag else "N/A"

        jobs_list.append({
            "Job Title": title,
            "Company":   company,
            "Location":  location,
            "Job Type":  job_type,
            "Posted":    posted,
            "Link":      link,
        })

print(f"\nTotal jobs scraped: {len(jobs_list)}")

# Filter by keyword
if keyword:
    filtered_jobs = []
    for job in jobs_list:
        if (keyword.lower() in job["Job Title"].lower() or
                keyword.lower() in job["Company"].lower() or
                keyword.lower() in job["Location"].lower() or
                keyword.lower() in job["Job Type"].lower()):
            filtered_jobs.append(job)
    print(f"Jobs matching '{keyword}': {len(filtered_jobs)}")
else:
    filtered_jobs = jobs_list

# Save to Excel
if len(filtered_jobs) == 0:
    print("No jobs found. Try a different keyword.")
else:
    df = pd.DataFrame(filtered_jobs)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    keyword_part = keyword.replace(" ", "_") if keyword else "all"
    filename = f"python_jobs_{keyword_part}_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\nDone! Results saved to: {filename}")
