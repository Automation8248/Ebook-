import os
import time
import random
import requests
import subprocess
from datetime import datetime
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_photo(driver, caption=""):
    """Screenshot Telegram par bhejne ka function"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"images/{timestamp}_welib.png"
    os.makedirs("images", exist_ok=True)
    driver.save_screenshot(screenshot_path)
    
    try:
        with open(screenshot_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]}
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto", files=files, data=data)
    except Exception as e:
        print(f"❌ Photo Error: {e}")

def send_telegram_file(file_path, file_type="document", caption=""):
    """Telegram par PDF ya Video bhejne ka function"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram Config (Token/Chat ID) missing hai!")
        return

    print(f"📤 Telegram par {file_type} bhej raha hoon: {file_path}")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/send{file_type.capitalize()}"
    
    try:
        with open(file_path, "rb") as f:
            files = {file_type: f}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            response = requests.post(url, files=files, data=data, timeout=120)
            
        if response.status_code == 200:
            print(f"✅ {file_type.capitalize()} successfully sent to Telegram! 🎉")
        else:
            print(f"❌ {file_type.capitalize()} bhejne mein error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def active_human_mouse_wait(driver, duration=10):
    """10 Second tak mouse ko screen par idhar-udhar ghumane ka logic"""
    end_time = time.time() + duration
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        ActionChains(driver).move_to_element(body).perform()
    except:
        pass

    while time.time() < end_time:
        x_offset = random.randint(-250, 250)
        y_offset = random.randint(-250, 250)
        try:
            ActionChains(driver).move_by_offset(x_offset, y_offset).perform()
        except:
            try:
                ActionChains(driver).move_to_element(driver.find_element(By.TAG_NAME, "body")).perform()
            except:
                pass
        time.sleep(random.uniform(0.5, 1.5))

def run_automation():
    print("🚀 Automation shuru ho raha hai...")
    
    # 🎥 SCREEN RECORDING START (FFMPEG)
    display = os.environ.get('DISPLAY', ':99')
    video_filename = f"automation_record_{int(time.time())}.mp4"
    print("🎥 Screen recording start...")
    
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-f', 'x11grab', '-video_size', '1920x1080',
        '-framerate', '15', '-i', f'{display}', '-codec:v', 'libx264',
        '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', video_filename
    ]
    record_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 🕵️ DRIVER SETUP (UC Mode)
    driver = Driver(
        uc=True,
        headless=False,
        disable_csp=True,
        undetectable=True,
        window_size="1920,1080",
        no_sandbox=True
    )

    try:
        print("🌐 Website open kar raha hoon...")
        driver.get("https://welib.st")
        time.sleep(2)
        
        # STEP 2: 10 SECOND ACTIVE WAIT (Pre-Click)
        print("⏳ 10 second tak mouse idhar-udhar move kar raha hoon (Anti-Bot Bypass)...")
        active_human_mouse_wait(driver, 10)
        
        # ========================================================
        # 🔥 FINAL PERFECT VERSION - VISIBLE MOUSE CURSOR + TEXT POSITION CLICK
        # ========================================================
        print("🎯 Cloudflare Iframe Bypass - VISIBLE MOUSE CURSOR + TEXT POSITION CLICK")

        # **RED DOT CURSOR VISIBLE TRACKER**
        driver.execute_script("""
            let redDot = document.createElement('div');
            redDot.id = 'mouse-tracker';
            redDot.style.cssText = `
                position: fixed; z-index: 999999; width: 16px; height: 16px;
                background: radial-gradient(circle, #ff4444 30%, #ff0000 60%, transparent);
                border: 3px solid #ffffff; border-radius: 50%; 
                box-shadow: 0 0 15px #ff0000, inset 0 0 5px rgba(255,255,255,0.3);
                pointer-events: none; transform: translate(-50%, -50%);
                animation: pulse 0.8s infinite;
            `;
            redDot.innerHTML = '🖱️';
            document.body.appendChild(redDot);
            
            let customMouse = {x: 0, y: 0};
            document.addEventListener('mousemove', (e) => {
                customMouse.x = e.pageX;
                customMouse.y = e.pageY;
                redDot.style.left = customMouse.x + 'px';
                redDot.style.top = customMouse.y + 'px';
            });
            
            let style = document.createElement('style');
            style.textContent = `@keyframes pulse {0%,100%{opacity:1} 50%{opacity:0.7; transform:scale(1.2)}}`;
            document.head.appendChild(style);
            
            console.log('🔴🔴 RED DOT MOUSE TRACKER ACTIVATED - VISIBLE!');
        """)

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        clicked = False

        for iframe_idx, iframe in enumerate(iframes, 1):
            try:  # <-- Yahi TRY block hai jiska EXCEPT pehle chhut gaya tha
                print(f"🔍 Iframe #{iframe_idx}/{len(iframes)} check kar raha hoon...")
                driver.switch_to.frame(iframe)
                time.sleep(0.5)
                
                # **ENHANCED TEXT DETECTION**
                verify_texts = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verify') and (contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'human') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'u r') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'automation'))]")
                checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], .mark, [role="checkbox"], .cf-checkbox input, #cf-challenge-checkbox, #turnstile-checkbox')
                
                print(f"📝 Verify texts: {len(verify_texts)} | Checkboxes: {len(checkboxes)}")
                
                if verify_texts:
                    print(f"🎯 VERIFY TEXT MILA: '{verify_texts[0].text.strip()[:50]}...'")
                    target_text = verify_texts[0]
                    text_rect = target_text.rect
                    print(f"📍 Text position: X={text_rect['x']}, Y={text_rect['y']}, Width={text_rect['width']}, Height={text_rect['height']}")
                    
                    # **GREEN HIGHLIGHT**
                    driver.execute_script("""
                        let textEl = arguments[0];
                        let highlight = document.createElement('div');
                        highlight.style.cssText = `
                            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                            border: 5px solid #00ff88; border-radius: 8px;
                            box-shadow: 0 0 25px #00ff88; z-index: 99999; pointer-events: none;
                            background: linear-gradient(45deg, rgba(0,255,136,0.2), transparent);
                        `;
                        textEl.parentNode.style.position = 'relative';
                        textEl.parentNode.appendChild(highlight);
                    """, target_text)
                    
                    actions = ActionChains(driver)
                    print("🖱️ VISIBLE PATH: Left → VERIFY TEXT CENTER → TIK!")
                    
                    actions.move_by_offset(80, 420).pause(0.6).perform()
                    print("✅ Phase 1: Screen-left - RED DOT visible")
                    time.sleep(0.4)
                    
                    text_center_x = text_rect['x'] + text_rect['width']/2 + random.randint(-15, 15)
                    text_center_y = text_rect['y'] + text_rect['height']/2 + random.randint(-10, 10)
                    
                    actions.move_to_element_with_offset(target_text, text_center_x - text_rect['x'], text_center_y - text_rect['y']).pause(1.2).perform()
                    print(f"✅ Phase 2: TEXT CENTER PE! ({text_center_x:.0f},{text_center_y:.0f})")
                    time.sleep(0.8)
                    
                    actions.move_by_offset(random.randint(-8,8), random.randint(-5,5)).pause(0.4).perform()
                    print("✅ Phase 3: Micro hesitation - natural")
                    
                    print("🎯 FINAL TIK-TIK: TEXT POSITION PE DOUBLE CLICK!")
                    actions.click_and_hold(target_text).pause(0.18).release().pause(0.1).click(target_text).perform()
                    
                    print("✅✅✅ TEXT POSITION PE DOUBLE TIK DIYA! 🎉🔥")
                    clicked = True
                    
                    send_telegram_photo(driver, f"✅✅ TEXT PE TIK DIYA! Iframe #{iframe_idx} - RED DOT visible")
                    
                    time.sleep(1.5)
                    driver.switch_to.default_content()
                    break
                    
                elif checkboxes:
                    print("📦 Text nahi mila, direct checkbox pe try...")
                    target_box = checkboxes[0]
                    actions = ActionChains(driver)
                    actions.move_to_element(target_box).pause(0.5).click_and_hold(target_box).pause(0.15).release().perform()
                    clicked = True
                    
                driver.switch_to.default_content()
                
            except Exception as e: # <-- YAHAN PAR EXCEPT BLOCK LAGA DIYA HAI
                print(f"⚠️ Iframe #{iframe_idx} error: {str(e)[:80]}")
                try:
                    driver.switch_to.default_content()
                except:
                    pass
                continue

        driver.switch_to.default_content()

        # **POST-CLICK HUMAN BEHAVIOR**
        if clicked:
            print("⏳ 8s SUCCESS WAIT - Human behavior...")
            for i in range(8):
                driver.execute_script(f"window.scrollBy({random.randint(-20,20)}, {random.randint(-15,15)});")
                time.sleep(random.uniform(0.8, 1.3))

        # **CLEANUP RED DOT**
        driver.execute_script("document.getElementById('mouse-tracker')?.remove();")
        print("🎉🎉 CLOUDFLARE BYPASS 100% COMPLETE! RED DOT removed")

        if not clicked:
            print("💥 FINAL NUCLEAR - Emergency bypass")
            driver.execute_script("""
                document.querySelectorAll('*').forEach(el => {
                    if (el.textContent.toLowerCase().includes('verify') && el.textContent.toLowerCase().includes('human')) {
                        el.click();
                    }
                    if (el.tagName === 'INPUT' && el.type === 'checkbox') {
                        el.checked = true; el.click();
                    }
                });
            """)
        # ========================================================
        
        # STEP 4: 10 SECOND ACTIVE WAIT (Post-Click Redirect)
        print("⏳ Redirect hone ke liye agle 10 second wait aur mouse movement...")
        active_human_mouse_wait(driver, 10)
        
        # STEP 5: SMART BOOK DETECTION
        print("📚 Redirect complete! Random book search kar raha hoon...")
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/book/']")))
        except:
            pass 

        book_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/book/'], .book")
        
        if book_elements:
            target_book = random.choice(book_elements[:15])
            book_url = target_book.get_attribute("href")
            print(f"🔗 Random Book mili: {book_url}")
            
            driver.get(book_url)
            time.sleep(5)
            
            # STEP 6: PDF DOWNLOAD
            print("⬇️ PDF Download link dhund raha hoon...")
            pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
            
            if pdf_links:
                pdf_url = pdf_links[0].get_attribute("href")
                pdf_file_path = f"welib_book_{int(time.time())}.pdf"
                
                print(f"📄 PDF Download ho raha hai: {pdf_url}")
                ua = driver.execute_script("return navigator.userAgent;")
                r = requests.get(pdf_url, headers={"User-Agent": ua})
                
                with open(pdf_file_path, "wb") as f:
                    f.write(r.content)
                print("✅ PDF successfully downloaded!")
                
                # 📤 SEND PDF TO TELEGRAM
                send_telegram_file(pdf_file_path, "document", "📚 Random Book PDF (Welib.st)")
            else:
                print("❌ Is book ka PDF link nahi mila.")
        else:
            print("❌ Koi books load nahi hui screen par.")

    except Exception as e:
        print(f"❌ Automation Error: {e}")
    
    finally:
        # STEP 7: CLEANUP & SEND VIDEO
        print("🧹 Browser band kar raha hoon...")
        driver.quit()
        
        print("🛑 Screen recording stop kar raha hoon...")
        record_process.terminate()
        record_process.wait()
        
        # 📤 SEND VIDEO TO TELEGRAM
        if os.path.exists(video_filename):
            send_telegram_file(video_filename, "video", "📹 Automation Live Screen Recording (Text Position Logic)")
        else:
            print("❌ Video file save nahi ho payi!")

if __name__ == "__main__":
    run_automation()
