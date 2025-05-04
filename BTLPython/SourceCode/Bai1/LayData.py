from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Comment
import time
import csv

# Utility: Save extracted table data to a CSV file
def write_csv(filename, data, header=None):
    with open(filename, mode="w", encoding="utf-8-sig", newline="") as fout:
        writer = csv.writer(fout)
        if header:
            writer.writerow(header)
        writer.writerows(data)

# Utility: Extract the last row of the table header (<thead>)
def extract_headers(table):
    thead = table.find("thead")
    if not thead:
        return []
    last_row = thead.find_all("tr")[-1]
    return [cell.get_text(strip=True).replace('\xa0', ' ') for cell in last_row.find_all(["th", "td"])]

# Setup: Configure Chrome in headless mode (no GUI)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize Chrome driver using webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Dictionary of target URLs and their corresponding table IDs
pages = {
    "https://fbref.com/en/comps/9/stats/Premier-League-Stats": "stats_standard",
    "https://fbref.com/en/comps/9/keepers/Premier-League-Stats": "stats_keeper",
    "https://fbref.com/en/comps/9/shooting/Premier-League-Stats": "stats_shooting",
    "https://fbref.com/en/comps/9/passing/Premier-League-Stats": "stats_passing",
    "https://fbref.com/en/comps/9/gca/Premier-League-Stats": "stats_gca",
    "https://fbref.com/en/comps/9/defense/Premier-League-Stats": "stats_defense",
    "https://fbref.com/en/comps/9/possession/Premier-League-Stats": "stats_possession",
    "https://fbref.com/en/comps/9/misc/Premier-League-Stats": "stats_misc"
}

tables = {}

# Iterate through all URLs and scrape the target table
for url, table_id in pages.items():
    print(f"\n🌐 Loading: {url}")
    driver.get(url)
    time.sleep(3)  # Wait for page to fully load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Some tables are hidden inside HTML comments -> parse them manually
    table = None
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment_soup = BeautifulSoup(comment, "html.parser")
        table = comment_soup.find("table", id=table_id)
        if table:
            break

    # Fallback: Try to find the table directly in the DOM
    if not table:
        table = soup.find("table", id=table_id)

    if not table:
        print(f"❌ Table '{table_id}' not found.")
        continue

    print(f"✅ Found table: {table_id}")
    header = extract_headers(table)
    print(f"📋 Header ({table_id}): {header}")

    # Extract all table rows (<tbody>) and skip pseudo-header rows
    table_data = []
    tbody = table.find("tbody")
    if tbody:
        for row in tbody.find_all("tr"):
            if row.get("class") and "thead" in row["class"]:
                continue  # Skip internal header rows
            cells = row.find_all(["th", "td"])
            row_data = [cell.get_text(strip=True) for cell in cells]
            if len(row_data) == len(header):
                table_data.append(row_data)

    # Store table data with corresponding header
    tables[table_id] = {"header": header, "data": table_data}

# Close the browser after scraping
driver.quit()

# Save each scraped table as a separate CSV file
for table_id, content in tables.items():
    filename = f"{table_id}.csv"
    write_csv(filename, content["data"], header=content["header"])
    print(f"💾 Saved {filename} ({len(content['data'])} rows)")
