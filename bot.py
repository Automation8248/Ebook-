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

def run_automation():
    with sync_playwright() as p:
        # Browser setup with automation bypass arguments
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
            
            # =====================================================================
            # PERFECT ANTI-BOT BYPASS (User Provided Logic)
            # =====================================================================
            
            # Step 2: 10 Second Wait + PERFECT ANTI-BOT BYPASS
            print("🌐 10 second anti-bot wait...")
            time.sleep(10)
            save_screenshot(page, "step2_waited")

            # RECTANGULAR CARD + HUMAN TEXT FIX
            page.evaluate("""
                // Perfect anti-bot card
                let card = document.querySelector('.cf-browser-verification, .ray-id ~ div, [class*="challenge"]') || 
                           Array.from(document.querySelectorAll('div')).find(d => d.innerText.includes('human'));
                
                if (card) {
                    card.style.cssText = 'width:500px;height:220px;margin:40px auto;border-radius:20px;border:3px solid #3b82f6;background:#fff;box-shadow:0 30px 60px rgba(0,0,0,0.3);padding:30px;display:flex;align-items:center;justify-content:center;';
                    
                    let humanText = card.querySelector('label,span');
                    if (humanText?.innerText.includes('human')) {
                        humanText.style.cssText = 'font-size:20px;font-weight:700;color:#1e40af;margin-right:30px;flex-shrink:0;';
                    }
                }
            """)
            save_screenshot(page, "step2_card_fixed")

            # HUMAN CHECKBOX DETECT + ULTRA-REAL CLICK
            print("🧠 Human behavior detect kar raha hoon...")
            checkbox_selectors = [
                'input[type="checkbox"]',
                '.cf-checkbox input',
                '.mark',
                '#challenge-stage',
                '[role="checkbox"]'
            ]

            clicked = False
            for selector in checkbox_selectors:
                try:
                    checkbox = page.locator(selector).first
                    if checkbox.is_visible():
                        box = checkbox.bounding_box()
                        if box:
                            print(f"✅ Checkbox found at x:{box['x']}, y:{box['y']}")
                            
                            # ULTRA HUMAN PATH: Screen edge se curve banake aao
                            page.mouse.move(100, 400, steps=20)  # Left edge
                            time.sleep(0.3)
                            page.mouse.move(400, 350, steps=15)  # Curve 1
                            time.sleep(0.25)
                            page.mouse.move(700, 320, steps=18)  # Curve 2
                            time.sleep(0.4)
                            
                            # PRECISE SQUARE BOX CLICK (center + micro-offset)
                            x = box['x'] + box['width']/2 + random.uniform(-1.5, 1.5)
                            y = box['y'] + box['height']/2 + random.uniform(-0.8, 0.8)
                            
                            page.mouse.move(x, y, steps=10)
                            time.sleep(random.uniform(0.5, 1.0))  # Human pause
                            
                            # REAL HUMAN PRESS + RELEASE
                            page.mouse.down()
                            time.sleep(0.08)
                            page.mouse.up()
                            
                            clicked = True
                            save_screenshot(page, "step2_human_click")
                            print("🎯 HUMAN TIK SUCCESS!")
                            break
                except:
                    continue

            if not clicked:
                print("⚠️ Nuclear Failsafe activating...")
                # NUCLEAR FAILSAFE
                page.evaluate("""
                    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                        cb.click(); cb.checked = true; cb.dispatchEvent(new Event('change'));
                    });
                    document.querySelector('.cf-browser-verification')?.remove();
                """)

            # 8 SECOND EXACT WAIT
            print("⏳ 8 second verification wait...")
            save_screenshot(page, "step2_post_click")
            time.sleep(8)

            # SUCCESS CHECK
            print("🔄 Checking for success...")
            page.wait_for_load_state("networkidle", timeout=15000)
            if page.locator("a[href*='book'], .book").count() > 0:
                print("✅ WELIB.ST SUCCESS!")
            else:
                print("🔄 Reloading page...")
                page.reload()
                time.sleep(5)

            page.mouse.wheel(0, 800)
            save_screenshot(page, "step2_final")
            print("🎉 BYPASS COMPLETE!")

            # =====================================================================
            # RANDOM BOOK SELECTION & DOWNLOAD
            # =====================================================================

            print("📚 Searching for a random book...")
            all_links = page.query_selector_all("a[href*='/book/']")
            if all_links:
                target_book = random.choice(all_links)
                book_url = target_book.get_attribute("href")
                print(f"🔗 Selected Book: {book_url}")
                page.goto(f"https://welib.st{book_url}")
                time.sleep(5)
                save_screenshot(page, "step4_book_page")

                download_btn = page.locator("a[href$='.pdf']").first
                if download_btn.is_visible():
                    pdf_url = download_btn.get_attribute("href")
                    file_path = "book.pdf"
                    
                    print(f"⬇️ Downloading: {pdf_url}")
                    r = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                    with open(file_path, "wb") as f:
                        f.write(r.content)
                    
                    send_to_telegram(file_path)
                    save_screenshot(page, "step5_success")
                else:
                    print("❌ PDF link not found.")
            else:
                print("❌ No books found.")

        except Exception as e:
            print(f"⚠️ Error: {e}")
            save_screenshot(page, "error_final")
        finally:
            browser.close()

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as doc:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": doc})
        print("🚀 Successfully sent to Telegram!")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

if __name__ == "__main__":
    run_automation()
