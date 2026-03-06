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
            # Timeout bada rakha hai kyunki video upload mein time lagta hai
            response = requests.post(url, files=files, data=data, timeout=60)
            
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
        
        # 2. Initial 10 Second Wait
        print("⏳ 10 second wait kar raha hoon...")
        time.sleep(10)
        
        # 3. Human Mouse Movement
        print("👤 Human ki tarah mouse idhar-udhar move kar raha hoon...")
        actions = ActionChains(driver)
        for _ in range(6):
            actions.move_by_offset(random.randint(-100, 100), random.randint(-80, 80)).perform()
            time.sleep(random.uniform(0.3, 0.8))
        
        # 4. Iframe Checkbox Click
        print("🎯 Iframe mein checkbox dhund raha hoon...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        clicked = False
        
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                targets = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"], .mark, #challenge-stage input')
                if targets and targets[0].is_displayed():
                    print("✅ Checkbox mil gaya! Mouse le jaa kar click kar raha hoon...")
                    
                    # Pehle thoda side mein move karega, fir checkbox par click karega
                    actions.move_to_element_with_offset(targets[0], -30, -15).perform()
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
            print("⚠️ Checkbox nahi mila ya automation ne pehle hi bypass kar diya hai.")

        # 5. Wait 10 Seconds for Redirect
        print("⏳ Click karne ke baad redirect hone ke liye 10 second wait kar raha hoon...")
        time.sleep(10)
        
        print("✅ Automation steps complete!")

    except Exception as e:
        print(f"❌ Error aaya: {e}")
    
    finally:
        # Browser band karna
        driver.quit()
        print("🔒 Browser closed.")
        
        # 🛑 SCREEN RECORDING STOP
        print("🛑 Screen recording stop kar raha hoon...")
        record_process.terminate()
        record_process.wait()
        
        # 📤 SEND VIDEO TO TELEGRAM
        if os.path.exists(video_filename):
            send_telegram_video(video_filename, "📹 Automation Screen Recording")
        else:
            print("❌ Video file create nahi hui!")

if __name__ == "__main__":
    run_automation()
