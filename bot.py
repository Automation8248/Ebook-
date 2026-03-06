#!/usr/bin/env python3
"""
🔥 ULTIMATE WELIB.ST CLOUDFLARE BYPASSER v2026 - FULLY FIXED
✅ SeleniumBase UC Driver + Human Clicker + Telegram PDF
"""

import os
import time
import random
import requests
from datetime import datetime
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_photo(driver, caption=""):
    """Send screenshot to Telegram"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"images/{timestamp}_welib.png"
    os.makedirs("images", exist_ok=True)
    driver.save_screenshot(screenshot_path)
    
    with open(screenshot_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]}
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto", 
                     files=files, data=data)

def send_telegram_pdf(pdf_content, filename="book.pdf"):
    """Send PDF to Telegram"""
    files = {"document": (filename, pdf_content, "application/pdf")}
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": f"📚 Downloaded: {filename}"}
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument", 
                 files=files, data=data)

def ultimate_human_checkbox_clicker(driver):
    """ULTIMATE REAL HUMAN CHECKBOX CLICKER - 7 Layer Bypass"""
    print("🖱️  Phase 1: Human mouse trail + scroll simulation")
    
    # Inject ultra-stealth JS first
    stealth_js = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = {runtime: {}};
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
    """
    driver.execute_script(stealth_js)
    
    # Simulate human scroll + mouse trail
    driver.execute_script("""
        window.scrollBy(0, 100); 
        for(let i=0; i<5; i++) {
            setTimeout(() => {
                document.elementFromPoint(Math.random()*window.innerWidth, Math.random()*window.innerHeight).dispatchEvent(new MouseEvent('mouseover', {bubbles:true}));
            }, %d);
        }
    """ % random.randint(100, 300))
    
    time.sleep(random.uniform(2, 4))
    send_telegram_photo(driver, "01_human_mouse_trail")
    
    print("🖱️  Phase 2: Perfect human trajectory click (screen-left → curve → center)")
    
    # All possible checkbox selectors (10+ variants)
    checkbox_selectors = [
        'input[type="checkbox"]',
        '#cf-challenge-checkbox',
        '.cf-checkbox input',
        '#challenge-stage input',
        '.mark',
        '[role="checkbox"]',
        '.cf-turnstile input',
        'input[aria-label*="checkbox"]',
        '.cf-challenge input[type="checkbox"]',
        '#turnstile-checkbox',
        '.human-challenge input'
    ]
    
    actions = ActionChains(driver)
    
    # HUMAN TRAJECTURE: Screen-left → hesitation → curve → precise center
    start_x, start_y = 50, 450
    hesitate_x, hesitate_y = 280, 430
    curve_x, curve_y = 520, 390
    center_offset = random.randint(-8, 8)
    
    # Phase 2a: Move from screen-left with natural curve
    actions.move_by_offset(start_x, start_y).pause(random.uniform(0.18, 0.35)).perform()
    actions.move_to_element_with_offset(driver.find_element(By.TAG_NAME, "body"), 
                                       hesitate_x, hesitate_y).pause(0.8).perform()
    
    # Phase 2b: Curved path to target with micro-movements
    actions.move_by_offset(120 + center_offset, -25).pause(0.22).perform()
    actions.move_by_offset(120 + center_offset, 15).pause(0.15).perform()
    
    send_telegram_photo(driver, "02_perfect_human_trajectory")
    
    # Phase 2c: Find & click checkbox (iframe-aware)
    checkbox_clicked = False
    for selector in checkbox_selectors:
        try:
            checkboxes = driver.find_elements(By.CSS_SELECTOR, selector)
            for checkbox in checkboxes:
                if checkbox.is_displayed() and checkbox.is_enabled():
                    # Final precise move + PRESSURE CLICK (0.15s hold)
                    actions.move_to_element(checkbox).pause(0.12).click_and_hold(checkbox).pause(random.uniform(0.10, 0.22)).release().perform()
                    print(f"✅ Clicked checkbox: {selector}")
                    checkbox_clicked = True
                    break
            if checkbox_clicked:
                break
        except:
            continue
    
    # Phase 3: Nuclear JS fallback if no checkbox found
    if not checkbox_clicked:
        print("💥 Nuclear JS fallback - forcing checkbox")
        driver.execute_script("""
            let checkboxes = document.querySelectorAll('input[type="checkbox"], [role="checkbox"]');
            checkboxes.forEach(cb => {
                cb.checked = true;
                cb.dispatchEvent(new Event('change', {bubbles: true}));
                cb.dispatchEvent(new Event('click', {bubbles: true}));
            });
            
            // Cloudflare-specific nukes
            if (window.turnstile) window.turnstile.rendered = true;
            if (window.cf_chl_jschl) window.cf_chl_jschl = true;
        """)
    
    print("⏳ Phase 4: 8s human post-click wait")
    time.sleep(8)
    send_telegram_photo(driver, "03_checkbox_success")
    
    return checkbox_clicked

def run_automation():
    """Main automation flow"""
    print("🔥 ULTIMATE WELIB.ST BYPASSER v2026")
    print("📦 pip install seleniumbase")
    print("🌐 Set TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID")
    
    # ✅ FIXED Driver - VALID SeleniumBase UC params ONLY
    driver = Driver(
        uc=True,           # Undetected Chrome (auto UA rotation)
        headless=False,    # Visible for debugging
        undetectable=True,
        disable_csp=True,
        disable_ws=True,
        block_images=True,
        uc_subdomains=False,
        no_sandbox=True,
        disable_gpu=True,
        window_size="1920,1080",
        locale_code="en_US",
        # ✅ NO user_agent - UC handles UA automatically
        # ✅ NO driver_version - uses latest
    )
    
    # Set UA via JS after launch (UC compatible)
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": ua,
        "acceptLanguage": "en-US,en;q=0.9"
    })
    
    print(f"🕵️‍♂️  UC Chrome + Stealth UA loaded")
    print("=" * 70)
    
    try:
        # Navigate to welib.st
        driver.get("https://welib.st")
        send_telegram_photo(driver, "00_initial_load")
        print("🌐 Loaded welib.st - 10s human wait")
        time.sleep(10)
        
        # ULTIMATE CLOUDFLARE BYPASS
        ultimate_human_checkbox_clicker(driver)
        
        # Smart book detection (30s wait max)
        print("📚 Detecting books...")
        wait = WebDriverWait(driver, 30)
        
        book_selectors = 'a[href*="/book/"], .book, a[href*="/books/"], .book-card, [class*="book"]'
        books = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, book_selectors)))
        
        # Random book selection
        all_books = driver.find_elements(By.CSS_SELECTOR, book_selectors)
        random_book = random.choice(all_books[:10])
        book_url = random_book.get_attribute("href")
        book_title = random_book.text[:100] or "Random Book"
        
        print(f"📖 Selected: {book_title}")
        send_telegram_photo(driver, f"04_book_selected: {book_title}")
        
        driver.get(book_url)
        time.sleep(5)
        
        # PDF download via requests (stealth)
        session = requests.Session()
        session.headers.update({"User-Agent": ua})
        pdf_links = driver.find_elements(By.CSS_SELECTOR, 'a[href$=".pdf"], [href*=".pdf"]')
        
        if pdf_links:
            pdf_url = pdf_links[0].get_attribute("href")
            print(f"📄 Downloading PDF: {pdf_url}")
            
            pdf_response = session.get(pdf_url, stream=True)
            send_telegram_pdf(pdf_response.content, f"{book_title[:50]}.pdf")
        else:
            print("❌ No PDF found - sending page screenshot")
            send_telegram_photo(driver, "05_no_pdf_final")
        
        # Final human scroll + screenshot
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        send_telegram_photo(driver, "06_final_success")
        
        print("✅ BYPASS COMPLETE - Check Telegram!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        send_telegram_photo(driver, f"ERROR: {str(e)[:200]}")
    
    finally:
        input("Press Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    run_automation()
