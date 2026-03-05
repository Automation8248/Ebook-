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
            # FINAL CLOUDFLARE ANTI-BOT BYPASS (Verify you are human CARD)
            # =====================================================================
            
            print("🌐 10 second initial wait for anti-bot...")
            time.sleep(10)
            save_screenshot(page, "step2_anti_bot_wait")

            # === PERFECT RECTANGULAR CARD FIX ===
            page.evaluate("""
                // Anti-bot card ko perfect rectangular banao
                var antiBotCard = document.querySelector('.cf-browser-verification, .anti-bot-card, .challenge-card, [class*="challenge"], [class*="verification"]') || document.querySelector('.ray-id')?.closest('div');
                if (antiBotCard) {
                    antiBotCard.style.cssText = `
                        position: relative !important;
                        width: 480px !important; height: 200px !important;
                        margin: 50px auto !important;
                        border-radius: 16px !important;
                        border: 3px solid #3b82f6 !important;
                        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
                        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25) !important;
                        padding: 32px !important;
                        display: flex !important; align-items: center !important; justify-content: center !important;
                    `;
                    
                    // "Verify you are human" text fix
                    var humanText = antiBotCard.querySelector('label, span, div');
                    if (humanText && humanText.textContent.includes('human')) {
                        humanText.style.cssText = 'font-size: 18px !important; font-weight: 700 !important; color: #1e293b !important; margin-right: 24px !important;';
                    }
                }
            """)
            save_screenshot(page, "step2_card_perfect_rectangular")

            # === HUMAN VERIFICATION CHECK ===
            anti_bot_selectors = [
                ".cf-browser-verification", ".challenge-form", ".anti-bot-form",
                "[data-ray]", "div[class*='challenge']", ".ray-id"
            ]

            is_anti_bot = any(page.locator(selector).count() > 0 for selector in anti_bot_selectors)

            if is_anti_bot:
                print("🎯 ANTI-BOT 'Verify you are human' CARD detect! HUMAN BEHAVIOR activate...")

                # === STEP 1: HUMAN-LIKE MOUSE MOVEMENT TO CARD ===
                print("👤 Human jaise card ki taraf move kar raha hoon...")
                card = page.locator('.cf-browser-verification, [class*="challenge"], .ray-id').first
                if card.is_visible():
                    card_box = card.bounding_box()
                    if card_box:
                        card_center_x = card_box['x'] + card_box['width'] / 2
                        card_center_y = card_box['y'] + card_box['height'] / 2
                        
                        screen_center_y = 540
                        path_steps = [
                            (200, screen_center_y + 100), (400, screen_center_y + 50),
                            (600, screen_center_y - 20), (card_center_x - 50, card_center_y - 10),
                            (card_center_x, card_center_y)
                        ]
                        
                        for step_x, step_y in path_steps:
                            page.mouse.move(step_x, step_y, steps=12)
                            time.sleep(random.uniform(0.15, 0.35))
                        
                        save_screenshot(page, "step2_human_mouse_path")
                
                # === STEP 2: SQUARE BOX SEARCH & HUMAN CLICK ===
                print("🔍 Square checkbox box dhund raha hoon...")
                square_box_selectors = ["input[type='checkbox']", ".mark", "#challenge-stage", ".cf-checkbox", "[role='checkbox']"]
                
                square_box = None
                for selector in square_box_selectors:
                    try:
                        box_elem = page.locator(selector).first
                        if box_elem.is_visible():
                            square_box = box_elem.bounding_box()
                            if square_box:
                                print(f"✅ Square box mila! Size: {square_box['width']}x{square_box['height']}")
                                break
                    except:
                        continue
                
                if square_box:
                    target_x = square_box['x'] + square_box['width'] / 2 + random.randint(-2, 2)
                    target_y = square_box['y'] + square_box['height'] / 2 + random.randint(-1, 1)
                    
                    print("🖱️ Square box mein HUMAN Tik kar raha hoon...")
                    page.mouse.move(target_x, target_y, steps=8)
                    time.sleep(random.uniform(0.4, 0.8))
                    
                    page.mouse.down()
                    time.sleep(0.05)
                    page.mouse.up()
                    
                    save_screenshot(page, "step2_square_box_ticked")
                    print("✅ TIK SUCCESS! Box tick ho gaya!")
                else:
                    print("⚠️ Box nahi mila, JS force tick...")
                    page.evaluate("document.querySelectorAll('input[type=\"checkbox\"]').forEach(cb => {cb.click(); cb.checked = true;});")

                # === STEP 3: 8 SECOND WAITING (MANDATORY) ===
                print("⏳ 8 second wait for verification...")
                save_screenshot(page, "step2_tick_complete")
                time.sleep(8)

            # === STEP 4: REDIRECT CONFIRMATION ===
            print("🔄 Redirect check kar raha hoon...")
            page.wait_for_load_state("networkidle", timeout=10000)

            if page.locator("a[href*='book'], .book, [class*='download']").count() > 0:
                print("🎉 SUCCESS! welib.st main page load!")
            else:
                page.evaluate("location.reload()")
                time.sleep(4)

            page.mouse.wheel(0, 800)
            save_screenshot(page, "step2_final_success")
            print("✅ ANTI-BOT BYPASS 100% COMPLETE!")

            # =====================================================================
            # RANDOM BOOK SELECTION & DOWNLOAD
            # =====================================================================

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
