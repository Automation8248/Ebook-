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
    """Screenshot Telegram par bhejne ka function"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"images/{timestamp}_pw_welib.png"
    os.makedirs("images", exist_ok=True)
    page.screenshot(path=screenshot_path)
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
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/send{file_type.capitalize()}"
    try:
        with open(file_path, "rb") as f:
            files = {file_type: f}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            requests.post(url, files=files, data=data, timeout=120)
    except Exception as e:
        pass

# ==========================================
# USER KA PART 1: pw_CAPTCHA.py (ADDED EXACLTY AS REQUESTED)
# ==========================================
def part1_walmart_captcha():
    print("🚀 Running Part 1: pw_CAPTCHA.py logic...")
    ## IMPORTANT ##
    ## fill the dictionary below with your details ##
    proxies = {
      "server": "http://brd.superproxy.io:33335",
      "username": 'brd-customer-<customer_id>-zone-<zone-name>',
      "password": '<zone-password>'
    }

    # initiallize playwright
    pw = sync_playwright().start()

    # create Firefox browser object
    browser = pw.firefox.launch(
        # uncomment the lines below if you're using a web driver
        #headless=False, 
        #slow_mo=2000,
        proxy=proxies
    )

    # create new browser tab
    page = browser.new_page()
    # navigate to web page locked by CAPTCHA
    try:
        page.goto("http://www.walmart.com")
        # locate search input
        page.locator("xpath=//input[@aria-label='Search']").fill("testing")
        # submit search term
        page.keyboard.press('Enter')
    except Exception as e:
        print(f"⚠️ Part 1 (Walmart) Proxy Error (Fake Credentials ki wajah se): {e}")

    browser.close()
    pw.stop()

# ==========================================
# USER KA PART 2: pw_quickstart.py (ADDED EXACTLY AS REQUESTED)
# ==========================================
def part2_google_quickstart():
    print("🚀 Running Part 2: pw_quickstart.py logic...")
    # initiallize playwright
    pw = sync_playwright().start()
    # create Firefox browser object
    browser = pw.firefox.launch(
        # uncomment the lines below if you're using a web driver
        #headless=False, 
        #slow_mo=2000
    )

    # create new browser tab
    page = browser.new_page()
    # navigate to web page
    page.goto("https://google.com")

    # web page details and source code
    print("Google Page Title:", page.title())
    page.screenshot(path="google_screenshot.png")

    browser.close()
    pw.stop()

# ==========================================
# MAIN AUTOMATION: Welib Cloudflare logic
# ==========================================
def run_playwright_automation():
    print("🚀 Main Playwright Automation shuru ho raha hai...")

    display = os.environ.get('DISPLAY', ':99')
    video_filename = f"automation_record_{int(time.time())}.mp4"
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-f', 'x11grab', '-video_size', '1920x1080',
        '-framerate', '15', '-i', f'{display}', '-codec:v', 'libx264',
        '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', video_filename
    ]
    record_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        with sync_playwright() as pw:
            browser = pw.firefox.launch(headless=False, slow_mo=150)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()

            # RED DOT CURSOR INJECTOR
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

            page.goto("https://welib.st", wait_until="domcontentloaded")
            time.sleep(3) 

            for _ in range(5):
                page.mouse.move(random.randint(100, 1000), random.randint(100, 600), steps=15)
                time.sleep(random.uniform(1.0, 2.0))

            clicked = False
            for frame in page.frames:
                try:
                    verify_text_locator = frame.locator("text=/verify.*human|u r|automation/i")
                    checkbox_locator = frame.locator("input[type='checkbox'], .mark, [role='checkbox']")
                    
                    if verify_text_locator.count() > 0 or checkbox_locator.count() > 0:
                        target_element = verify_text_locator.first if verify_text_locator.count() > 0 else checkbox_locator.first
                        box = target_element.bounding_box()
                        
                        if box:
                            page.mouse.move(80, 420, steps=10)
                            time.sleep(0.5)
                            
                            target_x = box['x'] + (box['width'] / 2) + random.randint(-10, 10)
                            target_y = box['y'] + (box['height'] / 2) + random.randint(-5, 5)
                            
                            page.mouse.move(target_x, target_y, steps=25)
                            time.sleep(0.6) 
                            
                            page.mouse.down()
                            time.sleep(0.18)
                            page.mouse.up()
                            time.sleep(0.1)
                            page.mouse.down()
                            time.sleep(0.12)
                            page.mouse.up()
                            
                            clicked = True
                            send_telegram_photo(page, "✅✅ Playwright se Box par TIK kiya! (Red Dot Visible)")
                            break
                except Exception as e:
                    continue

            if not clicked:
                try:
                    page.locator("iframe").first.frame_locator("input[type='checkbox']").click(force=True)
                except:
                    pass

            for _ in range(5):
                page.mouse.move(random.randint(200, 800), random.randint(200, 800), steps=10)
                time.sleep(2)

            browser.close()

    except Exception as e:
        print(f"❌ Automation Error: {e}")
        
    finally:
        record_process.terminate()
        record_process.wait()
        if os.path.exists(video_filename):
            send_telegram_file(video_filename, "video", "📹 Playwright Automation Live Screen Recording")

if __name__ == "__main__":
    # Part 2 (Google Test) Run hoga
    part2_google_quickstart()
    
    # Part 1 (Walmart Proxy Test) Run hoga. NOTE: Fake proxy details hone ki wajah se error aayega!
    part1_walmart_captcha()
    
    # Main Automation Run hoga
    run_playwright_automation()
