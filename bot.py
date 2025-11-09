import requests
import time
import os

BOT_TOKEN = "6080405612:AAFzpqJQfrjmn5MJQe8tlKLzwk-mYdN318Y"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=data)

def download_tiktok(url):
    try:
        api_url = "https://www.tikwm.com/api/"
        response = requests.post(api_url, data={"url": url}, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                video_url = result["data"]["play"]
                
                # إصلاح الرابط إذا كان نسبياً
                if video_url.startswith('//'):
                    video_url = 'https:' + video_url
                elif video_url.startswith('/'):
                    video_url = 'https://www.tikwm.com' + video_url
                
                # تحميل الفيديو
                video_response = requests.get(video_url, stream=True, timeout=60)
                if video_response.status_code == 200:
                    filename = f"tiktok_{int(time.time())}.mp4"
                    with open(filename, 'wb') as f:
                        for chunk in video_response.iter_content(8192):
                            f.write(chunk)
                    return filename
        return None
    except:
        return None

def send_video(chat_id, video_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(video_path, 'rb') as video_file:
        files = {'video': video_file}
        data = {'chat_id': chat_id, 'caption':"✅ \nالفيديو بدون علامة مائية 🎵"}
        response = requests.post(url, files=files, data=data, timeout=60)
        return response.status_code == 200

# البوت الرئيسي
print("🤖 بوت تيك توك يعمل...")
last_id = 0

while True:
    try:
        # الحصول على الرسائل
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        response = requests.get(url, params={"offset": last_id + 1, "timeout": 30})
        
        if response.status_code == 200:
            updates = response.json().get("result", [])
            
            for update in updates:
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")
                    
                    if text.startswith("/start"):
                        send_message(chat_id, "🎵 أرسل رابط تيك توك للتحميل \n instagram : 5r5_4 \n tiktok : 5r5_9 \n telegram : @rrr5_4")
                    
                    elif "tiktok.com" in text:
                        send_message(chat_id, "⏳ جاري التحميل...")
                        video_file = download_tiktok(text)
                        
                        if video_file:
                            send_video(chat_id, video_file)
                            os.remove(video_file)
                        else:
                            send_message(chat_id, "❌ فشل التحميل")
                    
                    last_id = update["update_id"]
        
        time.sleep(1)
        
    except Exception as e:
        print(f"خطأ: {e}")
        time.sleep(5)