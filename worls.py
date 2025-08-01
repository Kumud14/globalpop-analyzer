#!/usr/bin/env python
# coding: utf-8

# In[48]:


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
options.add_argument("--headless")  # Comment this if you want to see the browser
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# --- Setup driver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# --- Open page ---
driver.get("https://www.worldometers.info/world-population/")
wait = WebDriverWait(driver, 20)

# --- Wait for world population counter to load ---
try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.rts-counter[rel='current_population']")))
    
    # RE-LOCATE fresh to avoid stale reference
    population_element = driver.find_element(By.CSS_SELECTOR, "span.rts-counter[rel='current_population']")
    spans = population_element.find_elements(By.TAG_NAME, "span")
    world_population = ''.join([s.text for s in spans])

except Exception as e:
    print("❌ Error while retrieving World Population:", str(e))
    world_population = "N/A"

# --- Helper to get other values ---
def get_text(by, value):
    try:
        return driver.find_element(by, value).text.strip()
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
csv_file = "population_counters5.csv"
file_exists = os.path.isfile(csv_file)
df.to_csv(csv_file, mode='a', index=False, header=not file_exists)

# --- Show output ---
print("✅ Data saved to:", csv_file)
print(df)


# In[ ]:




