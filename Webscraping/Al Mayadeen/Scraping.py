from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# open the page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.almayadeen.net/news')

# Define WebDriverWait to use later for waiting elements to be clickable
wait = WebDriverWait(driver, 10)

# click on any load more button that exists
click_count = 0
max_clicks = 2

while click_count < max_clicks:
    try:
        # Use WebDriverWait to wait for the Load More button to be clickable
        load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "loadmorebtn")))

        # Scroll to the button before clicking 
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)

        # Click the button
        load_more_button.click()

        # Wait for the content to load before the next click
        time.sleep(3)
        
        # Increment the click counter
        click_count += 1
    except Exception as e:
        print(f"An error occurred: {e}")
        break  

# Now we have all the divs 

# After clicking "Load More" as needed, wait for the news items to appear
news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.no-gap.white-bg-colored.all-bordered")))

# Prepare a list to hold the news data
news_data = []

# Ensure the container for news items is present
news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.no-gap.white-bg-colored.all-bordered")))

for item in news_items:
    # Extract the href and title from the anchor tag within h4 with class 'item title'
    href = driver.find_element(By.CSS_SELECTOR, "div.white-card a").get_attribute("href")    
    title = driver.find_element(By.CSS_SELECTOR, "div.white-card a > h4").text    
    # Extract the category
    category = driver.find_element(By.CSS_SELECTOR, "a.category-meta").text    
    # Extract the date
    date = item.find_element(By.CSS_SELECTOR, "div.time p").text.strip()
    
    # Extract the country from the alt attribute of the img within 'div.img_icon'
    country= driver.find_element(By.CSS_SELECTOR, "div.country-img img").get_attribute("alt")
    
    # Append the collected data to our list
    news_data.append({
        'href': href,
        'title': title,
        'category': category,
        'date': date,
        'country': country
    })

driver.quit()

# lets save the data we took
# Specify the filename
filename = 'news_data.json'

# Writing JSON data
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print(f"Data saved to {filename}")

