import requests
from playwright.sync_api import sync_playwright
from config import load_companies
from typing import List, Dict

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HEADERS = {
    #"Authorization": f""
}

def is_job_posting(html: str) -> bool:
    """
    Sends HTML content to Hugging Face zero-shot classifier to determine if it's a job post.
    """
    payload = {
        "inputs": html,
        "parameters": {
            "candidate_labels": ["JobPosting", "NotJobPosting"]
        }
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"[!] HuggingFace API error: {response.status_code} - {response.text}")
        return False

    result = response.json()
    if not result or "labels" not in result:
        return False

    return result["labels"][0] == "JobPosting" and result["scores"][0] >= 0.7


def scrape_company_jobs(name: str, url: str) -> List[Dict[str, str]]:
    """
    Scrape job postings from a website using AI classification.

    Args:
        name (str): Company name.
        url (str): Careers page URL.

    Returns:
        List[Dict[str, str]]: List of identified job postings.
    """
    print(f"[*] Scraping: {name} ({url})")
    job_posts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(3000)

            elements = page.query_selector_all("section, article, div")
            print(f"[+] Found {len(elements)} elements")

            for el in elements:
                outer_html = el.inner_html()
                if outer_html and len(outer_html) > 100:
                    try:
                        if is_job_posting(outer_html):
                            job_posts.append({
                                "company": name,
                                "html": outer_html,
                                "url": url
                            })
                    except Exception as e:
                        print(f"[!] Classification error: {e}")
        except Exception as e:
            print(f"[!] Error scraping {name}: {e}")
        finally:
            browser.close()

    print(f"[+] Found {len(job_posts)} job posts for {name}")
    return job_posts


def scrape_all_jobs() -> List[Dict[str, str]]:
    """
    Scrapes all job postings from all companies.

    Returns:
        List[Dict[str, str]]: All classified job postings.
    """
    companies = load_companies()
    all_jobs = []
    for company in companies:
        jobs = scrape_company_jobs(company["name"], company["url"])
        all_jobs.extend(jobs)
    return all_jobs










