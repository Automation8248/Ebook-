import os
import time
import random
import requests
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Telegram Config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
IMG_FOLDER = "images"

if not os.path.exists(IMG_FOLDER):
    os.makedirs(IMG_FOLDER)

# === 6+ REAL USER AGENTS ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

def save_screenshot(driver, step_name):
    """Screenshot save karne ka function"""
    path = f"{IMG_FOLDER}/{step_name}_{int(time.time())}.png"
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

def simulate_human_scroll(driver):
    """Asli insaan ki tarah upar-niche scroll karne ka logic"""
    print("👤 Human-like scrolling up and down...")
    for _ in range(random.randint(2, 4)):
        # Niche scroll karo
        scroll_down = random.randint(400, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_down});")
        time.sleep(random.uniform(0.5, 1.5))
        
        # Thoda wapas upar aao (Hesitation simulation)
        scroll_up = random.randint(100, 300)
        driver.execute_script(f"window.scrollBy(0, -{scroll_up});")
        time.sleep(random.uniform(0.5, 1.5))

def run_automation():
    # Randomly ek User-Agent select karo
    selected_ua = random.choice(USER_AGENTS)
    print(f"🕵️ Selected User-Agent: {selected_ua}")

    # Initialize SeleniumBase Driver with UC Mode
    driver = Driver(uc=True, agent=selected_ua, headless=True)

    try:
        print("🌐 Opening website with SeleniumBase Driver (UC Mode)...")
        driver.get("https://welib.st")
        save_screenshot(driver, "step1_homepage_loaded")
        
        # Step 2: 10 Second Wait + Human Scroll for Cloudflare Bypass
        print("⏳ 10 second wait for Cloudflare verification...")
        time.sleep(10)
        simulate_human_scroll(driver)
        save_screenshot(driver, "step2_after_wait_and_scroll")

        # Wait for redirect to complete (checking if book links appear)
        print("🔄 Waiting for redirect and books to load (Max 30s)...")
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/book/']"))
            )
            print("✅ REDIRECT SUCCESS! Books found.")
        except:
            print("⚠️ Timeout! Could not find books, proceeding anyway just in case...")
            save_screenshot(driver, "error_timeout_waiting_for_books")
        
        simulate_human_scroll(driver)
        save_screenshot(driver, "step3_books_loaded")

        # Step 3: Random Book Selection
        print("📚 Searching for a random book...")
        book_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/book/']")
        
        if book_elements:
            target_book = random.choice(book_elements)
            book_url = target_book.get_attribute("href")
            print(f"🔗 Selected Book: {book_url}")
            
            driver.get(book_url)
            time.sleep(5)
            simulate_human_scroll(driver)
            save_screenshot(driver, "step4_book_page")

            # Step 4: Download PDF
            try:
                # Wait for the download link ending in .pdf
                download_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href$='.pdf']"))
                )
                pdf_url = download_btn.get_attribute("href")
                file_path = "book.pdf"
                
                print(f"⬇️ Downloading PDF from: {pdf_url}")
                # Use requests with the same selected User-Agent
                r = requests.get(pdf_url, headers={"User-Agent": selected_ua})
                with open(file_path, "wb") as f:
                    f.write(r.content)
                
                # Send to Telegram
                send_to_telegram(file_path)
                save_screenshot(driver, "step5_success")
            except Exception as e:
                print(f"❌ PDF download link not found. Error: {e}")
                save_screenshot(driver, "error_no_pdf_link")
        else:
            print("❌ No books found on the page.")

    except Exception as e:
        print(f"⚠️ Major Error occurred: {e}")
        save_screenshot(driver, "error_final_exception")
    
    finally:
        # Browser ko properly close karna zaroori hai
        print("🧹 Closing browser...")
        driver.quit()

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as doc:
            response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": doc})
        if response.status_code == 200:
            print("🚀 Successfully sent to Telegram!")
        else:
            print(f"❌ Telegram API Error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram Request Failed: {e}")

if __name__ == "__main__":
    run_automation()
