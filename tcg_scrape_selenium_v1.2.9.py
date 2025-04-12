# 1.2.5 - This version calculates the price differential from the market price and only includes 30%+ differentials in the CSV
# 1.2.6 - This version attempts to sort listings by best selling
# 1.2.7 - Added functionality to wait for certain problematic elements to be loaded
# 1.2.8 - According to my most recent test, 1.2.8 is not broken and is working as intended.
# 1.2.9 - Script now ignores listings that contain pictures of foreign cards with the same name, as this screws up the price differentials.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Element with {by}='{value}' not found within {timeout} seconds")
        return None

def scrape_tcgplayer(url, num_pages):
    driver = webdriver.Chrome()
    driver.get(url)
    page_number = 1

    while page_number <= num_pages:
        print(f"Scraping page {page_number}...")
        
        try:
            search_results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-result'))
            )
        except TimeoutException:
            print("No search results found. Exiting...")
            break

        if not search_results:
            print(f"Completed scraping all specified pages of data.")
            break

        # Sort by Best Selling
        if page_number == 1:
            try:
                sort_button = wait_for_element(driver, By.XPATH, '//div[@class="tcg-input-field__content"]')
                if sort_button:
                    sort_button.click()
                    best_selling_option = wait_for_element(driver, By.XPATH, '//li[@aria-label="Best Selling"]')
                    if best_selling_option:
                        best_selling_option.click()
            except Exception as e:
                print(f"Sort dropdown not found or clickable. Exiting... Error: {e}")
                break

        if page_number == 1:
            mode = 'w'
        else:
            mode = 'a'
        with open('tcgplayer_data.csv', mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            if page_number == 1:
                writer.writerow(['Title', 'Category', 'Condition', 'Price', 'Market Price', 'Differential', 'Page'])
                
            for result in search_results:
                try:
                    condition_elem = wait_for_element(result, By.CLASS_NAME, 'listing-item__listing-data__info__condition')
                    title_elem = wait_for_element(result, By.CLASS_NAME, 'product-info__title.truncate')
                    meta_elem = wait_for_element(result, By.CLASS_NAME, 'product-info__meta')  # Combined category and subtitle
                    # category_elem = wait_for_element(result, By.CLASS_NAME, 'product-info__meta') ---- This is normally 'product-info__category-name' -- I have changed it to try scraping YuGiOh booster boxes
                    # Actually, it seems that the website's structure has changed and Titles/Subtitles etc have been wrapped into product-info_meta. Script has been repurposed to reflect this.
                    # I believe that I was wrong again, and it's just a different format for booster boxes. Will deal with this later. 
                    price_elem = wait_for_element(result, By.CLASS_NAME, 'listing-item__listing-data__info__price')
                    market_price_elem = wait_for_element(result, By.CLASS_NAME, 'product-info__market-price--value')

                    if None not in (condition_elem, title_elem, meta_elem, price_elem, market_price_elem):
                        condition = condition_elem.text.strip()
                        title = title_elem.text.strip()
                        meta = meta_elem.text.strip()  # Combined category and subtitle
                        price = float(price_elem.text.strip().replace('$', ''))
                        market_price = float(market_price_elem.text.strip().replace('$', ''))

                        differential = 1 - (price / market_price)
                        if differential >= 0.3:
                            writer.writerow([title, meta, condition, price, market_price, differential, page_number])
                            print(f"Title: {title}, Meta: {meta}, Condition: {condition}, Price: {price}, Market Price: {market_price}, Differential: {differential}, Page Number: {page_number}")
                    
                except Exception as e:
                    print(f"Error: {e}")

        print(f"Page {page_number} done.")
        page_number += 1
        
        # Click the next page button
        try:
            next_page_button = wait_for_element(driver, By.XPATH, '//a[@aria-label="Next page"]')
            if next_page_button:
                next_page_button.click()
            else:
                print("Next page button not found. Exiting...")
                break
        except Exception as e:
            print(f"Next page button not found. Exiting... Error: {e}")
            break

        time.sleep(3)

    print("All specified price data has been scraped.")
    driver.quit()

if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    num_pages = int(input("Enter the number of pages to scrape: "))
    scrape_tcgplayer(url, num_pages)
