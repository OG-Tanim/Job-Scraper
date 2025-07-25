from playwright.sync_api import sync_playwright
from config import load_companies
from typing import List, Dict

def scrape_company_jobs(name: str, url: str) -> List[Dict[str, str]]:
    """
    Scrape job postings from a website.

    Args:
        name (str): The name of the company.
        url (str): The URL of the website to scrape.

    Returns:
        List[Dict[str, str]]: A list of job postings as dictionaries.
    """
    print(f"[*] Scraping: {name} ({url})")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(3000)  # Wait for JS to render

            links_data = []

            # Example: try to get all job link elements
            links = page.query_selector_all("a")
            for link in links:
                text = link.inner_text().strip()
                href = link.get_attribute("href")
                parent_text = el.evaluate("node => node.closest('section, div')?.innerText || ''")
                if text and href:
                    links_data.append({
                         "href": href,
                "text": text,
                "context": parent_text[:500]  # limit context length
                    })

            return links_data
        
        except Exception as e:
            print(f"[!] Error scraping {name}: {e}")
            return []
        finally:
            browser.close()

def scrape_all_jobs() -> List[Dict[str, str]]:
    companies = load_companies()
    all_jobs = []
    for company in companies:
        jobs = scrape_company_jobs(company["name"], company["url"])
        all_jobs.extend(jobs)
    return all_jobs










