import os
import time
import random
import requests
import subprocess
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_file(file_path, file_type="document", caption=""):
    """Telegram par PDF ya Video bhejne ka universal function"""
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
        # STEP 1: Website open karna
        print("🌐 Website open kar raha hoon...")
        driver.get("https://welib.st")
        time.sleep(2)
        
        # 🔴 VISUAL RED CURSOR INJECT KARNA
        cursor_js = """
        let cursor = document.createElement('div');
        cursor.id = 'automation-cursor';
        cursor.style.width = '20px'; cursor.style.height = '20px';
        cursor.style.background = 'rgba(255, 0, 0, 0.8)';
        cursor.style.border = '2px solid black'; cursor.style.borderRadius = '50%';
        cursor.style.position = 'fixed'; cursor.style.zIndex = '999999';
        cursor.style.pointerEvents = 'none';
        document.body.appendChild(cursor);
        document.addEventListener('mousemove', function(e) {
            cursor.style.left = (e.clientX - 10) + 'px';
            cursor.style.top = (e.clientY - 10) + 'px';
        });
        """
        driver.execute_script(cursor_js)
        
        # STEP 2: 10 SECOND ACTIVE WAIT (Pre-Click)
        print("⏳ 10 second tak mouse idhar-udhar move kar raha hoon (Anti-Bot Bypass)...")
        active_human_mouse_wait(driver, 10)
        
        # STEP 3: ENHANCED IFRAME CHECKBOX TICK + TEXT DETECTION + RED DOT
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

        # === STEP 3: ADJUSTED PROXIMITY-BASED IFRAME CHECKBOX TICK ===
        print("🎯 Iframe mein Cloudflare checkbox dhund raha hoon (Proximity Logic)...")

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        clicked = False

        for iframe in iframes:
            try:
                print(f"🔍 Iframe #{len([i for i in iframes if i == iframe])} check kar raha hoon...")
                driver.switch_to.frame(iframe)
                
                # "VERIFY YOU ARE HUMAN" TEXT + CHECKBOX DETECTION
                verify_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verify you are human') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verify human') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verify u r human') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'automation')]")
                checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], .mark, #challenge-stage input, [role="checkbox"], .cf-turnstile input, .cf-checkbox input, #turnstile-checkbox, .human-challenge input')
                
                print(f"📝 Verify text mila: {len(verify_elements)} | Checkboxes: {len(checkboxes)}")
                
                if checkboxes or verify_elements:
                    # GREEN HIGHLIGHT checkbox
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
                            console.log('🟢 CHECKBOX HIGHLIGHTED!');
                        """, checkboxes[0])
                    
                    # **PERFECT LOGIC: Verify text ke BAGAL mein checkbox dhundo**
                    target_checkbox = None
                    for verify_text in verify_elements:
                        nearby_checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], .mark, [role="checkbox"]')
                        for cb in nearby_checkboxes:
                            try:
                                rect_text = verify_text.rect
                                rect_cb = cb.rect
                                
                                distance_x = abs(rect_text['x'] - rect_cb['x'])
                                distance_y = abs(rect_text['y'] - rect_cb['y'])
                                
                                if distance_x < 150 and distance_y < 80:  # BAGAL mein hai!
                                    target_checkbox = cb
                                    print(f"🎯 VERIFICATION TEXT KE BAGAL MEIN CHECKBOX MILA! Distance: X={distance_x}, Y={distance_y}")
                                    break
                            except:
                                continue
                        if target_checkbox:
                            break
                    
                    # Fallback agar proximity nahi mila to pehla checkbox
                    if not target_checkbox and checkboxes:
                        target_checkbox = checkboxes[0]
                        print("🔄 Proximity nahi mila, direct checkbox use kar raha hoon")
                    
                    if target_checkbox:
                        target_text = verify_elements[0] if verify_elements else target_checkbox
                        
                        print("🖱️ Human path: Text ke BAGAL → Checkbox → PERFECT CLICK...")
                        actions = ActionChains(driver)
                        
                        # Phase 1: Screen-left se natural start
                        actions.move_by_offset(50, 450).pause(0.4).perform()
                        print("✅ Phase 1: Screen-left position")
                        
                        # Phase 2: "Verify you are human" TEXT PE PEHLE JAO
                        actions.move_to_element(target_text).pause(1.0).perform()
                        print("✅ Phase 2: VERIFY TEXT PE CURSOR - reading...")
                        time.sleep(0.6)
                        
                        # Phase 3: BAGAL mein checkbox ki taraf smooth curve
                        actions.move_to_element_with_offset(target_checkbox, random.randint(-5,5), random.randint(-8,8)).pause(0.3).perform()
                        print("✅ Phase 3: BAGAL mein CHECKBOX pe move")
                        
                        # Phase 4: **TIK-TIK** PRECISE CENTER CLICK with pressure
                        actions.move_to_element(target_checkbox).pause(0.5).perform()
                        print("🎯 Phase 4: CHECKBOX CENTER LOCK - TIK TIK PRESSURE CLICK...")
                        
                        # DOUBLE PRESSURE CLICK for 100% success
                        actions.click_and_hold(target_checkbox).pause(0.15).release().pause(0.1).click(target_checkbox).perform()
                        
                        print("✅ ✅ CHECKBOX TIK DIYA! DOUBLE CONFIRMED! 🎉")
                        clicked = True
                        
                        # Screenshot success
                        driver.save_screenshot(f"images/03_checkbox_clicked_iframe_{len(iframes)}.png")
                        send_telegram_file(f"images/03_checkbox_clicked_iframe_{len(iframes)}.png", "photo", f"✅ CHECKBOX TIK DIYA! Iframe #{len([i for i in iframes if i == iframe])}")
                        
                        driver.switch_to.default_content()
                        break
                    else:
                        print("❌ Koi suitable checkbox nahi mila is iframe mein")
                        driver.switch_to.default_content()
                        continue
                        
            except Exception as e:
                print(f"⚠️ Iframe error: {str(e)[:100]}")
                try:
                    driver.switch_to.default_content()
                except:
                    pass
                continue

        driver.switch_to.default_content()

        if not clicked:
            print("🚀 FINAL NUCLEAR BACKUP - All iframes fail hone pe...")
            driver.execute_script("""
                document.querySelectorAll('input[type="checkbox"], [role="checkbox"], .mark').forEach(cb => {
                    cb.checked = true;
                    cb.click();
                    cb.dispatchEvent(new Event('change', {bubbles: true}));
                    cb.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                });
                console.log('💥💥 NUCLEAR JS + MOUSE EVENT DEPLOYED!');
            """)
            time.sleep(2)

        print("🎉 Cloudflare checkbox mission COMPLETE!")

        # 8s POST-CLICK HUMAN WAIT with RED DOT tracking
        print("⏳ 8s human wait - RED DOT active...")
        for i in range(4):
            driver.execute_script(f"window.scrollBy(0, {random.randint(-30, 30)});")
            time.sleep(random.uniform(1.8, 2.2))

        print("✅ IFRAME CHECKBOX MISSION COMPLETE! RED DOT tracking OFF")
        driver.execute_script("document.getElementById('cursor-tracker')?.remove();")
        
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
        
        if os.path.exists(video_filename):
            send_telegram_file(video_filename, "video", "📹 Automation Live Screen Recording (Text + Box Hover)")
        else:
            print("❌ Video file save nahi ho payi!")

if __name__ == "__main__":
    run_automation()
