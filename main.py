from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pymongo
import time
from dotenv import load_dotenv
import os
load_dotenv()

DB_ATLAS = os.getenv("DB_ATLAS")
print("DB_ATLAS", DB_ATLAS)
def scrape_bse_website():
    CHROME_DRIVER_PATH = r"C:\Users\Shubham Sharma\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"



    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

  
    driver.get("https://www.bseindia.com")

   
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

   
    h1_elements = soup.find_all("h1")
    p_elements = soup.find_all("p")

    
    h1_texts = [element.text.strip() for element in h1_elements]
    p_texts = [element.text.strip() for element in p_elements]

    
    combined_data = [{"h1": h1_text, "p": p_text} for h1_text, p_text in zip(h1_texts, p_texts)]

    return combined_data

def save_to_mongodb(data):
    client = pymongo.MongoClient(DB_ATLAS)
    db = client["bse_data"]
    collection = db["homepage_data"]
    if data:  
        collection.insert_many(data)
        print("Data saved to MongoDB")
    else:
        print("No data to save")

def main():
    scraped_data = scrape_bse_website()  
    save_to_mongodb(scraped_data)  

if __name__ == "__main__":
    main()
