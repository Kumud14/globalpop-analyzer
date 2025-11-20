# In[ ]:

# !/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
import time
import os

# --- Chrome options ---
options = Options()
# Add a user-agent to mimic a real browser
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--headless")  # Comment this if you want to see the browser
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# --- Setup driver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# --- Open page ---
driver.get("https://www.worldometers.info/world-population/")
# Increased wait time for more reliability
wait = WebDriverWait(driver, 30)

# --- Wait for world population counter to load and get text ---
try:
    # Wait for the element to be VISIBLE, which is more robust
    population_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.rts-counter[rel='current_population']")))
    # Get the text directly. Selenium will concatenate the text from child spans.
    world_population = population_element.text
except Exception as e:
    print("❌ Error while retrieving World Population:", str(e))
    world_population = "N/A"

# --- Helper to get other values ---
def get_text(by, value):
    try:
        # It's better to wait for each element briefly to handle dynamic loading
        element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((by, value)))
        return element.text.strip()
    except:
        return "N/A"

# --- Gather all data ---
data = {
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "World Population": world_population,
    "Births Today": get_text(By.CSS_SELECTOR, "span[rel='births_today']"),
    "Deaths Today": get_text(By.CSS_SELECTOR, "span[rel='dth1s_today']"),
    "Net Growth Today": get_text(By.CSS_SELECTOR, "span[rel='absolute_growth']"),
    "Births This Year": get_text(By.CSS_SELECTOR, "span[rel='births_this_year']"),
    "Deaths This Year": get_text(By.CSS_SELECTOR, "span[rel='dth1s_this_year']"),
    "Net Growth This Year": get_text(By.CSS_SELECTOR, "span[rel='absolute_growth_year']")
}

driver.quit()

# --- Save to CSV ---
df = pd.DataFrame([data])
csv_file = "population5.csv"
file_exists = os.path.isfile(csv_file)
df.to_csv(csv_file, mode='a', index=False, header=not file_exists)

# --- Show output ---
print("✅ Data saved successfully to:", csv_file)
print(df)


