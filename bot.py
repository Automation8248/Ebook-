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
    path = f"{IMG_FOLDER}/{step_name}_{int(time.time())}.png"
    page.screenshot(path=path)
    print(f"📸 Screenshot saved: {path}")

def simulate_human_mouse(page):
    for _ in range(3):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        page.mouse.move(x, y, steps=10)
        time.sleep(random.uniform(0.5, 1.5))

def run_automation():
    with sync_playwright() as p:
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
            
            # Step 2: 10 Second Wait aur Cloudflare handling
            print("🌐 Website khul gayi hai. 10 second wait kar raha hoon...")
            time.sleep(10)
            save_screenshot(page, "step2_after_10s_wait")

            if page.locator("iframe").count() > 0:
                print("🛡️ Cloudflare challenge detected.")
                iframe = page.frame_locator("iframe").first
                checkbox = iframe.locator("input[type='checkbox'], .mark, #challenge-stage")
                
                if checkbox.is_visible():
                    print("🎯 Target acquired. Moving mouse to the checkbox...")
                    box = checkbox.bounding_box()
                    if box:
                        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=15)
                        time.sleep(1)
                        print("🖱️ Clicking the checkbox...")
                        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        save_screenshot(page, "step2_clicked_captcha")
                
                # Redirect hone tak wait karna (max 30s)
                print("⏳ Waiting for redirection...")
                for _ in range(30):
                    if page.locator("a[href*='/book/']").count() > 0:
                        print("✅ Successfully redirected!")
                        break
                    page.mouse.move(random.randint(200,800), random.randint(200,600), steps=5)
                    time.sleep(1)
            
            # Step 3: Scroll aur Random Book Select Karna
            print("📜 Scrolling down and searching for a book...")
            page.mouse.wheel(0, random.randint(600, 1000))
            save_screenshot(page, "step3_scrolled")
            
            all_links = page.query_selector_all("a[href*='/book/']")
            if all_links:
                target_book = random.choice(all_links)
                book_url = target_book.get_attribute("href")
                print(f"🔗 Selected: {book_url}")
                page.goto(f"https://welib.st{book_url}")
                time.sleep(5)
                save_screenshot(page, "step4_book_page")

                # Step 4: Download PDF
                download_btn = page.locator("a[href$='.pdf']").first
                if download_btn.is_visible():
                    pdf_url = download_btn.get_attribute("href")
                    file_path = "book.pdf"
                    r = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                    with open(file_path, "wb") as f:
                        f.write(r.content)
                    
                    send_to_telegram(file_path)
                    save_screenshot(page, "step5_success")
                else:
                    print("❌ Download link not found.")
            else:
                print("❌ No books found.")

        except Exception as e:
            print(f"⚠️ Error: {e}")
            save_screenshot(page, "error_final")
        finally:
            browser.close()

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(file_path, "rb") as doc:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"document": doc})
    print("🚀 Sent to Telegram!")

if __name__ == "__main__":
    run_automation()
