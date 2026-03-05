import os
import time
import random
import requests
from playwright.sync_api import sync_playwright

# Config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
IMG_FOLDER = "images"

if not os.path.exists(IMG_FOLDER):
    os.makedirs(IMG_FOLDER)

def save_screenshot(page, name):
    path = f"{IMG_FOLDER}/{name}_{int(time.time())}.png"
    page.screenshot(path=path)
    print(f"Screenshot saved: {path}")

def run_automation():
    with sync_playwright() as p:
        # Browser launch (Headless for GitHub Actions)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()

        try:
            # 1. Website par jana
            print("Opening website...")
            page.goto("https://welib.st", wait_until="networkidle")
            save_screenshot(page, "step1_homepage")

            # 2. Cloudflare Checkbox Handling
            # Note: Playwright automatically wait karta hai, lekin Cloudflare ke liye thoda extra time
            time.sleep(5) 
            if "Verify you are human" in page.content():
                print("Cloudflare detected, attempting to click...")
                # Try to click the checkbox if visible
                checkbox = page.frame_locator("iframe").locator("input[type='checkbox']")
                if checkbox.is_visible():
                    checkbox.click()
                    time.sleep(5)
                    save_screenshot(page, "step2_after_captcha")

            # 3. Random Book Select Karna
            links = page.locator("a[href*='/book/']").all_inner_texts()
            all_links = page.query_selector_all("a[href*='/book/']")
            if all_links:
                target_book = random.choice(all_links)
                book_url = target_book.get_attribute("href")
                page.goto(f"https://welib.st{book_url}")
                print(f"Book page opened: {book_url}")
                save_screenshot(page, "step3_book_page")
            else:
                print("No books found.")
                return

            # 4. Download Logic
            # Yahan hum direct PDF link search karenge
            download_btn = page.locator("a[href$='.pdf']").first
            if download_btn.is_visible():
                pdf_url = download_btn.get_attribute("href")
                file_path = "book.pdf"
                
                # Download file
                response = requests.get(pdf_url)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                
                print("Book downloaded. Sending to Telegram...")
                
                # 5. Telegram Pe Bhejna
                send_to_telegram(file_path)
            else:
                print("Download link not found.")

        except Exception as e:
            print(f"Error occurred: {e}")
            save_screenshot(page, "error_state")
        finally:
            browser.close()

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(file_path, "rb") as doc:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"document": doc})
    print("Sent successfully!")

if __name__ == "__main__":
    run_automation()
