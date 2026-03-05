import os
import time
import random
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
IMG_FOLDER = "images"

if not os.path.exists(IMG_FOLDER):
    os.makedirs(IMG_FOLDER)

def save_screenshot(page, step_name):
    """Har step ka screenshot lene ke liye function"""
    path = f"{IMG_FOLDER}/{step_name}_{int(time.time())}.png"
    page.screenshot(path=path)
    print(f"📸 Screenshot saved: {path}")

def random_delay(min_sec=2, max_sec=5):
    """Human-like delay create karne ke liye"""
    time.sleep(random.uniform(min_sec, max_sec))

def simulate_human_mouse(page):
    """Mouse ko screen par upar-neeche randomly move karna aur scroll karna"""
    print("🤖 Simulating human behavior...")
    # Random scroll
    page.mouse.wheel(0, random.randint(200, 500))
    random_delay(1, 2)
    page.mouse.wheel(0, -random.randint(100, 300))
    
    # Random mouse movements
    for _ in range(3):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        page.mouse.move(x, y, steps=10) # steps=10 smooth movement ke liye
        random_delay(0.5, 1.5)

def run_automation():
    with sync_playwright() as p:
        # Browser setup with specific arguments to avoid bot detection
        browser = p.chromium.launch(
            headless=True, 
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()

        try:
            # Step 1: Website open karna
            print("🌐 Opening website...")
            page.goto("https://welib.st", wait_until="domcontentloaded")
            save_screenshot(page, "step1_homepage_loaded")
            random_delay()

            # Step 2: Human Behavior & Cloudflare Check
            simulate_human_mouse(page)
            
            # Check if Cloudflare iframe is present
            if page.locator("iframe").count() > 0:
                print("🛡️ Cloudflare challenge detected.")
                iframe = page.frame_locator("iframe").first
                
                # Cloudflare ke checkbox ko locate karna
                checkbox = iframe.locator("input[type='checkbox'], .mark, #challenge-stage")
                
                if checkbox.is_visible():
                    print("🎯 Target acquired. Moving mouse to the checkbox...")
                    # Get box coordinates for smooth hover
                    box = checkbox.bounding_box()
                    if box:
                        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=15)
                        random_delay(1, 2)
                        print("🖱️ Clicking the checkbox...")
                        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        save_screenshot(page, "step2_clicked_captcha")
                
                # Redirect hone ka wait karna (max 15 seconds)
                print("⏳ Waiting for redirection...")
                page.wait_for_timeout(15000) 
                save_screenshot(page, "step3_after_redirection_wait")

            # Step 3: Find Random Book
            print("📚 Searching for a random book...")
            # Wait for book links to appear
            page.wait_for_selector("a[href*='/book/']", timeout=10000)
            all_links = page.query_selector_all("a[href*='/book/']")
            
            if not all_links:
                print("❌ No books found after bypass. Might still be stuck on Cloudflare.")
                save_screenshot(page, "error_no_books")
                return

            target_book = random.choice(all_links)
            book_url = target_book.get_attribute("href")
            
            print(f"🔗 Selected Book: {book_url}")
            page.goto(f"https://welib.st{book_url}")
            random_delay(2, 4)
            save_screenshot(page, "step4_book_page")

            # Step 4: Download PDF
            download_btn = page.locator("a[href$='.pdf']").first
            if download_btn.is_visible():
                pdf_url = download_btn.get_attribute("href")
                file_path = "downloaded_book.pdf"
                
                print(f"⬇️ Downloading PDF from: {pdf_url}")
                response = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                with open(file_path, "wb") as f:
                    f.write(response.content)
                
                print("✅ Book downloaded! Sending to Telegram...")
                send_to_telegram(file_path)
                save_screenshot(page, "step5_success")
            else:
                print("❌ PDF download link not found on the page.")
                save_screenshot(page, "error_no_download_btn")

        except Exception as e:
            print(f"⚠️ Error occurred: {e}")
            save_screenshot(page, "error_exception_caught")
        finally:
            browser.close()

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(file_path, "rb") as doc:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": doc})
    if response.status_code == 200:
        print("🚀 Successfully sent to Telegram!")
    else:
        print(f"❌ Failed to send to Telegram. Error: {response.text}")

if __name__ == "__main__":
    run_automation()
