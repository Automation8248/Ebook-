import os
import time
import random
import requests
import subprocess
from datetime import datetime
from playwright.sync_api import sync_playwright

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_photo(page, caption=""):
    """Screenshot Telegram par bhejne ka function (Playwright Version)"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"images/{timestamp}_pw_welib.png"
    os.makedirs("images", exist_ok=True)
    
    # Take screenshot using Playwright
    page.screenshot(path=screenshot_path)
    
    try:
        with open(screenshot_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]}
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto", files=files, data=data)
    except Exception as e:
        print(f"❌ Photo Error: {e}")

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

def run_playwright_automation():
    print("🚀 Naya Playwright Automation shuru ho raha hai...")

    # 🎥 SCREEN RECORDING START (FFMPEG)
    display = os.environ.get('DISPLAY', ':99')
    video_filename = f"automation_record_{int(time.time())}.mp4"
    print("🎥 Screen recording start...")
    
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-f', 'x11grab', '-video_size', '1920x1080',
        '-framerate', '15', '-i', f'{display}', '-codec:v', 'libx264',
        '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', video_filename
    ]
    # Start recording subprocess
    record_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ## IMPORTANT ##
    ## Aapki pw_CAPTCHA.py file se proxy configuration
    proxies = {
      "server": "http://brd.superproxy.io:33335",
      "username": 'brd-customer-<customer_id>-zone-<zone-name>',
      "password": '<zone-password>'
    }

    try:
        # initialize playwright
        with sync_playwright() as pw:
            # create Firefox browser object
            print("🦊 Firefox Browser launch kar raha hoon...")
            browser = pw.firefox.launch(
                headless=False, 
                slow_mo=150, # Actions ko dhima karne ke liye
                # proxy=proxies # Agar premium proxy use karni ho to ise uncomment karein
            )

            # create new browser context & tab
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()

            # 🔴 RED DOT CURSOR INJECTOR (Har page par chalega)
            page.add_init_script("""
                window.addEventListener('DOMContentLoaded', () => {
                    let redDot = document.createElement('div');
                    redDot.id = 'mouse-tracker';
                    redDot.style.cssText = `
                        position: fixed; z-index: 9999999; width: 16px; height: 16px;
                        background: radial-gradient(circle, #ff4444 30%, #ff0000 60%, transparent);
                        border: 3px solid #ffffff; border-radius: 50%; 
                        box-shadow: 0 0 15px #ff0000; pointer-events: none; transform: translate(-50%, -50%);
                    `;
                    document.body.appendChild(redDot);
                    document.addEventListener('mousemove', (e) => {
                        redDot.style.left = e.pageX + 'px';
                        redDot.style.top = e.pageY + 'px';
                    });
                });
            """)

            # navigate to web page
            print("🌐 https://welib.st par jaa raha hoon...")
            page.goto("https://welib.st", wait_until="domcontentloaded")
            time.sleep(3) # Initial load wait

            # ⏳ 10 SECONDS ACTIVE MOUSE MOVEMENT
            print("⏳ 10s Pre-Wait: Screen par mouse hila raha hoon...")
            for _ in range(5):
                page.mouse.move(random.randint(100, 1000), random.randint(100, 600), steps=15)
                time.sleep(random.uniform(1.0, 2.0))

            # 🎯 CLOUDFLARE IFRAME DETECTION (Playwright Way)
            print("🔍 Iframe aur Security box dhund raha hoon...")
            clicked = False
            
            # Playwright mein frames ko asani se iterate kar sakte hain
            for frame in page.frames:
                try:
                    # 'Verify you are human' text ya checkbox ka CSS/XPath dhundna
                    verify_text_locator = frame.locator("text=/verify.*human|u r|automation/i")
                    checkbox_locator = frame.locator("input[type='checkbox'], .mark, [role='checkbox']")
                    
                    if verify_text_locator.count() > 0 or checkbox_locator.count() > 0:
                        print(f"🎯 Iframe pakda gaya! URL: {frame.url[:40]}...")
                        
                        target_element = None
                        
                        if verify_text_locator.count() > 0:
                            target_element = verify_text_locator.first
                            print(f"📝 Text mila: {target_element.inner_text()}")
                        elif checkbox_locator.count() > 0:
                            target_element = checkbox_locator.first
                            print("📦 Direct checkbox mila.")
                        
                        if target_element:
                            # Element ka absolute bounding box nikalna
                            box = target_element.bounding_box()
                            
                            if box:
                                # Screen-left start
                                page.mouse.move(80, 420, steps=10)
                                time.sleep(0.5)
                                
                                # Calculate exact human center with slight random offset
                                target_x = box['x'] + (box['width'] / 2) + random.randint(-10, 10)
                                target_y = box['y'] + (box['height'] / 2) + random.randint(-5, 5)
                                
                                print("🖱️ VISIBLE PATH: Text/Box ki taraf curve movement...")
                                page.mouse.move(target_x, target_y, steps=25)
                                time.sleep(0.6) # Hesitation
                                
                                print("🎯 DOUBLE PRESSURE CLICK - TIK TIK!")
                                page.mouse.down()
                                time.sleep(0.18)
                                page.mouse.up()
                                time.sleep(0.1)
                                page.mouse.down()
                                time.sleep(0.12)
                                page.mouse.up()
                                
                                print("✅✅✅ TIK DIYA! Security badha di gayi.")
                                clicked = True
                                
                                send_telegram_photo(page, "✅✅ Playwright se Box par TIK kiya! (Red Dot Visible)")
                                break
                except Exception as e:
                    continue

            if not clicked:
                print("⚠️ Checkbox visible nahi mila, Playwright force click backup...")
                try:
                    page.locator("iframe").first.frame_locator("input[type='checkbox']").click(force=True)
                    print("💥 Force click executed!")
                except:
                    pass

            # ⏳ 10 SECONDS WAIT AFTER TICK
            print("⏳ Security Validate ho rahi hai... 10 second wait kar raha hoon...")
            for _ in range(5):
                page.mouse.move(random.randint(200, 800), random.randint(200, 800), steps=10)
                time.sleep(2)

            print("🎉 Playwright Automation Script Complete!")
            browser.close()

    except Exception as e:
        print(f"❌ Automation Error: {e}")
        
    finally:
        # STEP 7: CLEANUP & SEND VIDEO
        print("🛑 Screen recording stop kar raha hoon...")
        record_process.terminate()
        record_process.wait()
        
        # 📤 SEND VIDEO TO TELEGRAM
        if os.path.exists(video_filename):
            send_telegram_file(video_filename, "video", "📹 Playwright Automation Live Screen Recording")
        else:
            print("❌ Video file save nahi ho payi!")

if __name__ == "__main__":
    run_playwright_automation()
