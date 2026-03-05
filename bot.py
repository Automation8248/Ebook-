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
    """Mouse ko screen par upar-neeche randomly move karna"""
    for _ in range(3):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        page.mouse.move(x, y, steps=10)
        random_delay(0.5, 1.5)

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
            random_delay()

            # --- Updated Section with Cloudflare Bypass + Fixes ---

# Step 2: Website par pahunchne ke baad wait aur click (Cloudflare Bypass)
print("🌐 Website khul gayi hai. 10 second wait kar raha hoon...")
time.sleep(10) # 10 second ka fixed wait for free direct detection

save_screenshot(page, "step2_after_10s_wait")

# Cloudflare rectangular card fix + text positioning
page.add_style_tag("""
    .cf-browser-verification, .challenge-form, .cf-challenge-form {
        position: relative !important;
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        background: white !important;
    }
    .cf-browser-verification label, .challenge-form label {
        position: relative !important;
        top: 0 !important;
        display: inline-block !important;
        margin-top: 0 !important;
    }
    #challenge-stage, .ray-id {
        position: relative !important;
        z-index: 999 !important;
    }
""")

if page.locator("iframe").count() > 0 or page.locator("input[type='checkbox']").count() > 0:
    print("🛡️ Cloudflare challenge mila. Bypass kar raha hoon...")
    
    # Multiple checkbox selectors for Cloudflare
    checkbox_selectors = [
        "iframe input[type='checkbox']",
        "iframe .mark",
        "iframe #challenge-stage",
        "input[type='checkbox']",
        ".cf-browser-verification input[type='checkbox']",
        "#cf-challenge-running input[type='checkbox']"
    ]
    
    checkbox_clicked = False
    for selector in checkbox_selectors:
        try:
            if "iframe" in selector:
                iframe = page.frame_locator("iframe").first
                checkbox = iframe.locator(selector.replace("iframe ", ""))
            else:
                checkbox = page.locator(selector)
            
            if checkbox.is_visible():
                box = checkbox.bounding_box()
                if box:
                    # Human-like smooth mouse movement
                    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=15)
                    time.sleep(random.uniform(0.5, 1.2))  # Human delay
                    
                    # Precise click
                    print("🖱️ Checkbox par human-like click kar raha hoon...")
                    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    save_screenshot(page, "step2_checkbox_clicked")
                    checkbox_clicked = True
                    break
        except Exception as e:
            continue
    
    if not checkbox_clicked:
        print("⚠️ Checkbox manually nahi mila, JavaScript bypass try kar raha hoon...")
        page.evaluate("""
            // Force checkbox check via JS
            var checkboxes = document.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => cb.checked = true);
            
            // Trigger challenge completion
            var challengeForm = document.querySelector('.cf-browser-verification, .challenge-form');
            if (challengeForm) {
                challengeForm.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            
            // Simulate human completion
            window.cfChallengeComplete = true;
        """)

# Screenshot ke baad 8 second wait (exactly jaise manga tha)
print("📸 Challenge screenshot lene ke baad 8 second wait...")
save_screenshot(page, "step2_cloudflare_bypassed")
time.sleep(8)  # 8 second fixed wait after screenshot

# Advanced redirect wait with multiple checks
print("⏳ Redirect + final bypass wait (welib.st specific)...")
page.wait_for_load_state("networkidle", timeout=15000)

# welib.st specific selectors for successful redirect
success_selectors = [
    "a[href*='/book/']",
    ".book-item, .book-card",
    "[class*='book']",
    ".content-main",
    "body:not(.cf-browser-verification)"
]

redirect_success = False
for selector in success_selectors:
    try:
        page.wait_for_selector(selector, timeout=10000)
        print(f"✅ Redirect successful! ({selector} mila)")
        redirect_success = True
        break
    except:
        continue

if not redirect_success:
    print("🔄 Extra bypass measures...")
    page.evaluate("""
        // welib.st specific Cloudflare bypass
        if (location.hostname === 'welib.st') {
            document.querySelector('.cf-browser-verification')?.remove();
            document.body.classList.remove('cf-browser-verification');
            window.location.reload();
        }
    """)
    time.sleep(3)

print("✅ Cloudflare bypass complete! Niche scroll kar raha hoon...")
page.mouse.wheel(0, 800) # Smooth scroll down
save_screenshot(page, "step3_final_redirected_scrolled")

            # NAYA LOGIC: Redirect hone ke baad niche scroll karna
            print("📜 Scrolling down the page after redirect...")
            page.mouse.wheel(0, random.randint(600, 1500)) # Random amount scroll karega
            simulate_human_mouse(page) # Thoda mouse hilayega
            random_delay(2, 4)
            save_screenshot(page, "step4_scrolled_down")

            # Step 3: Find Random Book
            print("📚 Searching for a random book...")
            all_links = page.query_selector_all("a[href*='/book/']")
            
            if not all_links:
                print("❌ No books found.")
                save_screenshot(page, "error_no_books")
                return

            target_book = random.choice(all_links)
            book_url = target_book.get_attribute("href")
            
            print(f"🔗 Selected Book: {book_url}")
            page.goto(f"https://welib.st{book_url}")
            random_delay(2, 4)
            save_screenshot(page, "step5_book_page")

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
                save_screenshot(page, "step6_success")
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
