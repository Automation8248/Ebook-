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
        # Pehle mouse ko body ke center mein late hain
        body = driver.find_element(By.TAG_NAME, "body")
        ActionChains(driver).move_to_element(body).perform()
    except:
        pass

    while time.time() < end_time:
        x_offset = random.randint(-250, 250)
        y_offset = random.randint(-250, 250)
        try:
            # Mouse ko upar, niche, left, right move karna
            ActionChains(driver).move_by_offset(x_offset, y_offset).perform()
        except:
            # Agar mouse window se bahar jaye, toh reset kar do
            try:
                ActionChains(driver).move_to_element(driver.find_element(By.TAG_NAME, "body")).perform()
            except:
                pass
        
        # Thoda human hesitation (rukna)
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
        headless=False, # Xvfb ke liye False hona zaroori hai
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
        
        # 🔴 VISUAL RED CURSOR INJECT KARNA (Video mein mouse dikhane ke liye)
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
        
        # STEP 3: IFRAME CHECKBOX TICK
        print("🎯 Iframe mein Cloudflare checkbox dhund raha hoon...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        clicked = False
        
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                targets = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], .mark, #challenge-stage input')
                if targets and targets[0].is_displayed():
                    print("✅ Checkbox mil gaya! Mouse se click kar raha hoon...")
                    
                    # Human path to checkbox
                    ActionChains(driver).move_to_element_with_offset(targets[0], -20, -10).perform()
                    time.sleep(0.8)
                    ActionChains(driver).move_to_element(targets[0]).pause(0.5).click().perform()
                    
                    clicked = True
                    driver.switch_to.default_content()
                    break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                continue
        
        if not clicked:
            print("⚠️ Checkbox nahi mila ya automation ne pehle hi verify kar liya hai.")

        # STEP 4: 10 SECOND ACTIVE WAIT (Post-Click Redirect)
        print("⏳ Redirect hone ke liye agle 10 second wait aur mouse movement...")
        active_human_mouse_wait(driver, 10)
        
        # STEP 5: SMART BOOK DETECTION
        print("📚 Redirect complete! Random book search kar raha hoon...")
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/book/']")))
        except:
            pass # Timeout ke baad bhi continue karenge

        book_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/book/'], .book")
        
        if book_elements:
            target_book = random.choice(book_elements[:15]) # Top 15 books me se ek uthana
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
                # Same user-agent ke sath requests se download karna
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
            send_telegram_file(video_filename, "video", "📹 Automation Live Screen Recording (Bypass + Download)")
        else:
            print("❌ Video file save nahi ho payi!")

if __name__ == "__main__":
    run_automation()
