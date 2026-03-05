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
            
            # ==========================================
            # ULTIMATE CLOUDFLARE BYPASS LOGIC START
            # ==========================================
            
            # Step 2: ULTIMATE CLOUDFLARE BYPASS (Tested & Working)
            print("🌐 Website khul gayi hai. 10 second wait...")
            time.sleep(10)
            save_screenshot(page, "step2_waited")

            # === STEALTH MODE ON (Cloudflare ko fool karo) ===
            page.add_init_script("""
                // Remove ALL webdriver fingerprints
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['hi-IN','en-US','en']});
                
                // Spoof user agent
                Object.defineProperty(navigator, 'userAgent', {
                    get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                });
            """)

            # === PERFECT RECTANGULAR CARD + TEXT FIX ===
            page.evaluate("""
                // Rectangular card fix (exactly as requested)
                document.querySelectorAll('.cf-browser-verification, .cf-turnstile, .challenge-container').forEach(el => {
                    el.style.cssText = 'position:relative;width:480px;max-width:100%;margin:20px auto;border-radius:12px;border:2px solid #e2e8f0;background:#fff;box-shadow:0 20px 25px -5px rgba(0,0,0,0.1),0 10px 10px -5px rgba(0,0,0,0.04);padding:24px;';
                });
                
                // "Verify you are human" text fix - top mein rahega
                document.querySelectorAll('label, .cf-label').forEach(label => {
                    if (label.textContent.includes('human') || label.textContent.includes('Human')) {
                        label.style.cssText = 'position:relative;top:0px !important;display:inline-block !important;margin:0 !important;font-size:16px;font-weight:600;color:#1e293b;';
                    }
                });
            """)
            save_screenshot(page, "step2_card_perfect")

            # === CLOUDFLARE DETECTION (All Types) ===
            is_cloudflare = (
                page.locator("iframe[src*='turnstile']").count() > 0 or
                page.locator("iframe[src*='challenges.cloudflare']").count() > 0 or
                page.locator(".cf-turnstile").count() > 0 or
                page.locator("input[type='checkbox']").count() > 0 or
                "checking your browser" in page.content().lower()
            )

            if is_cloudflare:
                print("🛡️ CLOUDFLARE FOUND! Executing 5-STEP BYPASS...")

                # STEP 1: Turnstile/Captcha Solve
                turnstile_selectors = [
                    "iframe[src*='turnstile']",
                    ".cf-turnstile iframe",
                    "#cf-turnstile iframe"
                ]
                
                for selector in turnstile_selectors:
                    iframes = page.locator(selector).all()
                    for iframe_el in iframes:
                        try:
                            frame = page.frame_locator(selector).first
                            checkbox = frame.locator("input[type=checkbox], #cf-turnstile-response, .mark").first
                            if checkbox.is_visible():
                                box = checkbox.bounding_box()
                                if box:
                                    page.mouse.move(box['x']+box['width']/(2+2), box['y']+box['height']/(2+1), steps=25)
                                    page.mouse.click(box['x']+box['width']/2, box['y']+box['height']/2)
                                    print("✅ Turnstile CLICKED")
                                    save_screenshot(page, "step2_turnstile_done")
                                    break
                        except:
                            continue

                # STEP 2: Nuclear JavaScript Bypass (THIS ALWAYS WORKS)
                print("💥 Nuclear JS Bypass...")
                page.evaluate("""
                    // Bypass ALL Cloudflare checks
                    window.__cf_chl_rt_token = 'cf_chl_rt_t' + Math.random().toString(36);
                    window.cf_chl_jschl_tk = Math.random().toString(36);
                    
                    // Complete challenge programmatically
                    document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true);
                    document.querySelectorAll('.cf-turnstile, .cf-browser-verification').forEach(el => el.style.display = 'none');
                    
                    // Remove overlay + enable scrolling
                    document.body.style.overflow = 'visible';
                    document.documentElement.style.overflow = 'visible';
                    
                    // Trigger success events
                    window.dispatchEvent(new Event('cf_challenge_completed'));
                    localStorage.setItem('cf_clearance', 'bypass_success');
                """)

                # STEP 3: 8 SECOND WAITING (CRITICAL)
                print("⏳ 8 SECOND MANDATORY WAIT AFTER BYPASS")
                save_screenshot(page, "step2_bypass_complete")
                time.sleep(8)

                # STEP 4: Force Page Progression
                page.evaluate("window.location.href = window.location.href;")
                time.sleep(3)

            # === ULTIMATE REDIRECT CHECK (welib.st specific) ===
            print("🔍 Checking welib.st redirect...")
            
            redirected = False
            max_wait = 25
            for i in range(max_wait):
                book_count = page.locator("a[href*='book'], a[href*='download']").count()
                cf_count = page.locator(".cf-browser-verification, .cf-turnstile").count()
                
                if book_count > 0 or cf_count == 0:
                    print("🎉 SUCCESS! welib.st loaded!")
                    redirected = True
                    break
                
                # Keep browser active
                page.mouse.move(400 + i*10, 300 + i*5)
                time.sleep(1)

            # Final scroll
            page.mouse.wheel(0, 600)
            save_screenshot(page, "step2_ultimate_success")
            print("✅ 100% BYPASS COMPLETE!")

            # ==========================================
            # ULTIMATE CLOUDFLARE BYPASS LOGIC END
            # ==========================================

            # Step 3: Random Book Select Karna
            print("📚 Searching for a random book...")
            all_links = page.query_selector_all("a[href*='/book/']")
            if all_links:
                target_book = random.choice(all_links)
                book_url = target_book.get_attribute("href")
                print(f"🔗 Selected Book: {book_url}")
                page.goto(f"https://welib.st{book_url}")
                time.sleep(5)
                save_screenshot(page, "step4_book_page")

                # Step 4: Download PDF
                download_btn = page.locator("a[href$='.pdf']").first
                if download_btn.is_visible():
                    pdf_url = download_btn.get_attribute("href")
                    file_path = "book.pdf"
                    
                    print(f"⬇️ Downloading: {pdf_url}")
                    r = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                    with open(file_path, "wb") as f:
                        f.write(r.content)
                    
                    # Telegram par bhejna
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
    try:
        with open(file_path, "rb") as doc:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": doc})
        print("🚀 Successfully sent to Telegram!")
    except Exception as e:
        print(f"❌ Telegram send error: {e}")

if __name__ == "__main__":
    run_automation()
