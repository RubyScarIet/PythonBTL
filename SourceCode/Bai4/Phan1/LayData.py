import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configure the Chrome browser for Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Run browser in headless mode (without GUI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# List to store data of all players
all_rows = []
column_names = []

# Loop through pages of data on the website
for page in range(1, 23):
    url = f"https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players/playing-in-uk-premier-league/{page}"
    success = False

    # Retry up to 3 times if there's an error while collecting data
    for attempt in range(3):
        try:
            # Access the page and scroll down to load the entire content
            driver.get(url)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Wait until the player table appears
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "player-table-body"))
            )
            # Get the page source after it's fully loaded
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract column names if not already extracted
            if not column_names:
                thead = soup.find('thead')
                if thead:
                    headers = [th.get_text(strip=True) for th in thead.find_all('th')]
                    column_names = headers

            # Extract the data rows from the table
            tbody = soup.find('tbody', id='player-table-body')
            rows_added = 0
            if tbody:
                for row in tbody.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) < 2:  # Skip rows that don't have enough data
                        continue

                    # Get the player's name and team
                    a_player = cols[0].find('a')
                    player = a_player.get_text(strip=True) if a_player else cols[0].get_text(strip=True)

                    a_team = cols[1].find('a')
                    team = a_team.get_text(strip=True) if a_team else cols[1].get_text(strip=True)

                    # Extract other data in the row
                    other_data = [c.get_text(strip=True) for c in cols[2:]]
                    row_data = [player, team] + other_data

                    # If the row contains valid data, add it to the list
                    if any(cell for cell in row_data):
                        all_rows.append(row_data)
                        rows_added += 1

            print(f"✅ Page {page}: Added {rows_added} valid data rows")
            success = True
            break
        except Exception as e:
            print(f"[!] Error on page {page} ({attempt+1}/3): {e}")
            time.sleep(2)

    # If the page failed after 3 attempts, report it
    if not success:
        print(f"[❌] Page {page} failed after 3 attempts")

# Close the browser once the process is complete
driver.quit()

# Save all the collected data into a CSV file
df = pd.DataFrame(all_rows, columns=column_names)
df.to_csv("GiaTriCauThu.csv", index=False, encoding='utf-8-sig')
print(f"✅ Total: {len(df)} rows have been saved to 'GiaTriCauThu.csv'")

#  Wait before processing the data
time.sleep(2)

#  Import and process data AFTER CSV file has been created
import XuLyData as XL
XL.XoaHeader(["Skill/ pot"], "GiaTriCauThu.csv", "GiaTriCauThu.csv")  # Remove 'Skill/ pot' column
XL.DoiTen("#", "STT", "GiaTriCauThu.csv", "GiaTriCauThu.csv")  # Rename '#' column to 'STT'
XL.DoiTen("Team", "Squad", "GiaTriCauThu.csv", "GiaTriCauThu.csv")  # Rename 'Team' column to 'Squad'
XL.ChuanHoaTen("GiaTriCauThu.csv", "GiaTriCauThu.csv")  # Normalize player names
XL.ChuanHoaTen2("GiaTriCauThu.csv", "GiaTriCauThu.csv")  # Normalize player names again
XL.ChuanHoaSquad("GiaTriCauThu.csv", "GiaTriCauThu.csv")  # Normalize squad/team names
