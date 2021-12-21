from bs4 import BeautifulSoup

def extract_name(soup):
    try:
        return soup.find("div", {"class": "jobs-unified-top-card t-14 artdeco-card mb4"})
    except:
        print("Couldn't extract job name.")

def extract_description(soup):
    try:
        return soup.find("div", {"id": "job-details"})
    except:
        print("Couldn't extract job description.")

def extract_poster(soup):
    try:
        return soup.find(
            "div", {"class": "jobs-description__details"})
    except:
        print("Couldn't extract job poster.")
    
def extract_salary(soup):
    try:
        return soup.find("div", {"id": "SALARY"})
    except:
        print("Couldn't extract job salary.")

def extract_company(soup):
    try:
        return soup.find("div", {"class": "jobs-company__box"})
    except:
        print("Couldn't extract job company.")

def extract_info(source_code):
    soup = BeautifulSoup(source_code, "html.parser")
    extracted_date = {}

    # Extract job name
    extracted_date["job_name"] = extract_name(soup)

    # Extract job description
    extracted_date["job_descr"] = extract_description(soup)
    
    # Extract job poster
    extracted_date["job_poster"] = extract_poster(soup)

    # Extract job salary
    extracted_date["job_salary"] = extract_salary(soup)

    # Extract job company
    extracted_date["job_company"] = extract_company(soup)

    return extracted_date
    