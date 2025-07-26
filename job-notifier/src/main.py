from config import load_companies
from scraper import scrape_all_jobs

def main():
    print("== Starting Job Scraper ==")
    jobs = scrape_all_jobs()
    print(f"\n✅ Total Jobs Found: {len(jobs)}\n")

    for job in jobs:
        print(f"{job['company']} → {job['title']} ({job['link']})")


    
    companies = load_companies()
    for company in companies:
        print(f"[+] Loaded: {company['name']} ->{company['url']}")


if __name__ == "__main__":
    main()
