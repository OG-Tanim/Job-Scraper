from config import load_companies

def main():
    companies = load_companies()
    for company in companies:
        print(f"[+] Loaded: {company['name']} ->{company['url']}")


if __name__ == "__main__":
    main()