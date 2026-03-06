import os
import time
import random
import requests
import subprocess
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_video(video_path, caption=""):
    """Video ko Telegram par send karne ka function"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram Token ya Chat ID missing hai!")
        return

    print(f"📤 Telegram par video bhej raha hoon: {video_path}")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    
    try:
        with open(video_path, "rb") as video:
            files = {"video": video}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            response = requests.post(url, files=files, data=data, timeout=120)
            
        if response.status_code == 200:
            print("✅ Video successfully sent to Telegram! 🎉")
        else:
            print(f"❌ Video bhejne mein error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

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
    # Background mein recording chalu
    record_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 🕵️ DRIVER SETUP
    driver = Driver(
        uc=True,
        headless=False, # Xvfb ke liye headless=False hona zaroori hai
        disable_csp=True,
        undetectable=True,
        window_size="1920,1080",
        no_sandbox=True
    )

    try:
        # 1. Website par jana
        print("🌐 Website open kar raha hoon...")
        driver.get("https://welib.st")
        time.sleep(2) # Page load hone ke liye thoda time
        
        # 🟢 VISUAL CURSOR INJECTION 🟢
        # GitHub Actions ki video mein mouse dikhane ke liye ek Red Dot banayenge
        cursor_js = """
        let cursor = document.createElement('div');
        cursor.id = 'automation-cursor';
        cursor.style.width = '20px';
        cursor.style.height = '20px';
        cursor.style.background = 'rgba(255, 0, 0, 0.7)';
        cursor.style.border = '2px solid black';
        cursor.style.borderRadius = '50%';
        cursor.style.position = 'fixed';
        cursor.style.zIndex = '999999';
        cursor.style.pointerEvents = 'none';
        document.body.appendChild(cursor);
        document.addEventListener('mousemove', function(e) {
            cursor.style.left = (e.clientX - 10) + 'px';
            cursor.style.top = (e.clientY - 10) + 'px';
        });
        """
        driver.execute_script(cursor_js)
        
        actions = ActionChains(driver)
        
        # 2. ACTIVE 10-SECOND WAIT (Human Mouse Movement)
        print("⏳ 10 second tak mouse ko screen par idhar-udhar move kar raha hoon...")
        end_time = time.time() + 10
        
        # Mouse ko screen ke center mein lana
        try:
            actions.move_to_element(driver.find_element(By.TAG_NAME, "body")).perform()
        except:
            pass
            
        while time.time() < end_time:
            # Randomly upar, niche, aage, piche
            x_offset = random.randint(-300, 300)
            y_offset = random.randint(-300, 300)
            try:
                actions.move_by_offset(x_offset, y_offset).perform()
            except:
                # Agar mouse screen ke bahar chala jaye, toh wapas body par le aao
                actions.move_to_element(driver.find_element(By.TAG_NAME, "body")).perform()
            
            time.sleep(random.uniform(0.5, 1.5)) # Human hesitation
        
        # 3. Iframe Checkbox Click
        print("🎯 10 second pure hue! Ab Iframe mein checkbox dhund raha hoon...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        clicked = False
        
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                targets = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], .mark, #challenge-stage input')
                if targets and targets[0].is_displayed():
                    print("✅ Checkbox mil gaya! Mouse le jaa kar click kar raha hoon...")
                    
                    # Dheere se checkbox ki taraf badhna aur tick karna
                    actions.move_to_element_with_offset(targets[0], -20, -10).perform()
                    time.sleep(1)
                    actions.move_to_element(targets[0]).pause(0.5).click().perform()
                    
                    clicked = True
                    driver.switch_to.default_content()
                    break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                continue
        
        if not clicked:
            print("⚠️ Checkbox nahi mila ya pehle hi verify ho gaya hai.")

        # 4. ACTIVE 10-SECOND REDIRECT WAIT
        print("⏳ Click karne ke baad redirect hone ke liye agle 10 second wait kar raha hoon...")
        redirect_end_time = time.time() + 10
        while time.time() < redirect_end_time:
            try:
                # Redirect hone tak thoda bahut mouse hilate raho taaki freeze na lage
                actions.move_by_offset(random.randint(-50, 50), random.randint(-50, 50)).perform()
            except:
                pass
            time.sleep(1)
        
        print("✅ Automation steps complete! Naya interface open ho gaya hoga.")

    except Exception as e:
        print(f"❌ Error aaya: {e}")
    
    finally:
        # Browser band karna
        driver.quit()
        print("🔒 Browser closed.")
        
        # 🛑 SCREEN RECORDING STOP
        print("🛑 Screen recording band kar raha hoon...")
        record_process.terminate()
        record_process.wait()
        
        # 📤 SEND VIDEO TO TELEGRAM
        if os.path.exists(video_filename):
            send_telegram_video(video_filename, "📹 Automation Live Screen Recording (With Human Mouse)")
        else:
            print("❌ Video file create nahi hui!")

if __name__ == "__main__":
    run_automation()
