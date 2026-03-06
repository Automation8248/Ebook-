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
    """Screenshot save karke Telegram par bhejne ka function"""
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
        print("⚠️ Telegram Config missing hai!")
        return

    print(f"📤 Telegram par {file_type} bhej raha hoon: {file_path}")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/send{file_type.capitalize()}"
    
    try:
        with open(file_path, "rb") as f:
            files = {file_type: f}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            response = requests.post(url, files=files, data=data, timeout=120)
        if response.status_code == 200:
            print(f"✅ {file_type.capitalize()} sent successfully!")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def active_human_mouse_wait(driver, duration=10):
    """10 Second tak mouse ko screen par random ghumane ka logic"""
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
    
    # 🎥 SCREEN RECORDING START
    display = os.environ.get('DISPLAY', ':99')
    video_filename = f"automation_record_{int(time.time())}.mp4"
    print("🎥 Screen recording start...")
    
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-f', 'x11grab', '-video_size', '1920x1080',
        '-framerate', '15', '-i', f'{display}', '-codec:v', 'libx264',
        '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', video_filename
    ]
    record_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 🕵️ DRIVER SETUP (No uc_subdomains)
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
        
        # 🟢 10 SECOND ACTIVE WAIT (Pre-Click)
        print("⏳ 10 second tak mouse idhar-udhar move kar raha hoon...")
        active_human_mouse_wait(driver, 10)
        
        # ========================================================
        # 🔥 STEP 3: ENHANCED IFRAME CHECKBOX TICK + RED DOT HIGHLIGHT
        # ========================================================
        print("🎯 Iframe mein Cloudflare checkbox dhund raha hoon + RED DOT TRACKING...")

        driver.execute_script("""
            let redDot = document.createElement('div');
            redDot.id = 'cursor-tracker';
            redDot.style.cssText = `
                position: fixed; z-index: 999999; width: 12px; height: 12px; 
                background: radial-gradient(circle, #ff0000 40%, transparent 50%); 
                border: 2px solid #ff4444; border-radius: 50%; box-shadow: 0 0 10px #ff0000;
                pointer-events: none; transform: translate(-50%, -50%);
            `;
            document.body.appendChild(redDot);
            
            let tracker = redDot;
            document.addEventListener('mousemove', (e) => {
                tracker.style.left = e.pageX + 'px';
                tracker.style.top = e.pageY + 'px';
            });
            console.log('🔴 RED DOT TRACKER ACTIVATED!');
        """)

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        clicked = False

        for iframe in iframes:
            try: # <-- Yahan try block shuru hua
                print(f"🔍 Iframe check kar raha hoon...")
                driver.switch_to.frame(iframe)
                
                verify_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verify you are human') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verify human')]")
                checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], .mark, #challenge-stage input, [role="checkbox"], .cf-turnstile input')
                
                if checkboxes or verify_elements:
                    if checkboxes:
                        driver.execute_script("""
                            let checkbox = arguments[0];
                            let highlight = document.createElement('div');
                            highlight.style.cssText = `
                                position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                                border: 4px solid #00ff00; border-radius: 50%; 
                                box-shadow: 0 0 20px #00ff00; z-index: 99998; pointer-events: none;
                                background: radial-gradient(circle, rgba(0,255,0,0.1) 0%, transparent 70%);
                            `;
                            checkbox.parentNode.style.position = 'relative';
                            checkbox.parentNode.appendChild(highlight);
                        """, checkboxes[0])
                        send_telegram_photo(driver, "🔍 Checkbox highlighted with GREEN dots")
                    
                    target = checkboxes[0] if checkboxes else verify_elements[0]
                    print("🖱️ Human path start: Left → Hesitate → Curve → Click...")
                    
                    actions = ActionChains(driver)
                    actions.move_by_offset(50, 450).pause(0.3).perform()
                    actions.move_to_element_with_offset(target, 280, 430).pause(0.8).perform()
                    time.sleep(0.5)
                    
                    actions.move_by_offset(120 + random.randint(-10,10), -25).pause(0.22).perform()
                    actions.move_by_offset(80 + random.randint(-5,5), 15).pause(0.15).perform()
                    
                    center_offset_x = random.randint(-8, 8)
                    center_offset_y = random.randint(-5, 5)
                    actions.move_to_element_with_offset(target, center_offset_x, center_offset_y).pause(0.4).perform()
                    
                    actions.click_and_hold(target).pause(random.uniform(0.12, 0.18)).release().perform()
                    print("✅ CHECKBOX SUCCESSFULLY CLICKED! 🎉")
                    clicked = True
                    
                    send_telegram_photo(driver, "✅ CHECKBOX CLICKED!")
                    driver.switch_to.default_content()
                    break

            except Exception as e: # <-- Yahan except block theek se lagaya gaya hai
                print(f"⚠️ Iframe error: {e}")
                driver.switch_to.default_content()
                continue

        driver.switch_to.default_content()

        if not clicked:
            print("⚠️ Checkbox nahi mila ya verify ho gaya - Nuclear JS fallback...")
            driver.execute_script("""
                document.querySelectorAll('input[type="checkbox"], [role="checkbox"]').forEach(cb => {
                    cb.checked = true;
                    cb.click();
                    cb.dispatchEvent(new Event('change', {bubbles: true}));
                });
            """)

        print("⏳ 8s human wait - RED DOT active...")
        for i in range(4):
            driver.execute_script(f"window.scrollBy(0, {random.randint(-30, 30)});")
            time.sleep(random.uniform(1.8, 2.2))

        driver.execute_script("document.getElementById('cursor-tracker')?.remove();")
        
        # ========================================================
        
        # 🟢 10 SECOND ACTIVE WAIT (Post-Click Redirect)
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
                
                ua = driver.execute_script("return navigator.userAgent;")
                r = requests.get(pdf_url, headers={"User-Agent": ua})
                
                with open(pdf_file_path, "wb") as f:
                    f.write(r.content)
                print("✅ PDF successfully downloaded!")
                
                send_telegram_file(pdf_file_path, "document", "📚 Random Book PDF (Welib.st)")
            else:
                print("❌ Is book ka PDF link nahi mila.")
        else:
            print("❌ Koi books load nahi hui screen par.")

    except Exception as e:
        print(f"❌ Automation Error: {e}")
    
    finally:
        print("🧹 Browser band kar raha hoon...")
        driver.quit()
        
        print("🛑 Screen recording stop kar raha hoon...")
        record_process.terminate()
        record_process.wait()
        
        if os.path.exists(video_filename):
            send_telegram_file(video_filename, "video", "📹 Automation Live Screen Recording")
        else:
            print("❌ Video file save nahi ho payi!")

if __name__ == "__main__":
    run_automation()
