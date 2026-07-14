# Python.org Job Scraper

A simple web scraper that collects job listings from [python.org/jobs](https://www.python.org/jobs/) and saves them to an Excel file.

## Features

- Scrapes all job listings from python.org/jobs
- Filter jobs by any keyword (e.g. "Django", "remote", "backend")
- Saves results to a `.xlsx` Excel file

## Requirements

Install the required libraries before running:

```
pip install requests beautifulsoup4 pandas openpyxl lxml
```

## How to Run

```
python job_scraper.py
```

Then enter a keyword when prompted, or press **Enter** to get all jobs.

## Output

The results are saved as an Excel file in the same folder, for example:

```
python_jobs_backend_20260714_114512.xlsx
```

Each file contains the following columns:

| Column    | Description                  |
|-----------|------------------------------|
| Job Title | Name of the job position     |
| Company   | Company offering the job     |
| Location  | Job location                 |
| Job Type  | Skills/technologies required |
| Posted    | Date the job was posted      |
| Link      | Direct link to the job post  |

## Built With

- [Requests](https://docs.python-requests.org/) — for fetching web pages
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — for parsing HTML
- [Pandas](https://pandas.pydata.org/) — for saving data to Excel
